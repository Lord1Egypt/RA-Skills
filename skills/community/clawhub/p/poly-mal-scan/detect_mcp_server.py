#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
detect_mcp_server.py —— 恶意代码检测「语言路由」MCP 服务(独立单文件, 零第三方依赖)。

放置位置: 三个语言检测工具目录之外(本文件与 php_security/ js_security/ bash_security/ 平级)。

职责: 智能推测某个文件/代码片段「使用了哪些语言」, 并据此决定该调用哪些语言的
检测工具(php_security/phpdect、js_security/jsdect、bash_security/bashdect)。

关键能力:
  - 可能「没有代码」(纯文本/空文件) → 不调用任何检测工具;
  - 可能「不止一种语言」(如 .html 内嵌 <?php ?> 与 <script>, 或 .sh 里藏 <?php) → 调用多个检测工具;
  - 对未知语言(python/sql/css/html 等)如实标注「无对应检测工具」, 不瞎调用。

MCP 传输: stdio, 行分隔的 JSON-RPC 2.0(无需 mcp SDK / tree_sitter)。
提供的工具:
  - detect_languages(file_path | content, filename?) : 仅识别语言, 返回判定依据, 不真正扫描;
  - scan(file_path | content, filename?)            : 识别语言 → 调用对应检测工具 → 合并结果;
  - list_detectors()                                : 列出本服务可调用的检测工具。

CLI 自测(非 MCP 模式):
  python detect_mcp_server.py --detect <文件>      # 打印语言识别结果
  python detect_mcp_server.py --scan   <文件>      # 打印识别+扫描合并结果
