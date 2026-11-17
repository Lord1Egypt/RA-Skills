#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
zhc LSP 语言服务（stdio，零第三方依赖）

能力：
1. 实时诊断：直接复用 zhc.py 的词法/语法分析，把「第 N 行：……」转成 LSP Diagnostic
2. 补全：关键字、类型词、内置函数（自动补左括号）、当前文档已定义的变量
3. 悬停：内置函数签名与说明、类型说明、关键字说明
4. 文档符号：定义/函数，供大纲与面包屑使用

编译器定位顺序（找到 zhc.py 所在目录任意一处即可）：
    1. 客户端 initializationOptions.zhcPath / initializationOptions.zhcHome
    2. 环境变量 ZHC_HOME
    3. 本脚本相对位置（编辑器/zhc-lsp -> zhc）、当前目录、及其向上若干层
定位采用惰性加载：启动时找不到不会退出，客户端后续补传路径仍可恢复诊断。

启动（任意 LSP 客户端）：
    python zhc_lsp.py
自检：
    python zhc_lsp.py --自检
"""

import importlib
import json
import os
import re
import sys

_zhc = None
ZHC_DIR = ""
_已告警无编译器 = False


def 找编译器目录(额外=None):
    """定位含 zhc.py 的目录：显式路径 > ZHC_HOME > 脚本相对位置 > 工作目录向上。"""
    候选 = []
    if 额外:
        候选.append(额外)
    环境 = os.environ.get("ZHC_HOME", "").strip()
    if 环境:
        候选.append(环境)
    本处 = os.path.dirname(os.path.abspath(__file__))
    候选.append(os.path.abspath(os.path.join(本处, "..", "..")))  # 编辑器/zhc-lsp -> zhc
    候选.append(os.path.abspath(os.path.join(本处, "..")))
    候选.append(本处)
    向上 = os.getcwd()
    for _ in range(6):
        候选.append(向上)
        候选.append(os.path.join(向上, "zhc"))
        上级 = os.path.dirname(向上)
        if 上级 == 向上:
            break
        向上 = 上级
    for d in 候选:
        if not d:
            continue
        if os.path.isfile(d):
            d = os.path.dirname(d)
        if os.path.isfile(os.path.join(d, "zhc.py")):
            return os.path.abspath(d)
    return ""


def 加载编译器(目录=None):
    """惰性导入 zhc 模块；成功返回模块，失败返回 None。"""
    global _zhc, ZHC_DIR
    目标 = 找编译器目录(目录)
    if not 目标:
        return None
    if 目标 not in sys.path:
        sys.path.insert(0, 目标)
    ZHC_DIR = 目标
    try:
        if "zhc" in sys.modules:
            _zhc = sys.modules["zhc"]
        else:
            _zhc = importlib.import_module("zhc")
    except Exception as e:
        sys.stderr.write(f"[zhc-lsp] 导入 zhc.py 失败（{目标}）：{type(e).__name__}: {e}\n")
        _zhc = None
    return _zhc


def 取模块():
    if _zhc is None:
        加载编译器()
    return _zhc


文档 = {}  # uri -> 全文

# ---------------------------------------------------------------- 静态词表

关键字说明 = {
    "定义": "声明变量：定义 名 为 类型 初值",
    "设": "赋值：设 名 为 表达式",
    "输出": "输出到控制台：输出 值, 值2 …（可多个，自动以空格分隔）",
    "输入": "读取一行控制台输入：输入(提示)",
    "如果": "条件：如果 条件 则 … 结束（可接 否则如果 / 否则）",
    "否则如果": "否则如果 条件 则 …",
    "否则": "否则 …（与 如果 配对）",
    "当": "当型循环：当 条件 则 … 结束",
    "循环": "计数循环：循环 变量 从 起 到 止 步 步长 … 结束",
    "结束": "结束当前块（如果 / 当 / 循环 / 函数）",
    "则": "条件与循环块的块头结束标记",
    "函数": "函数定义：函数 名(参数:类型,…) 返回 类型 … 结束",
    "返回": "从函数返回：返回 表达式",
    "外部": "声明外部函数：外部 函数 名(参数:类型,…) 返回 类型（符号名须为 ASCII）",
    "且": "逻辑与",
    "或": "逻辑或",
}

类型说明 = {
    "整数": "64 位有符号整数（int64_t）",
    "浮点": "64 位双精度浮点（double）",
    "文本": "C 字符串（char*），拼接用 连接()，长度用 文本长度()，比较用 文本相同()",
    "逻辑": "布尔值，取值为 真 / 假",
    "字节": "8 位无符号整数（uint8）",
    "无符号": "64 位无符号整数（uint64）",
    "指针": "void* 裸指针，用 读字节 / 写字 等内置按偏移访问",
}

# 编译器不可用时的兜底关键表（保证补全不空）
兜底关键字 = ["定义", "设", "输出", "输入", "如果", "则", "否则如果", "否则", "当", "循环",
              "从", "到", "步", "结束", "函数", "返回", "外部", "且", "或"]
兜底类型 = ["整数", "浮点", "文本", "逻辑", "字节", "无符号", "指针"]


def 手册行(名):
    """从内置函数手册里抓出某个函数的签名行。"""
    z = 取模块()
    if not z:
        return ""
    try:
        手册 = z.api_manual()
    except Exception:
        return ""
    for 行 in 手册.splitlines():
        if 行.strip().startswith(名 + "("):
            return 行.strip()
    return ""


def 内置函数说明(名):
    z = 取模块()
    文档串 = ""
    try:
        条目 = z.BUILTIN_DOC.get(名) if z else None
        if isinstance(条目, str):
            文档串 = 条目
        elif isinstance(条目, (list, tuple)):
            文档串 = " ".join(str(x) for x in 条目)
    except Exception:
        pass
    签名 = 手册行(名)
    if not 签名 and not 文档串:
        return ""
    段 = []
    if 签名:
        段.append("```zhc\n" + 签名 + "\n```")
    if 文档串:
        段.append(文档串)
    return "\n\n".join(段)


# ---------------------------------------------------------------- 诊断

行号模式 = re.compile(r"第\s*(\d+)\s*行")


def _规范文本(文本):
    """剥掉 UTF-8 BOM。记事本保存的 .zc 常带 BOM，会让首行符号名与诊断位置整体偏移。"""
    return 文本[1:] if 文本[:1] == "\ufeff" else 文本


def 检查(src):
    z = 取模块()
    if not z:
        return []
    try:
        z.Mxh_K0_Compiler(z.Mxh_K1_Lexer(src).run()).compile()
        return []
    except z.Mxh_K4_编译错误 as e:
        消息 = str(e)
        # 结构化字段为唯一真源：原值原样透传到 data（门禁与客户端据此取用）；
        # range 只是「展示位置」，按 LSP 规范裁切到行内，不得反向改变诊断语义。
        原码 = getattr(e, "码", None)
        原行 = getattr(e, "行", None) or None
        原列 = getattr(e, "列", None) or None
        行 = 原行
        if not 行:
            m = 行号模式.search(消息)
            行 = max(1, int(m.group(1))) if m else 1
        各行 = src.splitlines()
        行 = min(max(1, int(行)), max(1, len(各行)))
        正文 = 各行[行 - 1] if 各行 else ""
        列 = int(原列) if 原列 else 1
        列 = min(max(1, 列), max(1, len(正文)))
        诊断 = {
            "range": {
                "start": {"line": 行 - 1, "character": 列 - 1},
                "end": {"line": 行 - 1, "character": max(列, len(正文))},
            },
            "severity": 1,
            "source": "zhc",
            "message": 消息,
            "data": {
                "码": 原码,
                "行": 原行,
                "列": 原列,
                "期望": getattr(e, "期望", None),
                "实际": getattr(e, "实际", None),
                "类别": getattr(e, "类别", None),
                "裁切": (原行 is not None and int(原行) != 行) or (原列 is not None and int(原列) != 列),
            },
        }
        if 原码:
            诊断["code"] = 原码
        return [诊断]
    except Exception as e:  # 编译器内部异常也要报给用户，而不是静默
        return [{
            "range": {"start": {"line": 0, "character": 0}, "end": {"line": 0, "character": 1}},
            "severity": 1,
            "source": "zhc",
            "message": f"内部错误：{type(e).__name__}: {e}",
            "data": {"码": None, "行": None, "列": None, "期望": None, "实际": None, "类别": "内部", "裁切": False},
        }]


def 发布诊断(uri, 发送):
    文本 = 文档.get(uri, "")
    发送({"jsonrpc": "2.0", "method": "textDocument/publishDiagnostics",
          "params": {"uri": uri, "diagnostics": 检查(文本)}})


# ---------------------------------------------------------------- 补全 / 悬停 / 符号

定义名模式 = re.compile(r"^\s*(?:定义|设)\s+([^\s，,。]+)")
函数名模式 = re.compile(r"^\s*函数\s+([^\s（(]+)")


def 文档内变量(文本):
    名 = []
    for 行 in 文本.splitlines():
        m = 定义名模式.match(行)
        if m and m.group(1) not in 名:
            名.append(m.group(1))
    return 名


def 补全项():
    z = 取模块()
    关键字 = list(z.KEYWORDS) if z else 兜底关键字
    类型词 = list(z.TYPE_KW) if z else 兜底类型
    内置 = list(z.BUILTINS) if z else []

    项 = []
    for k in 关键字:
        if k in ("则", "从", "到", "步"):
            continue
        项.append({
            "label": k,
            "kind": 14,
            "detail": "关键字",
            "documentation": 关键字说明.get(k, ""),
        })
    for t in 类型词:
        项.append({
            "label": t,
            "kind": 25,
            "detail": "类型",
            "documentation": 类型说明.get(t, ""),
        })
    for f in 内置:
        项.append({
            "label": f,
            "kind": 3,
            "detail": 手册行(f) or "内置函数",
            "insertText": f + "(",
            "documentation": 内置函数说明(f),
        })
    for 常量, 说明 in (("真", "逻辑真"), ("假", "逻辑假"), ("空", "空指针")):
        项.append({"label": 常量, "kind": 12, "detail": 说明})
    return 项


不是词 = set(" \t\r\n（）()，,。=＝<>＜＞+-*/%\"'「」【】[]{}:：；;")


def 取词(文本, 行, 字符):
    行s = 文本.splitlines()
    if 行 >= len(行s):
        return ""
    t = 行s[行]
    起 = 字符
    while 起 > 0 and 起 <= len(t) and t[起 - 1] not in 不是词:
        起 -= 1
    止 = 字符
    while 止 < len(t) and t[止] not in 不是词:
        止 += 1
    return t[起:止]


def 符号(文本):
    出 = []
    for i, 行 in enumerate(文本.splitlines()):
        m = 函数名模式.match(行)
        if m:
            出.append({
                "name": m.group(1), "kind": 12,
                "range": {"start": {"line": i, "character": 0}, "end": {"line": i, "character": len(行)}},
                "selectionRange": {"start": {"line": i, "character": 0},
                                   "end": {"line": i, "character": len(行)}},
            })
            continue
        m = 定义名模式.match(行)
        if m:
            c = 行.find(m.group(1))
            出.append({
                "name": m.group(1), "kind": 13,
                "range": {"start": {"line": i, "character": 0}, "end": {"line": i, "character": len(行)}},
                "selectionRange": {"start": {"line": i, "character": c},
                                   "end": {"line": i, "character": c + len(m.group(1))}},
            })
    return 出


# ---------------------------------------------------------------- 协议层

def 读包(流):
    长度 = 0
    while True:
        行 = 流.readline()
        if not 行:
            return None
        if 行 in (b"\r\n", b"\n"):
            break
        if 行.lower().startswith(b"content-length:"):
            长度 = int(行.split(b":")[1].strip())
    体 = 流.read(长度)
    if not 体:
        return None
    return json.loads(体.decode("utf-8"))


def 写包(流, 对象):
    体 = json.dumps(对象, ensure_ascii=False).encode("utf-8")
    流.write(b"Content-Length: %d\r\n\r\n" % len(体))
    流.write(体)
    流.flush()


def 服务(输入流=None, 输出流=None):
    输入流 = 输入流 or sys.stdin.buffer
    输出流 = 输出流 or sys.stdout.buffer

    def 发送(对象):
        写包(输出流, 对象)

    def 提示(级, 内容):
        发送({"jsonrpc": "2.0", "method": "window/logMessage",
              "params": {"type": 级, "message": 内容}})

    while True:
        请求 = 读包(输入流)
        if 请求 is None:
            return 0
        方法 = 请求.get("method", "")
        rid = 请求.get("id")
        params = 请求.get("params") or {}

        if 方法 == "initialize":
            选项 = params.get("initializationOptions") or {}
            指定 = 选项.get("zhcPath") or 选项.get("zhcHome") or ""
            if 指定:
                加载编译器(指定)
            模块 = 取模块()
            发送({"jsonrpc": "2.0", "id": rid, "result": {
                "capabilities": {
                    "textDocumentSync": 1,
                    "completionProvider": {"triggerCharacters": [" ", "（", "(", "为"], "resolveProvider": False},
                    "hoverProvider": True,
                    "documentSymbolProvider": True,
                },
                "serverInfo": {"name": "zhc-lsp", "version": "0.2.7"},
            }})
            if 模块:
                提示(3, f"zhc 语言服务已就绪，编译器：{ZHC_DIR}")
            else:
                提示(2, "未找到 zhc.py，诊断暂不可用。请在工作区放置 zhc/zhc.py，或设置 zhc.compilerPath / 环境变量 ZHC_HOME。")
        elif 方法 == "initialized":
            pass
        elif 方法 == "shutdown":
            发送({"jsonrpc": "2.0", "id": rid, "result": None})
        elif 方法 == "exit":
            return 0
        elif 方法 == "textDocument/didOpen":
            文档项 = params.get("textDocument", {})
            uri = 文档项.get("uri", "")
            文档[uri] = _规范文本(文档项.get("text", ""))
            发布诊断(uri, 发送)
        elif 方法 == "textDocument/didChange":
            文档项 = params.get("textDocument", {})
            uri = 文档项.get("uri", "")
            变更 = params.get("contentChanges") or []
            if 变更:
                文档[uri] = _规范文本(变更[-1].get("text", 文档.get(uri, "")))
            发布诊断(uri, 发送)
        elif 方法 == "textDocument/didSave":
            uri = (params.get("textDocument") or {}).get("uri", "")
            if uri in 文档:
                发布诊断(uri, 发送)
        elif 方法 == "textDocument/didClose":
            uri = (params.get("textDocument") or {}).get("uri", "")
            文档.pop(uri, None)
            发送({"jsonrpc": "2.0", "method": "textDocument/publishDiagnostics",
                  "params": {"uri": uri, "diagnostics": []}})
        elif 方法 == "textDocument/completion":
            uri = (params.get("textDocument") or {}).get("uri", "")
            项 = 补全项()
            for 名 in 文档内变量(文档.get(uri, "")):
                项.append({"label": 名, "kind": 6, "detail": "本文档已定义的变量"})
            发送({"jsonrpc": "2.0", "id": rid, "result": {"isIncomplete": False, "items": 项}})
        elif 方法 == "textDocument/hover":
            uri = (params.get("textDocument") or {}).get("uri", "")
            位置 = params.get("position") or {}
            词 = 取词(文档.get(uri, ""), 位置.get("line", 0), 位置.get("character", 0))
            内容 = ""
            if 词 in 关键字说明:
                内容 = 关键字说明[词]
            elif 词 in 类型说明:
                内容 = 类型说明[词]
            elif 词:
                内容 = 内置函数说明(词) or 关键字说明.get(词, "")
            if 内容:
                发送({"jsonrpc": "2.0", "id": rid,
                      "result": {"contents": {"kind": "markdown", "value": 内容}}})
            else:
                发送({"jsonrpc": "2.0", "id": rid, "result": None})
        elif 方法 == "textDocument/documentSymbol":
            uri = (params.get("textDocument") or {}).get("uri", "")
            发送({"jsonrpc": "2.0", "id": rid, "result": 符号(文档.get(uri, ""))})
        elif rid is not None:
            发送({"jsonrpc": "2.0", "id": rid, "error": {"code": -32601, "message": f"未支持的方法：{方法}"}})


def main():
    懒 = 取模块()
    if "--自检" in sys.argv:
        if not 懒:
            print("未找到 zhc.py：请设置 ZHC_HOME 或把 zhc.py 放在 workspace 下")
            return 2
        print(f"zhc.py 目录：{ZHC_DIR}")
        print(f"关键字 {len(懒.KEYWORDS)} 个，内置函数 {len(懒.BUILTINS)} 个，类型 {len(懒.TYPE_KW)} 个")
        return 0
    try:
        return 服务()
    except KeyboardInterrupt:
        return 0


if __name__ == "__main__":
    sys.exit(main())