"""
import sys
import os
import io
import re
import json
import tempfile

BASE = os.path.dirname(os.path.abspath(__file__))

# 三种被支持的检测工具(文件夹 -> 主模块 -> scan_to_json 入口)
DETECTOR_FOLDERS = {
    "php":  ("php_security",  "phpdect",  "scan_to_json"),
    "js":   ("js_security",   "jsdect",   "scan_to_json"),
    "bash": ("bash_security", "bashdect", "scan_to_json"),
}
SUPPORTED = set(DETECTOR_FOLDERS)  # php / js / bash

# 扩展名 -> 推测语言
PHP_EXT  = {".php", ".php3", ".php4", ".php5", ".phtml", ".inc",
            ".phar", ".module", ".install", ".profile", ".test", ".php7"}
JS_EXT   = {".js", ".mjs", ".cjs", ".jsx", ".es", ".es6"}
TS_EXT   = {".ts", ".tsx"}                 # 归并到 js(node 家族)检测
BASH_EXT = {".sh", ".bash", ".zsh", ".ksh", ".bashrc", ".bash_profile",
            ".bash_login", ".profile", ".zshrc", ".kshrc", ".env"}
HTML_EXT = {".html", ".htm", ".vue", ".twig", ".tpl", ".ejs"}

# JS 内容特征(避免误判纯文本)
_JS_RE = re.compile(
    r'(?:function\s+\w+\s*\(|const\s+\w+\s*=|let\s+\w+\s*=|var\s+\w+\s*='
    r'|=>\s*\(|require\s*\(|module\.exports|document\.|window\.)'
)
# Bash 强/弱特征
_BASH_STRONG_RE = re.compile(
    r'(/dev/(tcp|udp)/|bash\s+-i\b|nc\s+-e\b|mkfifo\s+/tmp|exec\s+5<>\s*/dev/(tcp|udp))'
)
_BASH_WEAK_RE = re.compile(
    r'(?:^|\n)\s*(?:export\s+\w+|source\s+\S+|\balias\s+\w+=|\$\w+\s*\(\s*\)|'
    r'\bchmod\s+[uog]?\+\w|\buseradd\s+-u\s+0|\biptables\s+-F|\brm\s+-rf\s+/)'
)


# ======================================================================
# 1. 语言识别(多信号启发式)
# ======================================================================
def _read_bytes(path):
    with open(path, "rb") as f:
        return f.read()


def recognize(path=None, content=None, filename=None):
    """返回语言识别结果 dict。

    字段:
      检测到的语言     : 全部识别到的代码语言(含无检测工具的, 如 html/python)
      判定依据         : {语言: [理由...]}
      使用检测工具     : 有对应检测工具的子集(php/js/bash)
      无对应工具的代码语言 : 已识别但本服务无检测工具的语言
      no_code          : 是否判定为「无代码」
    """
    if path is not None and content is None:
        if not os.path.isfile(path):
            return {"错误": "文件不存在: %s" % path,
                    "检测到的语言": [], "使用检测工具": [], "no_code": True}
        raw = _read_bytes(path)
        name = os.path.basename(path)
    elif content is not None:
        raw = content.encode("utf-8", "replace") if isinstance(content, str) else content
        name = filename or ""
    else:
        return {"检测到的语言": [], "判定依据": {"_": ["无输入"]},
                "使用检测工具": [], "无对应工具的代码语言": [], "no_code": True}

    try:
        text = raw.decode("utf-8", "replace")
    except Exception:
        text = ""
    ext = os.path.splitext(name)[1].lower()

    langs = set()
    reasons = {}

    def add(lang, why):
        langs.add(lang)
        reasons.setdefault(lang, []).append(why)

    # ---- 信号1: 扩展名 ----
    if ext in PHP_EXT:
        add("php", "扩展名 %s 属 PHP" % ext)
    if ext in JS_EXT:
        add("js", "扩展名 %s 属 JS" % ext)
    if ext in TS_EXT:
        add("js", "扩展名 %s 属 TypeScript, 归并到 JS(node)检测" % ext)
    if ext in BASH_EXT:
        add("bash", "扩展名 %s 属 Shell" % ext)
    if ext in HTML_EXT:
        add("html", "扩展名 %s 属 HTML/模板, 走内容内嵌识别" % ext)

    # ---- 信号2: Shebang ----
    first_line = (text.split("\n", 1)[0] if text else "")
    if first_line.startswith("#!"):
        if "php" in first_line:
            add("php", "shebang 指明 php: %s" % first_line.strip())
        if "node" in first_line:
            add("js", "shebang 指明 node: %s" % first_line.strip())
        if re.search(r'\b(ba)?sh\b|/sh\b|zsh|ksh', first_line):
            add("bash", "shebang 指明 shell: %s" % first_line.strip())

    # ---- 信号3: 内容特征 ----
    if "<?php" in text or "<?=" in text:
        add("php", "内容含 PHP 开标签 <?php/<?=")
    if _JS_RE.search(text):
        add("js", "内容命中 JS 语法特征(function/const/require/module.exports/...)")
    if re.search(r'<\s*script[\s>]', text, re.I) and _JS_RE.search(text):
        add("js", "内容含 <script> 且内嵌 JS 语法(HTML 内嵌)")
    if _BASH_STRONG_RE.search(text):
        add("bash", "内容含强 Shell 特征(/dev/tcp、nc -e、mkfifo、exec 5<>/dev/tcp)")
    if _BASH_WEAK_RE.search(text):
        add("bash", "内容含 Shell 语法特征(export/source/alias/chmod u+s/...)")

    # 去重: html 仅作为「容器」记录, 真正驱动检测的是其内嵌的 php/js
    detected = sorted(langs)
    detectors = [l for l in detected if l in SUPPORTED]
    no_tool = [l for l in detected if l not in SUPPORTED]

    # 若扩展名是 html 但没识别到内嵌 php/js, 视为「无代码/纯静态」(不调用任何工具)
    if "html" in detected and not detectors:
        no_code = True
    else:
        no_code = (len(detectors) == 0)

    return {
        "文件或名称": name or "(内存内容)",
        "检测到的语言": detected,
        "判定依据": reasons,
        "使用检测工具": detectors,
        "无对应工具的代码语言": no_tool,
        "no_code": no_code,
    }


# ======================================================================
# 2. 调用对应检测工具(懒加载模块)
# ======================================================================
_MOD_CACHE = {}


def _load_detector(lang):
    if lang in _MOD_CACHE:
        return _MOD_CACHE[lang]
    folder, mod_name, fn_name = DETECTOR_FOLDERS[lang]
    fp = os.path.join(BASE, folder)
    if fp not in sys.path:
        sys.path.insert(0, fp)
    mod = __import__(mod_name)
    fn = getattr(mod, fn_name)
    _MOD_CACHE[lang] = (mod, fn)
    return _MOD_CACHE[lang]


def _run_detector(lang, target_path):
    _, fn = _load_detector(lang)
    return fn(target_path, True)  # recursive=True 收集静态包含


def _ext_for(lang):
    return {"php": ".php", "js": ".js", "bash": ".sh"}.get(lang, ".txt")


# ======================================================================
# 3. 工具实现
# ======================================================================
def tool_detect_languages(path=None, content=None, filename=None):
    return recognize(path=path, content=content, filename=filename)


def tool_scan(path=None, content=None, filename=None):
    # 统一成「待扫文件路径」
    tmp_path = None
    if path is not None:
        if not os.path.isfile(path):
            return {"错误": "文件不存在: %s" % path}
        target = path
    elif content is not None:
        rec0 = recognize(content=content, filename=filename)
        primary = next((l for l in ("php", "js", "bash") if l in rec0["使用检测工具"]), "txt")
        ext = _ext_for(primary) if primary in SUPPORTED else ".txt"
        fd, tmp_path = tempfile.mkstemp(suffix=ext)
        os.write(fd, content.encode("utf-8", "replace") if isinstance(content, str) else content)
        os.close(fd)
        target = tmp_path
    else:
        return {"错误": "必须提供 file_path 或 content"}

    try:
        rec = recognize(path=target, content=None, filename=filename)
        if rec.get("no_code"):
            return {
                "文件": target,
                "检测到的语言": rec["检测到的语言"],
                "使用检测工具": [],
                "no_code": True,
                "是否有威胁": False,
                "说明": "未检测到可检测代码语言(PHP/JS/Bash), 未运行任何检测工具。",
                "结果": {},
            }
        results = {}
        for lang in rec["使用检测工具"]:
            try:
                results[lang] = _run_detector(lang, target)
            except Exception as e:
                results[lang] = {"错误": "%s: %s" % (type(e).__name__, e)}
        # 汇总「是否有威胁」
        any_threat = False
        for langres in results.values():
            if isinstance(langres, list):
                for f in langres:
                    if isinstance(f, dict) and f.get("是否有威胁"):
                        any_threat = True
                        break
        rec.update({
            "文件": target,
            "是否有威胁": any_threat,
            "结果": results,
        })
        return rec
    finally:
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except Exception:
                pass


def tool_list_detectors():
    out = {}
    for lang, (folder, mod, fn) in DETECTOR_FOLDERS.items():
        out[lang] = {
            "目录": folder,
            "主模块": mod + ".py",
            "入口": "%s.%s()" % (mod, fn),
            "支持": True,
        }
    out["_说明"] = "本服务仅对 PHP / JS / Bash 三种语言提供检测工具; " \
                  "其余已识别语言(如 html/python/sql)会标注但不调用。"
    return out


# ======================================================================
# 4. MCP 协议层(stdio + 行分隔 JSON-RPC 2.0, 零依赖)
# ======================================================================
TOOLS = [
    {
        "name": "detect_languages",
        "description": "仅识别文件/代码片段使用了哪些语言, 返回判定依据与应调用的检测工具, "
                       "不真正扫描。支持「无代码」与「多语言」情形。",
        "inputSchema": {
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": "待识别的文件路径"},
                "content":   {"type": "string", "description": "直接传入的代码片段内容"},
                "filename":  {"type": "string", "description": "当用 content 传入时, 可提供文件名以辅助判断扩展名"},
            },
            "required": [],
        },
    },
    {
        "name": "scan",
        "description": "识别语言 → 智能调用对应语言检测工具(PHP/JS/Bash) → 合并返回结果。 "
                       "无代码则不调用任何工具; 多语言则调用多个工具。",
        "inputSchema": {
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": "待扫描的文件路径"},
                "content":   {"type": "string", "description": "直接传入的代码片段内容"},
                "filename":  {"type": "string", "description": "当用 content 传入时, 可提供文件名以辅助判断扩展名"},
            },
            "required": [],
        },
    },
    {
        "name": "list_detectors",
        "description": "列出本 MCP 服务可调用的检测工具(目录/模块/入口)。",
        "inputSchema": {"type": "object", "properties": {}, "required": []},
    },
]


def _dispatch(name, args):
    args = args or {}
    if name == "detect_languages":
        return tool_detect_languages(
            path=args.get("file_path"), content=args.get("content"), filename=args.get("filename"))
    if name == "scan":
        return tool_scan(
            path=args.get("file_path"), content=args.get("content"), filename=args.get("filename"))
    if name == "list_detectors":
        return tool_list_detectors()
    raise ValueError("未知工具: %s" % name)


def _send(obj):
    sys.stdout.write(json.dumps(obj, ensure_ascii=False) + "\n")
    sys.stdout.flush()


def _handle(msg):
    method = msg.get("method")
    mid = msg.get("id")

    if method == "initialize":
        _send({
            "jsonrpc": "2.0", "id": mid,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "detect-router-mcp", "version": "1.0.0"},
            },
        })
        return
    if method == "notifications/initialized":
        return
    if method == "tools/list":
        _send({"jsonrpc": "2.0", "id": mid, "result": {"tools": TOOLS}})
        return
    if method == "tools/call":
        name = (msg.get("params") or {}).get("name")
        args = (msg.get("params") or {}).get("arguments", {})
        try:
            result = _dispatch(name, args)
            _send({
                "jsonrpc": "2.0", "id": mid,
                "result": {
                    "content": [{"type": "text",
                                 "text": json.dumps(result, ensure_ascii=False, indent=2)}],
                    "isError": False,
                },
            })
        except Exception as e:
            _send({
                "jsonrpc": "2.0", "id": mid,
                "result": {
                    "content": [{"type": "text", "text": "错误: %s" % e}],
                    "isError": True,
                },
            })
        return
    # 未知请求(带 id) -> method not found
    if mid is not None:
        _send({"jsonrpc": "2.0", "id": mid,
               "error": {"code": -32601, "message": "Method not found: %s" % method}})


def _serve():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except Exception:
            continue
        if not isinstance(msg, dict):
            continue
        _handle(msg)


# ======================================================================
# 5. CLI 自测(非 MCP 模式)
# ======================================================================
def _cli():
    if len(sys.argv) < 3:
        print("用法:")
        print("  python detect_mcp_server.py --detect <文件>")
        print("  python detect_mcp_server.py --scan   <文件>")
        sys.exit(2)
    mode, target = sys.argv[1], sys.argv[2]
    if mode == "--detect":
        print(json.dumps(tool_detect_languages(path=target), ensure_ascii=False, indent=2))
    elif mode == "--scan":
        print(json.dumps(tool_scan(path=target), ensure_ascii=False, indent=2))
    else:
        print("未知模式: %s" % mode)
        sys.exit(2)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in ("--detect", "--scan"):
        _cli()
    else:
        # 默认进入 MCP stdio 服务模式
        _serve()
