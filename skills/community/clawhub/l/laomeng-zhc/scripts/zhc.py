#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
zhc —— 纯中文编程语言编译器（三目标：x86-64 原生可执行文件 / wasm32-wasip1 静态 .wasm /
       wasm32-unknown-unknown 零 import 纯计算模块）

设计原则：
1. 源码全中文：关键字、标识符、字面量、注释均为中文，不出现英文语法成分。
2. 64 位语义：整数统一 int64_t，浮点统一 double，指针 64 位。
3. 中文分词：采用"关键字最长匹配 + 余下归标识符"的贪心切分，无需依赖空格。
4. 后端：生成 C99 中间码，交由 MSVC(cl) 编译为 x64 原生 exe，借用其优化器。

用法：
    python zhc.py 源码.zc                 # 编译为同名 exe
    python zhc.py 源码.zc --run           # 编译并运行
    python zhc.py 源码.zc --emit-c        # 只输出中间 C 代码

版本：ZHC-LANG 2.0（语言契约 1.8）
著作：BY LAOMENG 网络工作室（孟祥辉）
声明：版权与制作信息统一由 --关于 输出，源码与注释不另行标注。
"""

import os
import re
import sys
import json
import bisect
import difflib
import subprocess
import argparse
import base64
import zlib
import shutil
import tempfile

# ---------------------------------------------------------------- 基础表

# 产品身份：全部对外声明集中在此，其余位置不重复标注
ZHC_产品名 = "zhc 纯中文编程语言编译器"
ZHC_版本 = "2.0"
ZHC_契约版 = "1.8"
ZHC_著作权 = "BY LAOMENG 网络工作室（孟祥辉）"
ZHC_联系 = "mxh6789@live.cn"

# 外部构建进程的硬超时：cl/clang 遇到异常模板可能无限挂起，无超时会让整个编译永久卡死
ZHC_构建限时 = 600

ZHC_关于 = """{名}
版本      ZHC-LANG {v}（语言契约 {c}）
构建目标  x86-64 原生 PE32+ / wasm32-wasip1 静态模块 / wasm32-unknown-unknown 零 import 模块
著作权    {权}
联系方式  {邮}

实现说明
  词法、语法、语义检查、容器运行库、平台垫片与构建编排均为本工作室自行编写，
  以单文件 Python 实现，不依赖第三方 Python 包；后端借用 MSVC 与 wasi-sdk 的 C 编译器。

制作说明
  部分测试样本、门禁清单与文档初稿借助 AI 工具起草，随后逐条人工核校并纳入门禁复跑，
  通过后才计入契约签证。此处为唯一说明位置，源码、注释与分发件不再逐处标注。
""".format(名=ZHC_产品名, v=ZHC_版本, c=ZHC_契约版, 权=ZHC_著作权, 邮=ZHC_联系)


def Mxh_R3_c_str(s):
    """把 Python 字符串转成 C 字面量。cl 用 /utf-8 编译，源码里的中文按 UTF-8 字节进 .rdata，
    与运行时全部走 UTF-8 的约定一致。"""
    out = ['"']
    for ch in s:
        if ch == "\\":
            out.append("\\\\")
        elif ch == '"':
            out.append('\\"')
        elif ch == "\n":
            out.append("\\n")
        elif ch == "\r":
            out.append("\\r")
        elif ch == "\t":
            out.append("\\t")
        else:
            out.append(ch)
    out.append('"')
    return "".join(out)


def _桥目录():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "桥")

# 全角符号 -> 半角符号（仅符号，不触碰汉字）
FULL2HALF = {
    "（": "(", "）": ")", "，": ",", "：": ":", "；": ";",
    "“": '"', "”": '"', "‘": "'", "’": "'",
    "＋": "+", "－": "-", "＊": "*", "／": "/", "％": "%",
    "＜": "<", "＞": ">", "＝": "=", "！": "!",
    "　": " ",
}

# 关键字（长词优先由排序保证）
KEYWORDS = [
    "否则如果", "否则", "如果", "则", "结束",
    "当", "循环", "从", "到", "步",
    "定义", "设", "为", "输出", "输入",
    "函数", "返回", "接受",
    "且", "或", "非", "真", "假",
    "整数", "浮点", "文本", "逻辑", "空",
    # ---- 系统级扩展（P0）
    "外部", "位异或", "位与", "位或", "左移", "右移", "取反",
    "字节", "无符号", "指针",
    # ---- 容器级扩展（P4）：类型词 3 + 语句 1
    # 「记作」不用单字「记」：单字关键字会把任何含「记」的既有标识符截断（如 记数），
    # 破坏存量程序；两字「记作」冲突面可忽略。变更见《第4级_OFFICE-WEB契约草案_1.1》。
    "表", "记录", "列表", "遍历", "记作",
    # 「任意值」是运行期才定类型的表达式结果类型（取元素／解JSON），显式写出来便于阅读
    "任意值",
]
# P4 新增词（类型词 3 + 语句 2 + 任意值）：只允许在词段开头被识别。
# 理由见 lex_word 的"左侧黏连"判断——「字符串长度」「值_列表」这类既有标识符
# 不能因为尾部撞上新词就被切开；存量词一律保持原来的可黏连行为，保证零漂移。
P4_NEW_WORDS = frozenset([
    "表", "记录", "列表", "遍历", "记作", "任意值",
    # P4 新增内置函数名同样受保护：「字符串长度」「文件追加」「内容新建」之类不得被切开
    "新建", "长度", "取元素", "置元素", "追加", "造列",
    "转JSON", "解JSON", "桥可用", "桥调用",
])

KEYWORDS_SORTED = sorted(KEYWORDS, key=len, reverse=True)
KW_SET = set(KEYWORDS)

TYPE_KW = {
    "整数": "int", "浮点": "double", "文本": "str", "逻辑": "bool",
    # 系统级标量
    "字节": "u8", "无符号": "u64", "指针": "ptr",
    # 容器（P4）：三种容器共用一套运行期动态值，静态类型只为编译期把关
    "表": "table", "记录": "record", "列表": "list",
    "任意值": "any",
}
C_TYPE = {
    "int": "int64_t", "double": "double", "str": "const char*", "bool": "int",
    "u8": "uint8_t", "u64": "uint64_t", "ptr": "void*",
    "table": "zhc_val*", "record": "zhc_val*", "list": "zhc_val*",
    # 任意值：取／解JSON 这类「类型要到运行期才知道」的表达式用它，与容器同一表示
    "any": "zhc_val*",
}
# 类型码 -> 中文名：错误文案与 JSON 列类型标签共用同一张表，避免两处漂移
TYPE_CN = {
    "int": "整数", "double": "浮点", "str": "文本", "bool": "逻辑",
    "u8": "字节", "u64": "无符号", "ptr": "指针",
    "table": "表", "record": "记录", "list": "列表",
    "any": "任意值",
}
# 中文类型名 -> 类型码：造列 的类型词、解JSON 的列类型标签都走这张表
TYPE_CN2 = {v: k for k, v in TYPE_CN.items()}
CONTAINER_TYPES = ("table", "record", "list")

# 运算符（按长度优先匹配）
OPERATORS = ["<=", ">=", "==", "!=", "+", "-", "*", "/", "%", "(", ")", ",", ":", "<", ">", "="]


def Mxh_K1_is_word_char(ch):
    """可作为中文标识符成分的字符：汉字、字母、数字、下划线。"""
    if ch == "_":
        return True
    if ch.isdigit():
        return True
    if ch.isalpha():
        return True
    code = ord(ch)
    # CJK 基本区 / 扩展A / 兼容区
    return (0x4E00 <= code <= 0x9FFF) or (0x3400 <= code <= 0x4DBF) or (0xF900 <= code <= 0xFAFF)


class Mxh_K1_Token:
    """词法单元。line 为 1 基行号，col 为 1 基列号（按 Unicode 码点计，制表符算 1 列）。"""

    __slots__ = ("kind", "val", "line", "col")

    def __init__(self, kind, val, line, col=0):
        self.kind = kind
        self.val = val
        self.line = line
        self.col = col

    def __repr__(self):
        return f"Token({self.kind},{self.val!r},L{self.line}C{self.col})"


# 错误码位与行号：从既有消息措辞中解析，保证 40 处 raise 的文案一字不改
Mxh_K4_码模式 = re.compile(r"\[(E\d{3})\]")
Mxh_K4_行模式 = re.compile(r"第\s*(\d+)\s*行")

# 最近一次被定位到源码的记号。深层函数（如 cast）拿不到 token，用它兜底取行/列。
Mxh_K4_定位锚 = None

# 当前正在解析的语句起始记号。语义/类型类错误往往不带自己的 token，用它兜底定位到语句。
Mxh_K4_语句锚 = None


def Mxh_K4_锚():
    return Mxh_K4_定位锚


def Mxh_K4_定位():
    """隐式转换等没有自带记号的错误用它取位置：优先当前语句起始，退到最近读取的记号。"""
    return Mxh_K4_语句锚 if Mxh_K4_语句锚 is not None else Mxh_K4_定位锚


def Mxh_K4_列(line=0):
    """只有行号、没有自带记号的错误用它补列：锚正好落在该行就取锚的列，否则 0（未知）。"""
    a = Mxh_K4_定位()
    if a is None:
        return 0
    if not line or a.line == line:
        return a.col
    return 0


class Mxh_K4_编译错误(Exception):
    """编译期错误：既保留人类可读措辞（__str__ 与改造前完全一致），又携带结构化定位字段。

      码   错误码（E204 等）；无法解析时为 None
      行   1 基行号；0 表示不适用（构建期错误）
      列   1 基列号；0 表示不适用
      期望 期望出现的记号/类型，仅部分错误提供
      实际 实际出现的记号/类型，仅部分错误提供
      类别 源码（词法/语法/语义）或 构建（工具链环境）
    """

    def __init__(self, 消息="", *, 码=None, 行=None, 列=None, 期望=None, 实际=None, 类别="源码"):
        self.消息 = 消息
        if 码 is None:
            m = Mxh_K4_码模式.search(消息)
            码 = m.group(1) if m else None
        self.码 = 码
        if 行 is None:
            m = Mxh_K4_行模式.search(消息)
            if m:
                行 = int(m.group(1))
            else:
                # 消息里没写行号（内部校验类错误）：退到当前语句起始记号，保证至少给出语句行
                b = Mxh_K4_语句锚
                if b is not None:
                    行 = b.line
                    if 列 is None:
                        列 = b.col
        self.行 = 行
        if 列 is None and 行 is not None:
            a = Mxh_K4_定位锚
            if a is not None and a.line == 行:
                列 = a.col
            else:
                b = Mxh_K4_语句锚
                if b is not None and b.line == 行:
                    列 = b.col
        self.列 = 列
        self.期望 = 期望
        self.实际 = 实际
        self.类别 = 类别
        super().__init__(消息)

    def __str__(self):
        return self.消息

    def 定位(self):
        """(行, 列)，缺省以 0 兜底，便于下游直接使用。"""
        return (self.行 or 0, self.列 or 0)

    def 转字典(self):
        return {
            "码": self.码,
            "行": self.行,
            "列": self.列,
            "期望": self.期望,
            "实际": self.实际,
            "类别": self.类别,
            "消息": self.消息,
        }


# ---------------------------------------------------------------- 词法分析

class Mxh_K1_Lexer:
    def __init__(self, src):
        # 兼容 Windows 记事本等工具写出的 UTF-8 BOM，否则首字符会被判成非法字符
        if src[:1] == "\ufeff":
            src = src[1:]
        # 保留原文：字符串字面量内部的中文全角标点必须原样保留
        self.raw = src
        self.src = "".join(FULL2HALF.get(c, c) for c in src)
        self.i = 0
        self.n = len(self.src)
        self.line = 1
        self.tokens = []
        # 每一行的起始偏移（0 基），用于把偏移量换算成 1 基列号
        self._行首 = [0]
        for _k, _ch in enumerate(self.src):
            if _ch == "\n":
                self._行首.append(_k + 1)

    def _列(self, pos):
        """把 0 基字符偏移换算成 1 基列号。"""
        if pos < 0:
            pos = 0
        row = bisect.bisect_right(self._行首, pos)
        return pos - self._行首[row - 1] + 1

    def _行号(self, pos):
        """把 0 基字符偏移换算成 1 基行号（不受扫描过程中行计数状态影响）。"""
        if pos < 0:
            pos = 0
        return bisect.bisect_right(self._行首, pos)

    def emit(self, kind, val, start=None):
        """start 为该记号首个字符的 0 基偏移；缺省取当前读取位置。"""
        pos = self.i if start is None else start
        self.tokens.append(Mxh_K1_Token(kind, val, self.line, self._列(pos)))

    def run(self):
        s, n = self.src, self.n
        while self.i < n:
            c = s[self.i]
            if c in " \t\r":
                self.i += 1
                continue
            if c == "\n":
                self.line += 1
                self.i += 1
                continue
            if c == "#":                      # 注释到行尾
                while self.i < n and s[self.i] != "\n":
                    self.i += 1
                continue
            if c == ";":                      # 可选语句分隔符，忽略
                self.i += 1
                continue
            if c == '"':
                self.lex_string()
                continue
            if c.isdigit():
                self.lex_number()
                continue
            if c == "「":                      # 标识符强制转义
                self.lex_quoted_ident()
                continue
            if Mxh_K1_is_word_char(c):
                self.lex_word()
                continue
            self.lex_operator()
        self.emit("EOF", "<文件结束>")
        return self.tokens

    def lex_string(self):
        start = self.i
        self.i += 1
        buf = []
        s, n, raw = self.raw, self.n, self.raw
        while self.i < n:
            c = s[self.i]
            if c == '"':
                self.i += 1
                self.emit("STR", "".join(buf), start)
                return
            if c == "\\" and self.i + 1 < n:
                nxt = s[self.i + 1]
                mapping = {"n": "\n", "t": "\t", "\\": "\\", '"': '"'}
                buf.append(mapping.get(nxt, nxt))
                self.i += 2
                continue
            if c == "\n":
                self.line += 1
            buf.append(raw[self.i])   # 原样保留全角标点与中文
            self.i += 1
        raise Mxh_K4_编译错误(
            f"第 {self._行号(start)} 行：[E002] 字符串未闭合：缺少结尾的半角双引号 \"，字符串不能跨行",
            码="E002", 行=self._行号(start), 列=self._列(start))

    def lex_number(self):
        s, n = self.src, self.n
        start = self.i
        while self.i < n and s[self.i].isdigit():
            self.i += 1
        is_float = False
        if self.i + 1 < n and s[self.i] == "." and s[self.i + 1].isdigit():
            is_float = True
            self.i += 1
            while self.i < n and s[self.i].isdigit():
                self.i += 1
        text = s[start:self.i]
        self.emit("FLT" if is_float else "INT", text, start)

    def lex_quoted_ident(self):
        s, n = self.src, self.n
        start = self.i
        self.i += 1
        bstart = self.i
        while self.i < n and s[self.i] != "」":
            self.i += 1
        if self.i >= n:
            raise Mxh_K4_编译错误(
                f"第 {self.line} 行：[E003] 「」标识符未闭合：缺少结尾的「」，标识符不能跨行",
                码="E003", 行=self.line, 列=self._列(start))
        self.emit("ID", s[bstart:self.i], start)
        self.i += 1

    def lex_word(self):
        """核心：中文无空格分词——关键字最长匹配，余下累积为标识符。"""
        s, n = self.src, self.n
        buf = []
        buf_start = None
        while self.i < n and Mxh_K1_is_word_char(s[self.i]):
            matched = None
            for kw in KEYWORDS_SORTED:
                if s.startswith(kw, self.i):
                    # 词边界检查：关键字后面若还黏着标识符字符，说明这是更长的标识符，
                    # 不能按关键字切分。例：「当前」≠「当」+「前」，「文本A」≠「文本」+「A」。
                    j = self.i + len(kw)
                    if j < n and Mxh_K1_is_word_char(s[j]):
                        break
                    # 左侧黏连：P4 新增词（表/记录/列表/遍历/记作/任意值/长度/取元素…）
                    # 若前面紧贴标识符字符，说明它是更长标识符的尾巴，不能切。
                    # 例：「字符串长度」「值_列表」「数据表」都必须是单个标识符。
                    # 存量词不做此检查——它们从 P0/P1 起就允许无空格连写（如「真则」）。
                    if kw in P4_NEW_WORDS and self.i > 0 and Mxh_K1_is_word_char(s[self.i - 1]):
                        break
                    matched = kw
                    break
            if matched:
                if buf:
                    self.emit("ID", "".join(buf), buf_start)
                    buf = []
                    buf_start = None
                self.emit("KW", matched, self.i)
                self.i += len(matched)
            else:
                if buf_start is None:
                    buf_start = self.i
                buf.append(s[self.i])
                self.i += 1
        if buf:
            self.emit("ID", "".join(buf), buf_start)

    def lex_operator(self):
        s = self.src
        for op in OPERATORS:
            if s.startswith(op, self.i):
                self.emit("OP", op, self.i)
                self.i += len(op)
                return
        ch = self.src[self.i]
        if ch in ".。·":
            raise Mxh_K4_编译错误(
                f"第 {self.line} 行：[E013] 标识符中不允许出现「{ch}」："
                f"文件名、路径和普通文本必须用半角双引号包起来，"
                f"例如 读文件(\"数据.txt\")",
                码="E013", 行=self.line, 列=self._列(self.i))
        raise Mxh_K4_编译错误(
            f"第 {self.line} 行：[E004] 无法识别的字符 {ch!r}："
            f"该字符不属于本语言词法单元（中文、字母、数字、半角运算符、半角引号与本语言标点之外一律不识别）",
            码="E004", 行=self.line, 列=self._列(self.i))


# ---------------------------------------------------------------- 系统内置函数
# 由编译器直接展开为 Win32 / CRT 调用。设计原则：内存类内置一律按【字节偏移】寻址，
# 避免"字 / 字节"两套索引带来的歧义。

def _as_ptr(args, i):
    code, typ = args[i]
    if typ == "ptr":
        return code
    if typ == "str":
        return f"((void*)({code}))"
    return f"((void*)(intptr_t)({code}))"


def _as_i64(args, i):
    code, typ = args[i]
    if typ == "ptr":
        return f"((int64_t)(intptr_t)({code}))"
    return f"((int64_t)({code}))"


def _bi_tick(args):
    return "(int64_t)GetTickCount64()", "int"


def _bi_pid(args):
    return "(int64_t)(uint32_t)GetCurrentProcessId()", "int"


def _bi_sleep(args):
    return f"Sleep((DWORD)({_as_i64(args, 0)}))", "void"


def _bi_alloc(args):
    return ("VirtualAlloc(NULL,(SIZE_T)(%s),MEM_COMMIT|MEM_RESERVE,PAGE_READWRITE)"
            % _as_i64(args, 0)), "ptr"


def _bi_free(args):
    return f"VirtualFree({_as_ptr(args, 0)},0,MEM_RELEASE)", "int"


def _bi_read_byte(args):
    return ("((int64_t)((uint8_t*)%s)[(size_t)(%s)])"
            % (_as_ptr(args, 0), _as_i64(args, 1))), "int"


def _bi_write_byte(args):
    return ("(((uint8_t*)%s)[(size_t)(%s)]=(uint8_t)(%s))"
            % (_as_ptr(args, 0), _as_i64(args, 1), _as_i64(args, 2))), "void"


def _bi_read_word(args):
    return ("((int64_t)*(uint16_t*)((uint8_t*)%s+(size_t)(%s)))"
            % (_as_ptr(args, 0), _as_i64(args, 1))), "int"


def _bi_write_word(args):
    return ("(*(uint16_t*)((uint8_t*)%s+(size_t)(%s))=(uint16_t)(%s))"
            % (_as_ptr(args, 0), _as_i64(args, 1), _as_i64(args, 2))), "void"


def _bi_read_dword(args):
    return ("((int64_t)*(uint32_t*)((uint8_t*)%s+(size_t)(%s)))"
            % (_as_ptr(args, 0), _as_i64(args, 1))), "int"


def _bi_write_dword(args):
    return ("(*(uint32_t*)((uint8_t*)%s+(size_t)(%s))=(uint32_t)(%s))"
            % (_as_ptr(args, 0), _as_i64(args, 1), _as_i64(args, 2))), "void"


def _bi_read_qword(args):
    return ("((int64_t)*(uint64_t*)((uint8_t*)%s+(size_t)(%s)))"
            % (_as_ptr(args, 0), _as_i64(args, 1))), "int"


def _bi_msgbox(args):
    return ("zhc_msgbox((const char*)(%s),(const char*)(%s))"
            % (args[0][0], args[1][0])), "int"


def _bi_getenv(args):
    return f"zhc_getenv((const char*)({args[0][0]}))", "str"


def _bi_addr2str(args):
    return f"zhc_addr((uintptr_t)({_as_ptr(args, 0)}))", "str"


# ---- 控制台输入与文件 I/O（P0 标准库最小集） ----

def _bi_input(args):
    prompt = args[0][0] if args else '""'
    return f"zhc_input((const char*)({prompt}))", "str"


def _bi_read_file(args):
    return f"zhc_read_file((const char*)({args[0][0]}))", "str"


def _text_arg(args, idx):
    """取第 idx 个参数为 C 文本指针；数值/逻辑自动走环形缓冲转文本，省掉手工 转文本 嵌套，也不会泄漏。"""
    code, typ = args[idx][0], args[idx][1]
    if typ == "str":
        return f"(const char*)({code})"
    if typ in ("bool", "logic"):
        return f"zhc_tmp_b((int)({code}))"
    if typ == "double":
        return f"zhc_tmp_d({code})"
    return f"zhc_tmp_i((int64_t)({code}))"


def _bi_write_file(args):
    return ("zhc_write_file((const char*)(%s),(const char*)(%s),0)"
            % (args[0][0], _text_arg(args, 1))), "int"


def _bi_append_file(args):
    return ("zhc_write_file((const char*)(%s),(const char*)(%s),1)"
            % (args[0][0], _text_arg(args, 1))), "int"


def _bi_write_line(args):
    return ("zhc_write_line((const char*)(%s),(const char*)(%s))"
            % (args[0][0], _text_arg(args, 1))), "int"


def _bi_file_size(args):
    return f"zhc_file_size((const char*)({args[0][0]}))", "int"


def _bi_file_exists(args):
    return f"zhc_file_exists((const char*)({args[0][0]}))", "bool"


def _bi_argc(args):
    return "zhc_argc_n", "int"


def _bi_arg(args):
    return f"zhc_arg(({_as_i64(args, 0)}))", "str"


def _bi_free_text(args):
    return f"zhc_free_text((const char*)({args[0][0]}))", "void"


# ---- 文本处理：拼接与转文本（结果均由 malloc 分配，须 释放文本） ----

def _bi_concat(args):
    return ("zhc_concat((const char*)(%s),(const char*)(%s))"
            % (args[0][0], args[1][0])), "str"


def _bi_tostr(args):
    code, typ = args[0][0], args[0][1]
    if typ == "str":
        return f"zhc_dup((const char*)({code}))", "str"
    if typ in ("bool", "logic"):
        return f"zhc_bool2str((int)({code}))", "str"
    if typ == "double":
        return f"zhc_num2str_d({code})", "str"
    return f"zhc_num2str((int64_t)({code}))", "str"


def _bi_len(args):
    return f"zhc_textlen((const char*)({args[0][0]}))", "int"


def _bi_eq(args):
    return ("zhc_text_eq((const char*)(%s),(const char*)(%s))"
            % (args[0][0], args[1][0])), "bool"


def _wrap(code, typ):
    """把任意类型的表达式包成运行期动态值 zhc_val*（容器本身已是该表示，直接透传）。"""
    if typ in CONTAINER_TYPES or typ == "any":
        return code
    if typ == "int":
        return f"zhc_mkint((int64_t)({code}))"
    if typ == "double":
        return f"zhc_mkflt((double)({code}))"
    if typ == "bool":
        return f"zhc_mkbool((int)({code}))"
    if typ == "str":
        return f"zhc_mkstr((const char*)({code}))"
    if typ in ("u8", "u64"):
        return f"zhc_mkint((int64_t)({code}))"
    if typ == "ptr":
        return f"zhc_mkint((int64_t)(uintptr_t)({code}))"
    return code


def _need_container(name, args, idx):
    """容器类内置函数的参数约定：容器／any 直接透传，标量自动包成动态值。

    类型不合（如把整数当表）不在编译期拦，交给运行期 zhc_* 报 E401／E402，
    这样与既有内置函数「不校验、只展开」的风格一致，也不会打断既有编译路径。"""
    return _wrap(args[idx][0], args[idx][1])


# ---- P4 容器内置函数生成器
def _bi_cnew(args):
    return f"zhc_newof((const char*)({_text_arg(args, 0)}))", "any"


def _bi_clen(args):
    return f"zhc_len({_wrap(args[0][0], args[0][1])})", "int"


def _bi_cget(args):
    return (f"zhc_get({_wrap(args[0][0], args[0][1])},"
            f"{_wrap(args[1][0], args[1][1])})"), "any"


def _bi_cset(args):
    return (f"zhc_set({_wrap(args[0][0], args[0][1])},{_wrap(args[1][0], args[1][1])},"
            f"{_wrap(args[2][0], args[2][1])})"), "int"


def _bi_cpush(args):
    return f"zhc_push({_wrap(args[0][0], args[0][1])},{_wrap(args[1][0], args[1][1])})", "int"


def _bi_addcol(args):
    return (f"zhc_addcol({_wrap(args[0][0], args[0][1])},"
            f"(const char*)({_text_arg(args, 1)}),(const char*)({_text_arg(args, 2)}))"), "int"


def _bi_tojson(args):
    return f"zhc_tojson({_wrap(args[0][0], args[0][1])})", "str"


def _bi_fromjson(args):
    return f"zhc_fromjson((const char*)({_text_arg(args, 0)}))", "any"


def _bi_bridge_ok(args):
    return "zhc_bridge_ok()", "bool"


def _bi_bridge_call(args):
    return (f"zhc_export_call((const char*)({_text_arg(args, 0)}),(const char*)({_text_arg(args, 1)}),"
            f"(const char*)({_text_arg(args, 2)}))"), "str"


# 名字 -> (最少参数, 最多参数, 生成器)
BUILTINS = {
    "系统节拍": (0, 0, _bi_tick),
    "进程编号": (0, 0, _bi_pid),
    "睡眠": (1, 1, _bi_sleep),
    "申请内存": (1, 1, _bi_alloc),
    "释放内存": (1, 1, _bi_free),
    "读字节": (2, 2, _bi_read_byte),
    "写字节": (3, 3, _bi_write_byte),
    "读字": (2, 2, _bi_read_word),
    "写字": (3, 3, _bi_write_word),
    "读双字": (2, 2, _bi_read_dword),
    "写双字": (3, 3, _bi_write_dword),
    "读四字": (2, 2, _bi_read_qword),
    "弹窗": (2, 2, _bi_msgbox),
    "取环境": (1, 1, _bi_getenv),
    "地址转文本": (1, 1, _bi_addr2str),
    "输入": (0, 1, _bi_input),
    "读文件": (1, 1, _bi_read_file),
    "写文件": (2, 2, _bi_write_file),
    "追加文件": (2, 2, _bi_append_file),
    "写行": (2, 2, _bi_write_line),
    "文件大小": (1, 1, _bi_file_size),
    "文件存在": (1, 1, _bi_file_exists),
    "参数个数": (0, 0, _bi_argc),
    "取参数": (1, 1, _bi_arg),
    "释放文本": (1, 1, _bi_free_text),
    "连接": (2, 2, _bi_concat),
    "转文本": (1, 1, _bi_tostr),
    "文本长度": (1, 1, _bi_len),
    "文本相同": (2, 2, _bi_eq),
    # ---- P4 容器（表／记录／列表）
    "新建": (1, 1, _bi_cnew),
    "长度": (1, 1, _bi_clen),
    "取元素": (2, 2, _bi_cget),
    "置元素": (3, 3, _bi_cset),
    "追加": (2, 2, _bi_cpush),
    "造列": (3, 3, _bi_addcol),
    "转JSON": (1, 1, _bi_tojson),
    "解JSON": (1, 1, _bi_fromjson),
    "桥可用": (0, 0, _bi_bridge_ok),
    "桥调用": (3, 3, _bi_bridge_call),
}

# wasm32-unknown-unknown 目标（零 WASI import、无文件系统）下不可用的内置函数。
# 依据：noos 垫片把 fopen/fwrite/stat/argv 全实现为桩，放行只会得到「返回 -1 / 空文本」
# 的静默失败，故在编译期按 E314 拒绝。清单与「文件 I/O」六件套严格一致。
_NOOS_禁用内置 = frozenset({
    "读文件", "写文件", "追加文件", "写行", "文件大小", "文件存在",
})


# 内置函数文档：名字 -> (签名, 说明)。供 --api 输出与自然语言智能体取用，保证文档与实现同源。
BUILTIN_DOC = {
    "系统节拍": ("系统节拍() -> 整数", "系统启动至今的毫秒数"),
    "进程编号": ("进程编号() -> 整数", "当前进程 ID"),
    "睡眠": ("睡眠(毫秒)", "让当前线程休眠指定毫秒"),
    "申请内存": ("申请内存(字节数) -> 指针", "向系统提交可读写内存页，失败返回 空"),
    "释放内存": ("释放内存(内存块) -> 整数", "释放由 申请内存 得到的内存"),
    "读字节": ("读字节(内存块, 偏移) -> 整数", "读 8 位无符号数"),
    "写字节": ("写字节(内存块, 偏移, 值)", "写 8 位无符号数"),
    "读字": ("读字(内存块, 偏移) -> 整数", "读 16 位无符号数"),
    "写字": ("写字(内存块, 偏移, 值)", "写 16 位无符号数"),
    "读双字": ("读双字(内存块, 偏移) -> 整数", "读 32 位无符号数"),
    "写双字": ("写双字(内存块, 偏移, 值)", "写 32 位无符号数"),
    "读四字": ("读四字(内存块, 偏移) -> 整数", "读 64 位无符号数"),
    "弹窗": ("弹窗(正文, 标题) -> 整数", "弹出系统消息框，返回按键值"),
    "取环境": ("取环境(变量名) -> 文本", "读取环境变量，不存在时返回空文本"),
    "地址转文本": ("地址转文本(内存块) -> 文本", "把地址格式化为 0x 开头的文本"),
    "输入": ("输入([提示]) -> 文本", "在控制台打印提示并读入一行（结果下次调用会被覆盖）"),
    "读文件": ("读文件(路径) -> 文本", "按 UTF-8 读取整个文件，失败返回空文本；用完须 释放文本"),
    "写文件": ("写文件(路径, 内容) -> 整数", "整体覆盖写入，返回字节数，失败返回 -1；内容可为文本或数值（自动转文本）"),
    "追加文件": ("追加文件(路径, 内容) -> 整数", "在文件末尾追加，返回字节数，失败返回 -1；内容可为文本或数值"),
    "写行": ("写行(路径, 内容) -> 整数", "在文件末尾追加一行（自动补换行符），返回字节数，失败返回 -1；逐行写文件首选"),
    "文件大小": ("文件大小(路径) -> 整数", "文件字节数，失败返回 -1"),
    "文件存在": ("文件存在(路径) -> 逻辑", "文件存在返回 真"),
    "参数个数": ("参数个数() -> 整数", "命令行参数个数，含程序名"),
    "取参数": ("取参数(序号) -> 文本", "取第 N 个命令行参数（自 0 起），越界返回空文本"),
    "释放文本": ("释放文本(文本)", "释放 读文件 / 连接 / 转文本 申请的内存，其他文本不可释放"),
    "连接": ("连接(文本A, 文本B) -> 文本", "拼接两段文本，结果须 释放文本"),
    "转文本": ("转文本(值) -> 文本", "整数/浮点/逻辑/文本 转文本，结果须 释放文本"),
    "文本长度": ("文本长度(文本) -> 整数", "按字符数（非字节数）返回长度，中文算 1 个"),
    "文本相同": ("文本相同(文本A, 文本B) -> 逻辑", "内容相同返回 真；文本不能用 == 直接比较"),
    # ---- P4 容器（表／记录／列表）
    "新建": ("新建(类型名) -> 容器", "类型名为 \"表\"／\"记录\"／\"列表\"（也可直接写 新建(表)），返回空容器"),
    "长度": ("长度(容器) -> 整数", "表的行数／记录的键数／列表的元素个数；文本返回字符数"),
    "取元素": ("取元素(容器, 键) -> 任意值", "表按行号取整行（与表共享同一行，写入即生效）、记录按键取值、列表按下标取值"),
    "置元素": ("置元素(容器, 键, 值) -> 整数", "表替换整行、记录写入键（无则新增）、列表改下标；成功 1，失败 0"),
    "追加": ("追加(容器, 值) -> 整数", "表追加一行（首行自动建列，或先 造列）、列表尾插；返回新长度，失败 -1"),
    "造列": ("造列(表, 列名, 类型词) -> 整数", "为表定义列，类型词如 \"整数\"；列名重复或表已有序数据时报 E403／E404"),
    "转JSON": ("转JSON(容器) -> 文本", "按 IR 契约序列化为单行 JSON，浮点保留 15 位有效数字"),
    "解JSON": ("解JSON(文本) -> 容器", "把 JSON 文本解成 表／记录／列表；含「列」「行」的自定义形状会还原成表，非法报 E405"),
    "桥可用": ("桥可用() -> 逻辑", "JSON 桥后端是否已就绪；真=常驻后端可用，假=未启动或启动失败（表 模块可自动降级为 CSV）"),
    "桥调用": ("桥调用(模块, 方法, 参数JSON) -> 文本", "调用后端渲染器；表.导出xlsx 在桥失败时自动降级为 CSV 并返回 {\"成功\":true,\"降级\":true,\"实际格式\":\"csv\"}；文档／页面 不降级，原样返回 {\"成功\":false,\"错误\":{\"码\":\"B001\"}}"),
}


# ==================== wasm32-unknown-unknown（noos）第三目标垫片 ====================
# 与 Mxh_R2_WASM_SHIM 同构的单文件自包含方案：两组文本 zlib 压缩后 base64 内联，
# 构建期解压到临时目录使用，运行期不依赖任何外部文件名。
#
# 该目标是「零 WASI import」目标：不接 wasi-libc（其头文件对非 WASI 目标 #error），
# 系统头由 zhc_noos.h 顶替，mini-libc 子集由 zhc_noos_impl.c 提供
# （8 MB bump 堆 + 1 MB 线性内存输出缓冲，无 fd_write，无文件系统）。
# 输出经导出符号交给宿主读取：main / memory / zhc_out_ptr / zhc_out_len /
# zhc_out_reset / zhc_out_cap。
#
# 可读原文：P1_zhc_noos.h(6540B) / P1_zhc_noos_impl.c(26588B) / P1_run_noos.js(1113B)。
# 改动此处任一文本，都必须重跑 8 例对拍（期望 6 PASS + 2 例已知差异）。
Mxh_R2_NOOS_H_B64 = (
    "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"
)

Mxh_R2_NOOS_IMPL_B64 = (
    "eNrVPWtzHNWV3/UrrpXCmh5p5BnZ2MZjmfKykFBFkVTtppZCuKZ6enqkRjM9o+4eSbbRFq+AvYBNCMHEDoTsQpJawJhUAsYI"
    "/F92PZL55L+w55z76Hu7b49mbGcBV8J038d5n3PPffTVgTI7s+I1wl4vbgTdfmfeY//z/Ntsw427Bxcqg3A17G2E8pftfvLJ"
    "revnhx9dGr7/8e75V3cvv8w6QdNjw6vv7164Nvz8xSlWZjuXPmD/dvJfHmcArxcld7Yv3/72N8NXbwxf+d3ujZs7z/95+Mqv"
    "hp++u7v9m+Erf72zfWXnnVdvff0Fe/zAz9mt688Pv31t+OHnt//20Z3tc7tXru588Ortl74Z/seV4ZdXh9sv3tl+ffftzwHA"
    "zgfXd7ffuf3Zr3d+/4ed197a/fq9O9vn//f5F1n5wNRPgtDrDFo+m5asza9MT00dKLPF7D/GSZO0nBtevXnr+tfDj369e+NP"
    "ANDSAeG3/HYQ+uzpnz3S+Pkv/7XxyMlfsFJtwI4fZwtVZypO3CTwmLfiRgz/LTd6g2RJa3yqLtsMwjhYDv0Wb9Po+CFbZNX6"
    "1JTXC+OEQHD9YG0/iUrrvaDlsLMs8pNBFPJudbY1pQDBP9keoFnbY0VRH8/tZ/tohGMvrGXin+wV+bGfqH4mL9BFcktdiZNB"
    "UtI5jOdSSYQAYgqBq5KgTu/tXsRKAYcZsOMMeAhmZ2Vr/Be0WSlFfmLRUFCF1QaO4KmuunDdqE6zs6cAQbwUnOJNtqYsjbDJ"
    "zDPVmfrUVoFRDT94BWypOej2mdvp9Dw36UVjWdPPHj35C25OR7PmpMRBdrXcWPHd/pLex2JVgkVs2hjEUMCNK9vM7cDv0ZJ6"
    "39S0X9pks+wISG4/+/cjA9ImqrHMusRZKQ7O+I3EorXQJ3wCtgLuhA4XLSqLtwGiHNn8aFqp0z3L608YQpLaZE/+8okneD9O"
    "Wh8A7RcS0qAInRpwFwkwrxDQ+qRXDskzmPTCZI6J5/iM5FhKAJBCA4h/8ZksMUJWOut9h3X9LrpNf45V55issxAR+by7gKdI"
    "UDLnFWt2RPvWLHJKKfD6p0trcwgVOkEN2POtm+8Nr56DsH3r+hvDFy4PL/xh+N6l4Yd/Hl67ePvmN7ev/zcE4Z3Xz++8c214"
    "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"
)

Mxh_R2_NOOS_RUN_JS_B64 = (
    "eNptU8tu00AU3ecrLis7wkygbKpUQQoLpCIeiwh1UaHIca6TUT3jMDMmDVUkpIoiIXZFKkJCKiu64SFWqE3pz+Aku/4Cd/xI"
    "QmFje86559zHXNdqMD06hq1maxPSrxe/f55dTj6kb47n5+cw9LW4vXYjkTsyHsryDdOTT+nHo8vJ2/n3/dm7ExA+l/b07Wx2"
    "ejF9+Tk9eJV+eT//dZi+Pp1NDtODH5UgltpAqKEBCp8lXKHrhNqpbhTMwDd94gYqDlBr5qve8+21pyXbSUIiQ80U+t17PMLW"
    "SAau1SwMRNylEIlD2MJOU2sUnWjEHsbdJEKX9ItALgaxMraQfwNZQbrkthDgboY94PT9X1ERkImY8AcuQuMOIJO+wGVamcmv"
    "FrhJsC8DtGIP9sYrWSnaikr7kpCIttNtx07d8ZwX/aAdJ6Y9MGrlFKHlBIpYjZzFHAXXmsteVgd2Wcgjg8rdseVeoxeXlLa6"
    "KIF8KHKvAuXM2kGcSFMvj4yS9EzfWwYsKTsGbn05E9mU4Do4zKEnz+diVUVn9dURW7wos73gC8CrjDcqPAS3OBcFQKPRgJvV"
    "vFJicZeVY1Co0VThKuJSjwARGlABtejImu9YxKgR7OUYSeyAKRLGEPgm6JNxtWQd01fxsA62IWSCVtbvIUWSR7HPRuUmK9eT"
    "Z815qvxvnoBVnm6u2JYnXJr1plL+yDaW3yijhQ5ReTaNZ70yJdlkNbezElVQYoU9YfQsQW26+f3ezaxYqGLhknuVmbhlFE3X"
    "dRITrttfdFwp/8tcxYaKG3Tvtx4/IsTG8nDkEuGBTKLIg1t2if4AONCNig=="
)


def Mxh_R2_noos_垫片():
    """Win32 面垫片剥掉全部系统 #include 后的版本，供 noos 目标使用。

    noos 目标不接 libc，垫片原带的 8 个头（stdio / stdlib / string / stdint /
    wchar / sys.stat / time / wasi.api）一个都不能引；它们声明的能力由
    zhc_noos.h + mini-libc 实现顶替。剥的只是 include 行，垫片正文一字不动，
    因此两个 wasm 目标共用同一份 Win32 面语义。
    """
    keep = []
    for line in Mxh_R2_WASM_SHIM.splitlines():
        s = line.strip()
        if s.startswith("#include <") and s.endswith(">"):
            continue
        keep.append(line)
    return "\n".join(keep)


Mxh_R2_NOOS_资产 = {
    "zhc_noos.h": Mxh_R2_NOOS_H_B64,
    "zhc_noos_impl.c": Mxh_R2_NOOS_IMPL_B64,
    "run_noos.js": Mxh_R2_NOOS_RUN_JS_B64,
}


def Mxh_R2_noos_text(名):
    """解出内联垫片原文（UTF-8）。名取 zhc_noos.h / zhc_noos_impl.c / run_noos.js。"""
    return zlib.decompress(base64.b64decode(Mxh_R2_NOOS_资产[名])).decode("utf-8")


def _pad(text, width):
    """按显示宽度补齐（中文字符占两列），保证手册纵向对齐。"""
    w = sum(2 if ord(ch) > 0x2E7F else 1 for ch in text)
    return text + " " * max(1, width - w)


def api_manual():
    """生成系统级类型与内置函数手册（纯文本）。"""
    lines = ["ZHC 类型："]
    lines.append("  整数 int64   浮点 double   文本 char*   逻辑 真/假")
    lines.append("  字节 uint8   无符号 uint64  指针 void*（空 = 空指针）")
    lines.append("  表   二维表：列名固定、行可变（列定义用 造列，行用 追加／置元素 写入）")
    lines.append("  记录 键值对集合，键为文本（用 置元素 写入，取元素 按键读取）")
    lines.append("  列表 有序异构集合（用 追加 尾插，取元素 按下标读取）")
    lines.append("  任意值 取元素／解JSON 这类要到运行期才知道类型的表达式的结果类型，可赋给任何标量或容器")
    lines.append("")
    lines.append("ZHC 系统级内置函数：")
    for name, (sig, desc) in BUILTIN_DOC.items():
        lines.append(f"  {_pad(sig, 32)}{desc}")
    lines.append("")
    lines.append("ZHC 运算符：")
    lines.append("  算术 + - * / %   比较 < > <= >= == !=")
    lines.append("  位运算 位与 位或 位异或 左移 右移 取反")
    lines.append("  逻辑 且 或 非")
    lines.append("")
    lines.append("ZHC 外部函数（直接声明 Win32 导出符号，名字必须是 ASCII）：")
    lines.append("  外部 函数 GetTickCount64() 返回 整数")
    return "\n".join(lines)


# 内置函数名也参与分词，避免被拆成普通标识符
for _bn in BUILTINS:
    if _bn not in KEYWORDS:
        KEYWORDS.append(_bn)

# 必须重建分词索引：否则「读字节」会被关键字「字节」截断成「读」+「字节」
KEYWORDS_SORTED = sorted(set(KEYWORDS), key=len, reverse=True)
KW_SET = set(KEYWORDS)


# 允许在实参位置直接写类型词的 (内置函数名, 参数下标)，下标 0 基。
# 只放"这个参数语义上就是要一个类型名"的位置，其余位置类型词一律按语法错误处理。
_TYPEWORD_ARG = frozenset([
    ("新建", 0),      # 新建(表) / 新建(记录) / 新建(列表)
    ("造列", 2),      # 造列(t, 姓名, 文本)
])


class Mxh_K2_FuncSig:
    def __init__(self, name, params, ret):
        self.name = name
        self.params = params      # [(名字, 类型)]
        self.ret = ret            # 类型 或 None
        self.cname = None
        self.extern = False       # 外部函数：cname 保持原名，不生成函数体
        self.line = 0             # 函数定义所在的 1 基行号（用于重名等错误定位）
        self.col = 0              # 函数定义所在的 1 基列号


# 运行库：内置函数展开时会用到，随中间码一并输出（static，未使用时由编译器丢弃）
# 两个 wasm 目标（wasm32-wasi / wasm32-unknown-unknown）内联进中间 C 的 Win32 面垫片
# （UTF-8<->UTF-32、无子进程桥）。noos 目标额外剥掉本垫片的系统 #include，见 Mxh_R2_noos_垫片()。
# x86-64 目标完全不引用本常量，保证既有构建链与产物零变化。
Mxh_R2_WASM_SHIM = r'''/* zhc wasm32-wasip1 垫片：把 ZHC 运行库用到的 Win32 面映射到 wasi-libc。
   由 zhc.py 在目标为 wasm32-wasi 时内联进中间 C，x86-64 目标不引用本文件。
   wasm32-unknown-unknown 目标复用同一份正文，仅剥掉系统头（见 Mxh_R2_noos_垫片）。
   口径：UTF-8 <-> UTF-32（wchar_t 在 wasi 下为 4 字节）；桥一律不可用（无子进程）。 */
#ifndef ZHC_WASM_SHIM_H
#define ZHC_WASM_SHIM_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <wchar.h>
#include <sys/stat.h>
#include <time.h>
#include <wasi/api.h>

typedef int BOOL;
typedef unsigned int DWORD;
typedef unsigned int UINT;
typedef void* HANDLE;
typedef wchar_t* LPWSTR;
typedef const wchar_t* LPCWSTR;

#ifndef TRUE
#define TRUE 1
#endif
#ifndef FALSE
#define FALSE 0
#endif
#ifndef NULL
#define NULL ((void*)0)
#endif

#define CP_UTF8 65001
#define CP_ACP 0
#define MB_ERR_INVALID_CHARS 8
#define MB_OK 0
#define MB_ICONINFORMATION 64
#define STD_INPUT_HANDLE  ((DWORD)0xFFFFFFF6u)
#define STD_OUTPUT_HANDLE ((DWORD)0xFFFFFFF5u)
#define STD_ERROR_HANDLE  ((DWORD)0xFFFFFFF4u)
#define INVALID_FILE_ATTRIBUTES ((DWORD)0xFFFFFFFFu)
#define FILE_ATTRIBUTE_DIRECTORY 0x10u
#define FILE_ATTRIBUTE_NORMAL 0x80u
#define HANDLE_FLAG_INHERIT 1u
#define STARTF_USESTDHANDLES 0x100u
#define CREATE_NO_WINDOW 0x08000000u
#define WAIT_OBJECT_0 0u
#define WAIT_TIMEOUT 258u

typedef struct { DWORD nLength; void* lpSecurityDescriptor; BOOL bInheritHandle; } SECURITY_ATTRIBUTES;

typedef struct {
    DWORD cb;
    LPWSTR lpReserved;
    LPWSTR lpDesktop;
    LPWSTR lpTitle;
    DWORD dwX, dwY, dwXSize, dwYSize, dwXCountChars, dwYCountChars, dwFillAttribute, dwFlags;
    unsigned short wShowWindow;
    unsigned short cbReserved2;
    unsigned char* lpReserved2;
    HANDLE hStdInput, hStdOutput, hStdError;
} STARTUPINFOW;

typedef struct { HANDLE hProcess, hThread; DWORD dwProcessId, dwThreadId; } PROCESS_INFORMATION;

#ifndef ZeroMemory
#define ZeroMemory(p, n) memset((void*)(p), 0, (size_t)(n))
#endif

/* ---- MSVC 安全 CRT -> wasi-libc ---- */
#define sprintf_s(buf, sz, ...) snprintf((char*)(buf), (size_t)(sz), __VA_ARGS__)
#define strcpy_s(dst, sz, src)  snprintf((char*)(dst), (size_t)(sz), "%s", (const char*)(src))
#define fopen_s(ppf, path, mode) ((*(ppf) = fopen((path), (mode))) ? 0 : 1)

#define _TRUNCATE ((size_t)-1)
#define _snprintf_s(buf, sz, cnt, ...) snprintf((char*)(buf), (size_t)(sz), __VA_ARGS__)

/* 宽字符安全格式化：仅桥命令构造使用，而 wasi 无子进程、该路径不可达。
   保底写成空串并返回 -1（等价「无法构造命令」），不在垫片里复刻整条宽格式化语义。 */
static inline int _snwprintf_s(wchar_t* buf, size_t sz, size_t cnt, const wchar_t* fmt, ...) {
    (void)cnt; (void)fmt;
    if (buf && sz) buf[0] = 0;
    return -1;
}

static inline int zhc_shim_stricmp(const char* a, const char* b) {
    while (*a && *b) {
        int x = (*a >= 'A' && *a <= 'Z') ? *a + 32 : *a;
        int y = (*b >= 'A' && *b <= 'Z') ? *b + 32 : *b;
        if (x != y) return x - y;
        a++; b++;
    }
    return (int)(unsigned char)*a - (int)(unsigned char)*b;
}
#define _stricmp(a, b) zhc_shim_stricmp((const char*)(a), (const char*)(b))

static inline int zhc_shim_strcat_s(char* dst, size_t sz, const char* src) {
    size_t used = strlen(dst);
    if (used >= sz) return 1;
    snprintf(dst + used, sz - used, "%s", src);
    return 0;
}
#define strcat_s(dst, sz, src) zhc_shim_strcat_s((char*)(dst), (size_t)(sz), (const char*)(src))

/* ---- UTF-8 <-> UTF-32 ---- */
/* n < 0 表示按 NUL 结尾处理（含结尾 NUL 计入返回值）；dst 为 NULL 或容量不足时只报所需长度 */
static inline int zhc_shim_u8_to_u32(const char* s, int n, wchar_t* dst, int cap) {
    int need = 0, i = 0, o = 0;
    if (n < 0) n = (int)strlen(s) + 1;
    while (i < n) {
        unsigned char c = (unsigned char)s[i];
        unsigned int cp;
        int k;
        if (c < 0x80) { cp = (unsigned int)c; k = 0; }
        else if ((c & 0xE0) == 0xC0) { cp = (unsigned int)(c & 0x1Fu); k = 1; }
        else if ((c & 0xF0) == 0xE0) { cp = (unsigned int)(c & 0x0Fu); k = 2; }
        else if ((c & 0xF8) == 0xF0) { cp = (unsigned int)(c & 0x07u); k = 3; }
        else return 0;
        if (i + k >= n) return 0;
        for (int j = 1; j <= k; j++) cp = (cp << 6) | ((unsigned int)s[i + j] & 0x3Fu);
        if (dst && o < cap) dst[o] = (wchar_t)cp;
        o++;
        need = o;
        i += k + 1;
    }
    return need;
}

static inline int zhc_shim_u32_to_u8(const wchar_t* w, int n, char* dst, int cap) {
    int need = 0, i, o = 0;
    if (n < 0) { n = 0; while (w[n]) n++; n++; }
    for (i = 0; i < n; i++) {
        unsigned int cp = (unsigned int)w[i];
        if (cp < 0x80u) need += 1;
        else if (cp < 0x800u) need += 2;
        else if (cp < 0x10000u) need += 3;
        else need += 4;
    }
    if (!dst || cap < need) return need;
    for (i = 0; i < n; i++) {
        unsigned int cp = (unsigned int)w[i];
        if (cp < 0x80u) { dst[o++] = (char)cp; }
        else if (cp < 0x800u) {
            dst[o++] = (char)(0xC0u | (cp >> 6));
            dst[o++] = (char)(0x80u | (cp & 0x3Fu));
        } else if (cp < 0x10000u) {
            dst[o++] = (char)(0xE0u | (cp >> 12));
            dst[o++] = (char)(0x80u | ((cp >> 6) & 0x3Fu));
            dst[o++] = (char)(0x80u | (cp & 0x3Fu));
        } else {
            dst[o++] = (char)(0xF0u | (cp >> 18));
            dst[o++] = (char)(0x80u | ((cp >> 12) & 0x3Fu));
            dst[o++] = (char)(0x80u | ((cp >> 6) & 0x3Fu));
            dst[o++] = (char)(0x80u | (cp & 0x3Fu));
        }
    }
    return need;
}

static inline int MultiByteToWideChar(UINT cp, DWORD flags, const char* src, int n, wchar_t* dst, int cap) {
    (void)flags;
    /* wasi 无代码页：只认 UTF-8；对 GBK 等老代码页按「无法转换」处理（与 Windows 上转换失败路径同构） */
    if (cp != CP_UTF8) return 0;
    if (!src) return 0;
    return zhc_shim_u8_to_u32(src, n, dst, cap);
}

static inline int WideCharToMultiByte(UINT cp, DWORD flags, const wchar_t* src, int n, char* dst, int cap,
                                      const char* dflt, BOOL* used) {
    (void)flags; (void)dflt; (void)used;
    if (cp != CP_UTF8) return 0;
    if (!src) return 0;
    return zhc_shim_u32_to_u8(src, n, dst, cap);
}

/* ---- 控制台 ---- */
static inline HANDLE GetStdHandle(DWORD which) { return (HANDLE)(uintptr_t)which; }

static inline BOOL WriteConsoleW(HANDLE h, const wchar_t* w, DWORD n, DWORD* written, void* reserved) {
    (void)reserved;
    char stackbuf[4096];
    char* buf = stackbuf;
    int need = zhc_shim_u32_to_u8(w, (int)n, NULL, 0);
    if (need <= 0) { if (written) *written = 0; return 1; }
    if (need > (int)sizeof(stackbuf)) {
        buf = (char*)malloc((size_t)need);
        if (!buf) return 0;
    }
    zhc_shim_u32_to_u8(w, (int)n, buf, need);
    FILE* f = ((uintptr_t)h == (uintptr_t)STD_ERROR_HANDLE) ? stderr : stdout;
    fwrite(buf, 1, (size_t)need, f);
    fflush(f);
    if (buf != stackbuf) free(buf);
    if (written) *written = n;
    return 1;
}

static inline BOOL WriteFile(HANDLE h, const void* buf, DWORD n, DWORD* written, void* ov) {
    (void)h; (void)buf; (void)n; (void)written; (void)ov;
    return 0;
}

static inline BOOL ReadFile(HANDLE h, void* buf, DWORD n, DWORD* got, void* ov) {
    (void)h; (void)buf; (void)n; (void)ov;
    if (got) *got = 0;
    return 0;
}

static inline int MessageBoxW(HANDLE h, LPCWSTR t, LPCWSTR c, UINT type) {
    (void)h; (void)t; (void)c; (void)type;
    return 0; /* wasi 无图形界面：弹窗按「用户关闭」处理 */
}

/* ---- 文件系统 ---- */
static inline DWORD GetFileAttributesA(const char* path) {
    struct stat st;
    if (!path || stat(path, &st) != 0) return INVALID_FILE_ATTRIBUTES;
    return S_ISDIR(st.st_mode) ? FILE_ATTRIBUTE_DIRECTORY : FILE_ATTRIBUTE_NORMAL;
}

static inline DWORD GetFileAttributesW(const wchar_t* path) {
    char buf[4096];
    int need;
    if (!path) return INVALID_FILE_ATTRIBUTES;
    need = zhc_shim_u32_to_u8(path, -1, buf, (int)sizeof(buf));
    if (need <= 0 || need > (int)sizeof(buf)) return INVALID_FILE_ATTRIBUTES;
    return GetFileAttributesA(buf);
}

static inline BOOL CreateDirectoryW(const wchar_t* path, SECURITY_ATTRIBUTES* sa) {
    char buf[4096];
    int need;
    (void)sa;
    if (!path) return 0;
    need = zhc_shim_u32_to_u8(path, -1, buf, (int)sizeof(buf));
    if (need <= 0 || need > (int)sizeof(buf)) return 0;
    return mkdir(buf, 0777) == 0 ? 1 : 0;
}

/* ---- 时间 ---- */
static inline DWORD GetTickCount(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return (DWORD)((uint64_t)ts.tv_sec * 1000ull + (uint64_t)(ts.tv_nsec / 1000000));
}

static inline void Sleep(DWORD ms) {
    struct timespec ts;
    ts.tv_sec = (time_t)(ms / 1000u);
    ts.tv_nsec = (long)((ms % 1000u) * 1000000u);
    nanosleep(&ts, NULL);
}

/* ---- 命令行参数 ---- */
static wchar_t** zhc_shim_argv = NULL;
static int zhc_shim_argc = 0;

static inline void zhc_shim_load_args(void) {
    size_t n = 0, sz = 0;
    char** raw;
    char* data;
    if (zhc_shim_argv) return;
    if (__wasi_args_sizes_get(&n, &sz) != 0 || n == 0) { zhc_shim_argv = NULL; zhc_shim_argc = 0; return; }
    raw = (char**)malloc(sizeof(char*) * n);
    data = (char*)malloc(sz ? sz : 1);
    if (!raw || !data) { free(raw); free(data); return; }
    if (__wasi_args_get((uint8_t**)raw, (uint8_t*)data) != 0) { free(raw); free(data); return; }
    zhc_shim_argv = (wchar_t**)malloc(sizeof(wchar_t*) * n);
    if (!zhc_shim_argv) { free(raw); free(data); return; }
    for (size_t i = 0; i < n; i++) {
        int need = zhc_shim_u8_to_u32(raw[i], -1, NULL, 0);
        wchar_t* w = (wchar_t*)malloc(sizeof(wchar_t) * (size_t)(need > 0 ? need : 1));
        if (!w) { zhc_shim_argc = 0; return; }
        if (need > 0) zhc_shim_u8_to_u32(raw[i], -1, w, need);
        else w[0] = 0;
        zhc_shim_argv[i] = w;
    }
    zhc_shim_argc = (int)n;
    free(raw);
    free(data);
}

static inline LPCWSTR GetCommandLineW(void) {
    static wchar_t buf[8192];
    size_t o = 0;
    zhc_shim_load_args();
    buf[0] = 0;
    for (int i = 0; i < zhc_shim_argc; i++) {
        const wchar_t* w = zhc_shim_argv[i];
        if (i && o + 1 < sizeof(buf) / sizeof(buf[0])) buf[o++] = L' ';
        while (w && *w && o + 1 < sizeof(buf) / sizeof(buf[0])) buf[o++] = *w++;
    }
    buf[o] = 0;
    return buf;
}

static inline LPWSTR* CommandLineToArgvW(LPCWSTR cmd, int* argc) {
    LPWSTR* out;
    (void)cmd; /* 直接取 wasi 真实 argv，避免自行切分与运行环境口径分叉 */
    zhc_shim_load_args();
    if (argc) *argc = zhc_shim_argc;
    if (zhc_shim_argc <= 0) return NULL;
    out = (LPWSTR*)malloc(sizeof(LPWSTR) * (size_t)zhc_shim_argc);
    if (!out) return NULL;
    for (int i = 0; i < zhc_shim_argc; i++) out[i] = zhc_shim_argv[i];
    return out;
}

static inline HANDLE LocalFree(HANDLE p) {
    free(p);
    return NULL;
}

/* ---- 桥（子进程）：wasi 无子进程能力，一律不可用 ---- */
static inline BOOL CreatePipe(HANDLE* r, HANDLE* w, SECURITY_ATTRIBUTES* sa, DWORD size) {
    (void)sa; (void)size;
    if (r) *r = NULL;
    if (w) *w = NULL;
    return 0;
}

static inline BOOL SetHandleInformation(HANDLE h, DWORD mask, DWORD flags) {
    (void)h; (void)mask; (void)flags;
    return 0;
}

static inline BOOL CreateProcessW(LPCWSTR app, LPWSTR cmd, void* pa, void* ta, BOOL inherit,
                                  DWORD flags, void* env, LPCWSTR dir, STARTUPINFOW* si, PROCESS_INFORMATION* pi) {
    (void)app; (void)cmd; (void)pa; (void)ta; (void)inherit; (void)flags;
    (void)env; (void)dir; (void)si;
    if (pi) ZeroMemory(pi, sizeof(PROCESS_INFORMATION));
    return 0;
}

static inline BOOL PeekNamedPipe(HANDLE h, void* buf, DWORD n, DWORD* got, DWORD* avail, DWORD* left) {
    (void)h; (void)buf; (void)n;
    if (got) *got = 0;
    if (avail) *avail = 0;
    if (left) *left = 0;
    return 0;
}

static inline DWORD WaitForSingleObject(HANDLE h, DWORD ms) {
    (void)h; (void)ms;
    return WAIT_TIMEOUT;
}

static inline BOOL TerminateProcess(HANDLE h, UINT code) {
    (void)h; (void)code;
    return 0;
}

static inline BOOL FlushFileBuffers(HANDLE h) {
    (void)h;
    return 0;
}

static inline BOOL CloseHandle(HANDLE h) {
    (void)h;
    return 1;
}

static inline void SetConsoleOutputCP(UINT cp) { (void)cp; }
static inline void SetConsoleCP(UINT cp) { (void)cp; }

/* ================= P0：Win32 虚拟内存语义 -> wasm 线性内存 =================
   背景：ZHC 中文关键字「申请内存 / 释放内存」在内核内置函数 _bi_alloc / _bi_free
         中硬编码展开为 VirtualAlloc / VirtualFree（不区分编译目标）。x86-64 目标
         由 Windows 头提供该 API；wasm32-wasip1 目标无此 API，故此前「内存操作」
         类源码在 wasm 下构建失败（rc=2，7 error）。
   语义对齐要点：
     1) 零初始化：MEM_COMMIT|MEM_RESERVE 提交的页恒为零填充，故用 calloc 而非
        malloc —— 保证「申请后未写先读」在 x86 与 wasm 下同为 0，而非未定义值。
     2) 释放粒度：MEM_RELEASE 整块释放，与 free 一致；VirtualFree 第二参数
        （区域大小）在 RELEASE 语义下无意义，忽略。
     3) 失败语义：VirtualAlloc 失败返回 NULL，calloc 失败亦返回 NULL，一致；
        VirtualFree 成功返回非 0，此处返回 1。
     4) 地址参数：ZHC 不暴露非 NULL 地址提交保留页的能力，addr 恒为 NULL，忽略。
   影响面：仅 wasm 垫片内生效，#define 不影响 x86-64 分支（该分支不含本头）。 */
/* SIZE_T 在 x86-64 分支由 Windows 头提供，wasm 垫片此前缺失；
   而内核 _bi_alloc 生成的 C 含 (SIZE_T) 强制转换，故必须补齐。 */
#ifndef _ZHC_SHIM_SIZE_T_DEFINED
typedef size_t SIZE_T;
#define _ZHC_SHIM_SIZE_T_DEFINED
#endif

#ifndef ZH_MEM_COMMIT
#define ZH_MEM_COMMIT     0x00001000u
#endif
#ifndef ZH_MEM_RESERVE
#define ZH_MEM_RESERVE    0x00002000u
#endif
#ifndef ZH_MEM_RELEASE
#define ZH_MEM_RELEASE    0x00008000u
#endif
#ifndef ZH_PAGE_READWRITE
#define ZH_PAGE_READWRITE 0x04u
#endif

static inline void* zhc_shim_VirtualAlloc(void* addr, SIZE_T size, DWORD type, DWORD protect) {
    (void)addr; (void)type; (void)protect;
    if (size == 0) return NULL;
    return calloc(1, (size_t)size);
}

static inline int zhc_shim_VirtualFree(void* addr, SIZE_T size, DWORD type) {
    (void)size; (void)type;
    if (addr == NULL) return 0;
    free(addr);
    return 1;
}

#define MEM_COMMIT     ZH_MEM_COMMIT
#define MEM_RESERVE    ZH_MEM_RESERVE
#define MEM_RELEASE    ZH_MEM_RELEASE
#define PAGE_READWRITE ZH_PAGE_READWRITE
#define VirtualAlloc   zhc_shim_VirtualAlloc
#define VirtualFree    zhc_shim_VirtualFree
/* ================= P0 补丁结束 ================= */


#endif /* ZHC_WASM_SHIM_H */
'''


Mxh_R1_RUNTIME = r'''
/* ---- zhc 运行库 ---- */
static int zhc_msgbox(const char* s, const char* t) {
    int n1 = MultiByteToWideChar(CP_UTF8, 0, s, -1, NULL, 0);
    wchar_t* w1 = (wchar_t*)malloc(sizeof(wchar_t) * (size_t)(n1 > 0 ? n1 : 1));
    if (n1 > 0) MultiByteToWideChar(CP_UTF8, 0, s, -1, w1, n1);
    int n2 = MultiByteToWideChar(CP_UTF8, 0, t, -1, NULL, 0);
    wchar_t* w2 = (wchar_t*)malloc(sizeof(wchar_t) * (size_t)(n2 > 0 ? n2 : 1));
    if (n2 > 0) MultiByteToWideChar(CP_UTF8, 0, t, -1, w2, n2);
    int r = MessageBoxW(NULL, w1, w2, MB_OK | MB_ICONINFORMATION);
    free(w1); free(w2);
    return r;
}

static const char* zhc_getenv(const char* n) {
    const char* v = getenv(n);
    return v ? v : "";
}

static const char* zhc_addr(uintptr_t p) {
    static char b[24];
    sprintf(b, "0x%llX", (unsigned long long)p);
    return b;
}

/* ---- 控制台输入 ---- */
static char zhc_inbuf[8192];
static char zhc_inbuf2[8192];

static void zhc_wputs(const char* s) {
    int n = MultiByteToWideChar(CP_UTF8, 0, s, -1, NULL, 0);
    if (n <= 0) return;
    wchar_t* w = (wchar_t*)malloc(sizeof(wchar_t) * (size_t)n);
    if (!w) return;
    MultiByteToWideChar(CP_UTF8, 0, s, -1, w, n);
    DWORD wr = 0;
    WriteConsoleW(GetStdHandle(STD_OUTPUT_HANDLE), w, (DWORD)(n - 1), &wr, NULL);
    free(w);
}

static int zhc_utf8_ok(const unsigned char* s, size_t n) {
    size_t i = 0;
    while (i < n) {
        unsigned char c = s[i];
        if (c < 0x80) { i++; continue; }
        int k;
        if ((c & 0xE0) == 0xC0) k = 1;
        else if ((c & 0xF0) == 0xE0) k = 2;
        else if ((c & 0xF8) == 0xF0) k = 3;
        else return 0;
        for (int j = 1; j <= k; j++) {
            if (i + (size_t)j >= n) return 0;
            if ((s[i + (size_t)j] & 0xC0) != 0x80) return 0;
        }
        i += (size_t)k + 1;
    }
    return 1;
}

/* 把 src 从代码页 cp 转为 UTF-8 写入 dst，失败返回 0 */
static int zhc_cp_to_utf8(const char* src, int n, char* dst, int cap, UINT cp) {
    int wl, ul, ok = 0;
    wchar_t* w;
    if (n <= 0) { if (cap > 0) dst[0] = 0; return 1; }
    wl = MultiByteToWideChar(cp, MB_ERR_INVALID_CHARS, src, n, NULL, 0);
    if (wl <= 0) return 0;
    w = (wchar_t*)malloc(sizeof(wchar_t) * (size_t)wl);
    if (!w) return 0;
    MultiByteToWideChar(cp, 0, src, n, w, wl);
    ul = WideCharToMultiByte(CP_UTF8, 0, w, wl, NULL, 0, NULL, NULL);
    if (ul > 0 && ul < cap) {
        WideCharToMultiByte(CP_UTF8, 0, w, wl, dst, ul, NULL, NULL);
        dst[ul] = 0;
        ok = 1;
    }
    free(w);
    return ok;
}

/* 提示语后读一行；中文输入若为 ANSI/GBK 编码则自动转 UTF-8。返回值下次调用会被覆盖 */
static const char* zhc_input(const char* prompt) {
    size_t n;
    if (prompt && prompt[0]) zhc_wputs(prompt);
    if (!fgets(zhc_inbuf, (int)sizeof zhc_inbuf, stdin)) { zhc_inbuf[0] = 0; return zhc_inbuf; }
    n = strlen(zhc_inbuf);
    while (n > 0 && (zhc_inbuf[n - 1] == '\n' || zhc_inbuf[n - 1] == '\r')) zhc_inbuf[--n] = 0;
    if (zhc_utf8_ok((const unsigned char*)zhc_inbuf, n)) return zhc_inbuf;
    if (zhc_cp_to_utf8(zhc_inbuf, (int)n, zhc_inbuf2, (int)sizeof zhc_inbuf2, CP_ACP)) return zhc_inbuf2;
    if (CP_ACP != 936 && zhc_cp_to_utf8(zhc_inbuf, (int)n, zhc_inbuf2, (int)sizeof zhc_inbuf2, 936))
        return zhc_inbuf2;
    return zhc_inbuf;
}

/* ---- 文件读写 ---- */
static const char* zhc_read_file(const char* path) {
    char* b;
    FILE* f;
    long n;
    size_t got;
    f = fopen(path, "rb");
    if (!f) { b = (char*)malloc(1); if (b) b[0] = 0; return b; }
    fseek(f, 0, SEEK_END);
    n = ftell(f);
    fseek(f, 0, SEEK_SET);
    if (n < 0) n = 0;
    b = (char*)malloc((size_t)n + 1);
    if (!b) { fclose(f); return NULL; }
    got = fread(b, 1, (size_t)n, f);
    fclose(f);
    b[got] = 0;
    /* 去掉 UTF-8 BOM，避免输出时出现不可见前缀 */
    if (got >= 3 && (unsigned char)b[0] == 0xEF && (unsigned char)b[1] == 0xBB
        && (unsigned char)b[2] == 0xBF) {
        memmove(b, b + 3, got - 2);
        got -= 3;
    }
    /* 老式 GBK 文本：转为 UTF-8 后再交给程序 */
    if (got > 0 && !zhc_utf8_ok((const unsigned char*)b, got)) {
        int wl = MultiByteToWideChar(936, 0, b, (int)got, NULL, 0);
        if (wl > 0) {
            wchar_t* w = (wchar_t*)malloc(sizeof(wchar_t) * (size_t)wl);
            if (w) {
                int ul;
                MultiByteToWideChar(936, 0, b, (int)got, w, wl);
                ul = WideCharToMultiByte(CP_UTF8, 0, w, wl, NULL, 0, NULL, NULL);
                if (ul > 0) {
                    char* u = (char*)malloc((size_t)ul + 1);
                    if (u) {
                        WideCharToMultiByte(CP_UTF8, 0, w, wl, u, ul, NULL, NULL);
                        u[ul] = 0;
                        free(b);
                        free(w);
                        return u;
                    }
                }
                free(w);
            }
        }
    }
    return b;
}

static int zhc_write_file(const char* path, const char* s, int append) {
    FILE* f = fopen(path, append ? "ab" : "wb");
    if (!f) return -1;
    if (!s) s = "";
    size_t n = strlen(s);
    size_t w = fwrite(s, 1, n, f);
    fclose(f);
    return (int)w;
}

static int zhc_file_exists(const char* path) {
    DWORD a = GetFileAttributesA(path);
    return (a != INVALID_FILE_ATTRIBUTES && !(a & FILE_ATTRIBUTE_DIRECTORY)) ? 1 : 0;
}

/* 数值/逻辑 临时转文本：8 槽环形缓冲，专供 写文件 / 写行 这类即用即弃的场景，调用方不得保存指针 */
static const char* zhc_tmp_i(int64_t v) {
    static char b[8][32];
    static int i = 0;
    i = (i + 1) & 7;
    sprintf_s(b[i], sizeof(b[i]), "%lld", (long long)v);
    return b[i];
}

static const char* zhc_tmp_d(double v) {
    static char b[8][64];
    static int i = 0;
    i = (i + 1) & 7;
    sprintf_s(b[i], sizeof(b[i]), "%.15g", v);
    return b[i];
}

static const char* zhc_tmp_b(int v) {
    return v ? "真" : "假";
}

/* 追加一行：内容后自动补换行，省掉手工拼接换行符 */
static int zhc_write_line(const char* path, const char* s) {
    FILE* f;
    size_t n, w, w2;
    if (!s) s = "";
    f = fopen(path, "ab");
    if (!f) return -1;
    n = strlen(s);
    w = fwrite(s, 1, n, f);
    w2 = fwrite("\n", 1, 1, f);
    fclose(f);
    return (int)(w + w2);
}

/* 文件字节数，失败返回 -1 */
static int64_t zhc_file_size(const char* path) {
    FILE* f = fopen(path, "rb");
    long sz;
    if (!f) return -1;
    fseek(f, 0, SEEK_END);
    sz = ftell(f);
    fclose(f);
    return (int64_t)sz;
}

static void zhc_free_text(const char* s) {
    if (s) free((void*)s);
}

/* ---- 文本处理：拼接 / 转文本 / 长度 / 比较 ---- */
static const char* zhc_dup(const char* s) {
    size_t n;
    char* r;
    if (!s) s = "";
    n = strlen(s);
    r = (char*)malloc(n + 1);
    if (!r) return "";
    memcpy(r, s, n + 1);
    return r;
}

static const char* zhc_concat(const char* a, const char* b) {
    size_t na, nb;
    char* r;
    if (!a) a = "";
    if (!b) b = "";
    na = strlen(a);
    nb = strlen(b);
    r = (char*)malloc(na + nb + 1);
    if (!r) return a;
    memcpy(r, a, na);
    memcpy(r + na, b, nb + 1);
    return r;
}

static const char* zhc_num2str(int64_t v) {
    char b[32];
    sprintf_s(b, sizeof(b), "%lld", (long long)v);
    return zhc_dup(b);
}

static const char* zhc_num2str_d(double v) {
    char b[64];
    sprintf_s(b, sizeof(b), "%.15g", v);
    return zhc_dup(b);
}

static const char* zhc_bool2str(int v) {
    return zhc_dup(v ? "真" : "假");
}

static int64_t zhc_textlen(const char* s) {
    int n;
    if (!s) return 0;
    n = MultiByteToWideChar(CP_UTF8, 0, s, -1, NULL, 0);
    return n > 0 ? (int64_t)(n - 1) : 0;
}

static int zhc_text_eq(const char* a, const char* b) {
    if (!a) a = "";
    if (!b) b = "";
    return strcmp(a, b) == 0 ? 1 : 0;
}

/* ---- 命令行参数（宽字符读入后转 UTF-8） ---- */
static int zhc_argc_n = 0;
static char** zhc_argv = NULL;

static void zhc_init_args(void) {
    LPWSTR* w = CommandLineToArgvW(GetCommandLineW(), &zhc_argc_n);
    if (!w || zhc_argc_n <= 0) { zhc_argc_n = 0; return; }
    zhc_argv = (char**)malloc(sizeof(char*) * (size_t)zhc_argc_n);
    for (int i = 0; i < zhc_argc_n; i++) {
        int n = WideCharToMultiByte(CP_UTF8, 0, w[i], -1, NULL, 0, NULL, NULL);
        char* b = (char*)malloc((size_t)(n > 0 ? n : 1));
        if (n > 0) WideCharToMultiByte(CP_UTF8, 0, w[i], -1, b, n, NULL, NULL);
        else b[0] = 0;
        zhc_argv[i] = b;
    }
    LocalFree(w);
}

static const char* zhc_arg(int i) {
    if (!zhc_argv || i < 0 || i >= zhc_argc_n) return "";
    return zhc_argv[i];
}

/* ==== 容器运行时：表／记录／列表统一为动态值 ====
   内存由运行时托管（只分配不回收，进程退出由系统整体回收），因此容器可在变量间自由传递，
   不会出现悬垂指针或二次释放。文本所有权：写入容器的文本都会被复制一份。 */

#define ZHC_T_NULL 0
#define ZHC_T_BOOL 1
#define ZHC_T_INT  2
#define ZHC_T_FLT  3
#define ZHC_T_STR  4
#define ZHC_T_TAB  5
#define ZHC_T_REC  6
#define ZHC_T_ARR  7

typedef struct zhc_val zhc_val;
typedef struct zhc_kv { char* k; zhc_val* v; } zhc_kv;

struct zhc_val {
    int t;
    int b;
    int64_t i;
    double d;
    char* s;
    char** col;   int* cty;  int ncol, ccol;   /* 表：列名 / 列类型码 */
    zhc_val** row; int nrow, crow;             /* 表：行（每行是一个记录） */
    zhc_kv* kv;    int nkv, ckv;               /* 记录 */
    zhc_val** it;  int nit, cit;               /* 列表 */
};

static void zhc_rt_err(const char* code, const char* func, const char* msg) {
    fprintf(stderr, "[%s] 运行期错误：%s %s\n", code, func, msg);
    fflush(stderr);
}

static const char* zhc_tname(int t) {
    switch (t) {
    case ZHC_T_NULL: return "空";
    case ZHC_T_BOOL: return "逻辑";
    case ZHC_T_INT:  return "整数";
    case ZHC_T_FLT:  return "浮点";
    case ZHC_T_STR:  return "文本";
    case ZHC_T_TAB:  return "表";
    case ZHC_T_REC:  return "记录";
    case ZHC_T_ARR:  return "列表";
    }
    return "未知";
}

/* 中文类型名 -> 运行期类型码；非法返回 -1 */
static int zhc_tcode(const char* cn) {
    if (!cn) return -1;
    if (strcmp(cn, "整数") == 0) return ZHC_T_INT;
    if (strcmp(cn, "浮点") == 0) return ZHC_T_FLT;
    if (strcmp(cn, "文本") == 0) return ZHC_T_STR;
    if (strcmp(cn, "逻辑") == 0) return ZHC_T_BOOL;
    if (strcmp(cn, "字节") == 0) return ZHC_T_INT;
    if (strcmp(cn, "无符号") == 0) return ZHC_T_INT;
    if (strcmp(cn, "指针") == 0) return ZHC_T_INT;
    if (strcmp(cn, "表") == 0) return ZHC_T_TAB;
    if (strcmp(cn, "记录") == 0) return ZHC_T_REC;
    if (strcmp(cn, "列表") == 0) return ZHC_T_ARR;
    return -1;
}

static zhc_val* zhc_newv(int t) {
    zhc_val* v = (zhc_val*)calloc(1, sizeof(zhc_val));
    if (v) v->t = t;
    return v;
}

static zhc_val* zhc_mknull(void) { return zhc_newv(ZHC_T_NULL); }
static zhc_val* zhc_mkbool(int x) { zhc_val* v = zhc_newv(ZHC_T_BOOL); if (v) v->b = x ? 1 : 0; return v; }
static zhc_val* zhc_mkint(int64_t x) { zhc_val* v = zhc_newv(ZHC_T_INT); if (v) v->i = x; return v; }
static zhc_val* zhc_mkflt(double x) { zhc_val* v = zhc_newv(ZHC_T_FLT); if (v) v->d = x; return v; }
static zhc_val* zhc_mkstr(const char* s) { zhc_val* v = zhc_newv(ZHC_T_STR); if (v) v->s = (char*)zhc_dup(s ? s : ""); return v; }

/* 新建("表"|"记录"|"列表") */
static zhc_val* zhc_newof(const char* cn) {
    int t = zhc_tcode(cn);
    if (t != ZHC_T_TAB && t != ZHC_T_REC && t != ZHC_T_ARR) {
        zhc_rt_err("E401", "新建", "类型名必须是 表／记录／列表 之一，收到的是其他文本");
        return zhc_mknull();
    }
    return zhc_newv(t);
}

/* ---- 记录：查找 / 设置 ---- */
static int zhc_rec_find(zhc_val* r, const char* k) {
    int i;
    for (i = 0; i < r->nkv; i++)
        if (strcmp(r->kv[i].k, k) == 0) return i;
    return -1;
}

static zhc_val* zhc_rec_get(zhc_val* r, const char* k) {
    int i = zhc_rec_find(r, k);
    return i < 0 ? NULL : r->kv[i].v;
}

static int zhc_rec_put(zhc_val* r, const char* k, zhc_val* v) {
    int i = zhc_rec_find(r, k);
    if (i >= 0) { r->kv[i].v = v; return i; }
    if (r->nkv == r->ckv) {
        int nc = r->ckv ? r->ckv * 2 : 8;
        zhc_kv* p = (zhc_kv*)realloc(r->kv, sizeof(zhc_kv) * (size_t)nc);
        if (!p) { zhc_rt_err("E000", "置元素", "记录扩容失败"); return -1; }
        r->kv = p; r->ckv = nc;
    }
    r->kv[r->nkv].k = (char*)zhc_dup(k);
    r->kv[r->nkv].v = v;
    return r->nkv++;
}

/* ---- 表：列 ---- */
static int zhc_tab_col(zhc_val* t, const char* name) {
    int i;
    for (i = 0; i < t->ncol; i++)
        if (strcmp(t->col[i], name) == 0) return i;
    return -1;
}

/* 造列：返回 1 成功；0 列名重复；-1 类型名非法；-2 已有数据（E404） */
static int64_t zhc_addcol(zhc_val* t, const char* name, const char* typecn) {
    int tc, i;
    if (!t || t->t != ZHC_T_TAB) { zhc_rt_err("E401", "造列", "第一个参数必须是表"); return -1; }
    if (zhc_tab_col(t, name) >= 0) { zhc_rt_err("E403", "造列", "列名重复"); return 0; }
    if (t->nrow > 0) { zhc_rt_err("E404", "造列", "表里已有数据，不能再增列"); return -2; }
    tc = zhc_tcode(typecn);
    if (tc < 0) { zhc_rt_err("E401", "造列", "类型词非法：须为 整数／浮点／文本／逻辑／字节／无符号／指针／表／记录／列表"); return -1; }
    if (t->ncol == t->ccol) {
        int nc = t->ccol ? t->ccol * 2 : 8;
        char** pc = (char**)realloc(t->col, sizeof(char*) * (size_t)nc);
        int* pt = (int*)realloc(t->cty, sizeof(int) * (size_t)nc);
        if (!pc || !pt) { zhc_rt_err("E000", "造列", "表扩容失败"); return -1; }
        t->col = pc; t->cty = pt; t->ccol = nc;
    }
    t->col[t->ncol] = (char*)zhc_dup(name);
    t->cty[t->ncol] = tc;
    t->ncol++;
    for (i = 0; i < t->nrow; i++) {   /* 不会发生（已拦 nrow>0），保留以防顺序被改 */
        if (zhc_rec_get(t->row[i], name) == NULL) zhc_rec_put(t->row[i], name, zhc_mknull());
    }
    return 1;
}

/* 把 v 按列类型 cty 归一；成功返回 zc（可能是新值），失败返回 NULL */
static zhc_val* zhc_coerce(zhc_val* v, int cty, const char* colname) {
    if (!v) return NULL;
    (void)colname;
    if (v->t == ZHC_T_NULL) return v;
    if (cty == ZHC_T_BOOL) {
        /* 逻辑列单独收紧：以前和整数列共用一个分支，真/假会被压成 1/0，
           导出 JSON 就成数字，下游分不清「在售」到底是布尔还是数量 */
        if (v->t == ZHC_T_BOOL) return v;
        if (v->t == ZHC_T_INT) return zhc_mkbool(v->i != 0);
        if (v->t == ZHC_T_FLT) return zhc_mkbool(v->d != 0.0);
        zhc_rt_err("E402", "追加", "列类型不匹配：该列只接受逻辑值");
        return NULL;
    }
    if (cty == ZHC_T_INT) {
        if (v->t == ZHC_T_INT) return v;
        if (v->t == ZHC_T_BOOL) return zhc_mkint((int64_t)(v->b ? 1 : 0));
        if (v->t == ZHC_T_FLT) {
            if (v->d == (double)(int64_t)v->d) return zhc_mkint((int64_t)v->d);
            zhc_rt_err("E402", "追加", "浮点值不能写入整数列");
            return NULL;
        }
        zhc_rt_err("E402", "追加", "列类型不匹配：该列只接受数值");
        return NULL;
    }
    if (cty == ZHC_T_FLT) {
        if (v->t == ZHC_T_FLT) return v;
        if (v->t == ZHC_T_INT) return zhc_mkflt((double)v->i);
        if (v->t == ZHC_T_BOOL) return zhc_mkflt((double)(v->b ? 1 : 0));
        zhc_rt_err("E402", "追加", "列类型不匹配：该列只接受数值");
        return NULL;
    }
    if (cty == ZHC_T_STR) {
        if (v->t == ZHC_T_STR) return v;
        if (v->t == ZHC_T_INT) return zhc_mkstr(zhc_num2str(v->i));
        if (v->t == ZHC_T_FLT) return zhc_mkstr(zhc_num2str_d(v->d));
        if (v->t == ZHC_T_BOOL) return zhc_mkstr(zhc_bool2str(v->b));
        zhc_rt_err("E402", "追加", "列类型不匹配：该列只接受标量");
        return NULL;
    }
    if (v->t == cty) return v;
    zhc_rt_err("E402", "追加", "列类型不匹配");
    (void)colname;
    return NULL;
}

/* 按记录建列（首行自动推断） */
static void zhc_tab_autocol(zhc_val* t, zhc_val* r) {
    int i;
    for (i = 0; i < r->nkv; i++) {
        int cty;
        zhc_val* v = r->kv[i].v;
        if (!v || v->t == ZHC_T_NULL) cty = ZHC_T_STR;
        else if (v->t == ZHC_T_BOOL) cty = ZHC_T_BOOL;
        else if (v->t == ZHC_T_INT) cty = ZHC_T_INT;
        else if (v->t == ZHC_T_FLT) cty = ZHC_T_FLT;
        else if (v->t == ZHC_T_STR) cty = ZHC_T_STR;
        else cty = v->t;
        zhc_addcol(t, r->kv[i].k, zhc_tname(cty));
    }
}

/* 按列顺序把行归一为记录 */
static zhc_val* zhc_tab_norm(zhc_val* t, zhc_val* r) {
    zhc_val* o;
    int i;
    if (r->t != ZHC_T_REC) return NULL;
    if (t->ncol == 0) zhc_tab_autocol(t, r);
    o = zhc_newv(ZHC_T_REC);
    for (i = 0; i < t->ncol; i++) {
        zhc_val* v = zhc_rec_get(r, t->col[i]);
        zhc_val* c;
        if (v == NULL) { zhc_rt_err("E402", "追加", "记录缺少列键，已补 空"); zhc_rec_put(o, t->col[i], zhc_mknull()); continue; }
        c = zhc_coerce(v, t->cty[i], t->col[i]);
        if (c == NULL) return NULL;
        zhc_rec_put(o, t->col[i], c);
    }
    if (r->nkv != t->ncol) zhc_rt_err("E402", "追加", "记录含表里没有的键，多余键已被丢弃");
    return o;
}

static int64_t zhc_len(zhc_val* v) {
    if (!v) return 0;
    if (v->t == ZHC_T_TAB) return (int64_t)v->nrow;
    if (v->t == ZHC_T_REC) return (int64_t)v->nkv;
    if (v->t == ZHC_T_ARR) return (int64_t)v->nit;
    if (v->t == ZHC_T_STR) return zhc_textlen(v->s);
    zhc_rt_err("E401", "长度", "参数必须是 表／记录／列表");
    return -1;
}

/* 取(容器, 键)：表按行号 -> 行记录（别名，改写立即生效）；记录按键 -> 值；列表按下标 -> 元素 */
static zhc_val* zhc_get(zhc_val* v, zhc_val* k) {
    if (!v) return zhc_mknull();
    if (v->t == ZHC_T_TAB) {
        if (!k || k->t != ZHC_T_INT) { zhc_rt_err("E402", "取元素", "表的下标必须是整数行号"); return zhc_mknull(); }
        if (k->i < 0 || k->i >= (int64_t)v->nrow) { zhc_rt_err("E402", "取元素", "行号越界"); return zhc_mknull(); }
        return v->row[k->i];
    }
    if (v->t == ZHC_T_REC) {
        zhc_val* r;
        if (!k || k->t != ZHC_T_STR) { zhc_rt_err("E402", "取元素", "记录的键必须是文本"); return zhc_mknull(); }
        r = zhc_rec_get(v, k->s);
        return r ? r : zhc_mknull();
    }
    if (v->t == ZHC_T_ARR) {
        if (!k || k->t != ZHC_T_INT) { zhc_rt_err("E402", "取元素", "列表的下标必须是整数"); return zhc_mknull(); }
        if (k->i < 0 || k->i >= (int64_t)v->nit) { zhc_rt_err("E402", "取元素", "下标越界"); return zhc_mknull(); }
        return v->it[k->i];
    }
    zhc_rt_err("E401", "取元素", "第一个参数必须是 表／记录／列表");
    return zhc_mknull();
}

/* 置(容器, 键, 值)：表置整行，记录置键，列表置下标；返回 1 成功 0 失败 */
static int64_t zhc_set(zhc_val* v, zhc_val* k, zhc_val* x) {
    if (!v) { zhc_rt_err("E401", "置元素", "第一个参数必须是 表／记录／列表"); return 0; }
    if (v->t == ZHC_T_TAB) {
        zhc_val* n;
        if (!k || k->t != ZHC_T_INT) { zhc_rt_err("E402", "置元素", "表的下标必须是整数行号"); return 0; }
        if (k->i < 0 || k->i >= (int64_t)v->nrow) { zhc_rt_err("E402", "置元素", "行号越界"); return 0; }
        n = zhc_tab_norm(v, x ? x : zhc_mknull());
        if (!n) { zhc_rt_err("E402", "置元素", "整行替换要求值是记录，且与列定义兼容"); return 0; }
        v->row[k->i] = n;
        return 1;
    }
    if (v->t == ZHC_T_REC) {
        if (!k || k->t != ZHC_T_STR) { zhc_rt_err("E402", "置元素", "记录的键必须是文本"); return 0; }
        return zhc_rec_put(v, k->s, x ? x : zhc_mknull()) < 0 ? 0 : 1;
    }
    if (v->t == ZHC_T_ARR) {
        if (!k || k->t != ZHC_T_INT) { zhc_rt_err("E402", "置元素", "列表的下标必须是整数"); return 0; }
        if (k->i < 0 || k->i >= (int64_t)v->nit) { zhc_rt_err("E402", "置元素", "下标越界"); return 0; }
        v->it[k->i] = x ? x : zhc_mknull();
        return 1;
    }
    zhc_rt_err("E401", "置元素", "第一个参数必须是 表／记录／列表");
    return 0;
}

/* 追加(容器, 值)：表追加一行；列表尾插；记录不支持追加 */
static int64_t zhc_push(zhc_val* v, zhc_val* x) {
    if (!v) { zhc_rt_err("E401", "追加", "第一个参数必须是 表／列表"); return -1; }
    if (v->t == ZHC_T_ARR) {
        if (v->nit == v->cit) {
            int nc = v->cit ? v->cit * 2 : 8;
            zhc_val** p = (zhc_val**)realloc(v->it, sizeof(zhc_val*) * (size_t)nc);
            if (!p) { zhc_rt_err("E000", "追加", "列表扩容失败"); return -1; }
            v->it = p; v->cit = nc;
        }
        v->it[v->nit++] = x ? x : zhc_mknull();
        return (int64_t)v->nit;
    }
    if (v->t == ZHC_T_TAB) {
        zhc_val* n;
        if (x && x->t == ZHC_T_ARR) {     /* 按列顺序的数组行 */
            int i;
            zhc_val* r;
            if (v->ncol == 0) { zhc_rt_err("E404", "追加", "表还没有列，请先用 造列 定义列，或改用记录追加以自动建列"); return -1; }
            if (x->nit != v->ncol) { zhc_rt_err("E402", "追加", "行元素个数与列数不一致"); return -1; }
            r = zhc_newv(ZHC_T_REC);
            for (i = 0; i < v->ncol; i++) zhc_rec_put(r, v->col[i], x->it[i]);
            n = zhc_tab_norm(v, r);
        } else {
            n = zhc_tab_norm(v, x ? x : zhc_mknull());
        }
        if (!n) return -1;
        if (v->nrow == v->crow) {
            int nc = v->crow ? v->crow * 2 : 8;
            zhc_val** p = (zhc_val**)realloc(v->row, sizeof(zhc_val*) * (size_t)nc);
            if (!p) { zhc_rt_err("E000", "追加", "表扩容失败"); return -1; }
            v->row = p; v->crow = nc;
        }
        v->row[v->nrow++] = n;
        return (int64_t)v->nrow;
    }
    zhc_rt_err("E401", "追加", "记录没有追加语义，请改用 置元素");
    return -1;
}

/* 遍历记录用的按键取键 */
static const char* zhc_keyof(zhc_val* v, int64_t i) {
    if (!v || v->t != ZHC_T_REC) { zhc_rt_err("E401", "遍历", "记录遍历的取值必须是记录"); return ""; }
    if (i < 0 || i >= (int64_t)v->nkv) return "";
    return v->kv[i].k;
}

/* ---- 文本缓冲 ---- */
typedef struct { char* p; size_t n, cap; } zhc_sb;

static void zhc_sb_init(zhc_sb* b) {
    b->cap = 128; b->n = 0;
    b->p = (char*)malloc(b->cap);
    if (b->p) b->p[0] = 0;
}

static void zhc_sb_putn(zhc_sb* b, const char* s, size_t n) {
    if (!b->p) return;
    if (b->n + n + 1 > b->cap) {
        size_t nc = b->cap * 2;
        char* q;
        while (nc < b->n + n + 1) nc *= 2;
        q = (char*)realloc(b->p, nc);
        if (!q) return;
        b->p = q; b->cap = nc;
    }
    memcpy(b->p + b->n, s, n);
    b->n += n;
    b->p[b->n] = 0;
}

static void zhc_sb_puts(zhc_sb* b, const char* s) { zhc_sb_putn(b, s, strlen(s)); }
static void zhc_sb_putc(zhc_sb* b, char c) { zhc_sb_putn(b, &c, 1); }

/* ---- JSON 序列化（契约固定口径：浮点 %.15g，缺小数点补 .0；控制字符转 \\u00xx） ---- */
static void zhc_fmt_d(char* out, size_t cap, double v) {
    int k, i;
    if (v != v || v > 1.7976931348623158e308 || v < -1.7976931348623158e308) {
        strcpy_s(out, cap, "null");
        return;
    }
    sprintf_s(out, cap, "%.15g", v);
    k = (int)strlen(out);
    for (i = 0; i < k; i++)
        if (out[i] == '.' || out[i] == 'e' || out[i] == 'E') return;
    if ((size_t)k + 3 <= cap) { out[k] = '.'; out[k + 1] = '0'; out[k + 2] = 0; }
}

static void zhc_json_str(zhc_sb* b, const char* s) {
    const unsigned char* p = (const unsigned char*)(s ? s : "");
    zhc_sb_putc(b, '"');
    for (; *p; p++) {
        unsigned char c = *p;
        switch (c) {
        case '"':  zhc_sb_puts(b, "\\\""); break;
        case '\\': zhc_sb_puts(b, "\\\\"); break;
        case '\n': zhc_sb_puts(b, "\\n"); break;
        case '\r': zhc_sb_puts(b, "\\r"); break;
        case '\t': zhc_sb_puts(b, "\\t"); break;
        case '\b': zhc_sb_puts(b, "\\b"); break;
        case '\f': zhc_sb_puts(b, "\\f"); break;
        default:
            if (c < 0x20) { char t[8]; sprintf_s(t, sizeof t, "\\u%04x", (unsigned)c); zhc_sb_puts(b, t); }
            else zhc_sb_putc(b, (char)c);
        }
    }
    zhc_sb_putc(b, '"');
}

static void zhc_json_wr(zhc_sb* b, zhc_val* v) {
    char t[64];
    int i;
    if (!v) { zhc_sb_puts(b, "null"); return; }
    switch (v->t) {
    case ZHC_T_NULL: zhc_sb_puts(b, "null"); return;
    case ZHC_T_BOOL: zhc_sb_puts(b, v->b ? "true" : "false"); return;
    case ZHC_T_INT:  sprintf_s(t, sizeof t, "%lld", (long long)v->i); zhc_sb_puts(b, t); return;
    case ZHC_T_FLT:  zhc_fmt_d(t, sizeof t, v->d); zhc_sb_puts(b, t); return;
    case ZHC_T_STR:  zhc_json_str(b, v->s); return;
    case ZHC_T_ARR:
        zhc_sb_putc(b, '[');
        for (i = 0; i < v->nit; i++) {
            if (i) zhc_sb_putc(b, ',');
            zhc_json_wr(b, v->it[i]);
        }
        zhc_sb_putc(b, ']');
        return;
    case ZHC_T_REC:
        zhc_sb_putc(b, '{');
        for (i = 0; i < v->nkv; i++) {
            if (i) zhc_sb_putc(b, ',');
            zhc_json_str(b, v->kv[i].k);
            zhc_sb_putc(b, ':');
            zhc_json_wr(b, v->kv[i].v);
        }
        zhc_sb_putc(b, '}');
        return;
    case ZHC_T_TAB:
        zhc_sb_puts(b, "{\"列\":[");
        for (i = 0; i < v->ncol; i++) {
            if (i) zhc_sb_putc(b, ',');
            zhc_sb_puts(b, "{\"名\":");
            zhc_json_str(b, v->col[i]);
            zhc_sb_puts(b, ",\"类型\":");
            zhc_json_str(b, zhc_tname(v->cty[i]));
            zhc_sb_putc(b, '}');
        }
        zhc_sb_puts(b, "],\"行\":[");
        for (i = 0; i < v->nrow; i++) {
            int c;
            if (i) zhc_sb_putc(b, ',');
            zhc_sb_putc(b, '[');
            for (c = 0; c < v->ncol; c++) {
                if (c) zhc_sb_putc(b, ',');
                zhc_json_wr(b, zhc_rec_get(v->row[i], v->col[c]));
            }
            zhc_sb_putc(b, ']');
        }
        zhc_sb_puts(b, "]}");
        return;
    }
    zhc_sb_puts(b, "null");
}

static const char* zhc_tojson(zhc_val* v) {
    zhc_sb b;
    zhc_sb_init(&b);
    if (!b.p) return "";
    zhc_json_wr(&b, v);
    return b.p;
}

/* ---- JSON 解析（严格：非法输入返回 空 并在 stderr 报 E405） ---- */
typedef struct { const char* p; const char* e; int ok; } zhc_jp;

static void zhc_jp_ws(zhc_jp* j) {
    while (j->p < j->e && (*j->p == ' ' || *j->p == '\t' || *j->p == '\n' || *j->p == '\r')) j->p++;
}

static zhc_val* zhc_jp_val(zhc_jp* j);

static void zhc_sb_putu(zhc_sb* b, unsigned cp) {
    char t[4];
    if (cp < 0x80) { zhc_sb_putc(b, (char)cp); return; }
    if (cp < 0x800) {
        t[0] = (char)(0xC0 | (cp >> 6));
        t[1] = (char)(0x80 | (cp & 0x3F));
        zhc_sb_putn(b, t, 2);
        return;
    }
    if (cp < 0x10000) {
        t[0] = (char)(0xE0 | (cp >> 12));
        t[1] = (char)(0x80 | ((cp >> 6) & 0x3F));
        t[2] = (char)(0x80 | (cp & 0x3F));
        zhc_sb_putn(b, t, 3);
        return;
    }
    t[0] = (char)(0xF0 | (cp >> 18));
    t[1] = (char)(0x80 | ((cp >> 12) & 0x3F));
    t[2] = (char)(0x80 | ((cp >> 6) & 0x3F));
    t[3] = (char)(0x80 | (cp & 0x3F));
    zhc_sb_putn(b, t, 4);
}

static int zhc_hex4(const char* p, unsigned* out) {
    unsigned v = 0;
    int i;
    for (i = 0; i < 4; i++) {
        char c = p[i];
        v <<= 4;
        if (c >= '0' && c <= '9') v |= (unsigned)(c - '0');
        else if (c >= 'a' && c <= 'f') v |= (unsigned)(c - 'a' + 10);
        else if (c >= 'A' && c <= 'F') v |= (unsigned)(c - 'A' + 10);
        else return 0;
    }
    *out = v;
    return 1;
}

static char* zhc_jp_str(zhc_jp* j) {
    zhc_sb b;
    if (j->p >= j->e || *j->p != '"') { j->ok = 0; return NULL; }
    j->p++;
    zhc_sb_init(&b);
    if (!b.p) { j->ok = 0; return NULL; }
    while (j->p < j->e) {
        char c = *j->p;
        if (c == '"') { j->p++; return b.p; }
        if (c == '\\') {
            j->p++;
            if (j->p >= j->e) break;
            c = *j->p++;
            switch (c) {
            case '"':  zhc_sb_putc(&b, '"'); break;
            case '\\': zhc_sb_putc(&b, '\\'); break;
            case '/':  zhc_sb_putc(&b, '/'); break;
            case 'b':  zhc_sb_putc(&b, '\b'); break;
            case 'f':  zhc_sb_putc(&b, '\f'); break;
            case 'n':  zhc_sb_putc(&b, '\n'); break;
            case 'r':  zhc_sb_putc(&b, '\r'); break;
            case 't':  zhc_sb_putc(&b, '\t'); break;
            case 'u': {
                unsigned cp, lo;
                if (j->e - j->p < 4 || !zhc_hex4(j->p, &cp)) { j->ok = 0; return NULL; }
                j->p += 4;
                if (cp >= 0xD800 && cp <= 0xDBFF && j->e - j->p >= 6 && j->p[0] == '\\' && j->p[1] == 'u'
                    && zhc_hex4(j->p + 2, &lo) && lo >= 0xDC00 && lo <= 0xDFFF) {
                    cp = 0x10000 + ((cp - 0xD800) << 10) + (lo - 0xDC00);
                    j->p += 6;
                }
                zhc_sb_putu(&b, cp);
                break;
            }
            default: j->ok = 0; return NULL;
            }
            continue;
        }
        zhc_sb_putc(&b, c);
        j->p++;
    }
    j->ok = 0;
    return NULL;
}

/* 判定表签名：恰含「列」「行」两键，且 列 为 {名,类型} 对象数组、行 为数组 */
static int zhc_is_tabsig(zhc_val* o) {
    zhc_val* c;
    zhc_val* r;
    int i;
    if (!o || o->t != ZHC_T_REC || o->nkv != 2) return 0;
    c = zhc_rec_get(o, "列");
    r = zhc_rec_get(o, "行");
    if (!c || c->t != ZHC_T_ARR || !r || r->t != ZHC_T_ARR) return 0;
    for (i = 0; i < c->nit; i++) {
        zhc_val* it = c->it[i];
        zhc_val* n;
        zhc_val* t;
        if (!it || it->t != ZHC_T_REC || it->nkv != 2) return 0;
        n = zhc_rec_get(it, "名");
        t = zhc_rec_get(it, "类型");
        if (!n || n->t != ZHC_T_STR || !t || t->t != ZHC_T_STR) return 0;
        if (zhc_tcode(t->s) < 0) return 0;
    }
    return 1;
}

static zhc_val* zhc_jp_val(zhc_jp* j) {
    zhc_jp_ws(j);
    if (j->p >= j->e) { j->ok = 0; return NULL; }
    if (*j->p == '{') {
        zhc_val* rec = zhc_newv(ZHC_T_REC);
        j->p++;
        zhc_jp_ws(j);
        if (j->p < j->e && *j->p == '}') { j->p++; return rec; }
        for (;;) {
            char* k;
            zhc_val* v;
            zhc_jp_ws(j);
            k = zhc_jp_str(j);
            if (!k) return NULL;
            zhc_jp_ws(j);
            if (j->p >= j->e || *j->p != ':') { j->ok = 0; return NULL; }
            j->p++;
            v = zhc_jp_val(j);
            if (!j->ok) return NULL;
            zhc_rec_put(rec, k, v);
            zhc_jp_ws(j);
            if (j->p < j->e && *j->p == ',') { j->p++; continue; }
            if (j->p < j->e && *j->p == '}') { j->p++; break; }
            j->ok = 0;
            return NULL;
        }
        if (zhc_is_tabsig(rec)) {           /* 表签名 -> 还原成表 */
            zhc_val* tab = zhc_newv(ZHC_T_TAB);
            zhc_val* cs = zhc_rec_get(rec, "列");
            zhc_val* rs = zhc_rec_get(rec, "行");
            int i, c;
            for (i = 0; i < cs->nit; i++) {
                zhc_val* it = cs->it[i];
                zhc_addcol(tab, zhc_rec_get(it, "名")->s, zhc_rec_get(it, "类型")->s);
            }
            for (i = 0; i < rs->nit; i++) {
                zhc_val* r = rs->it[i];
                zhc_val* o;
                if (!r || r->t != ZHC_T_ARR || r->nit != tab->ncol) { j->ok = 0; return NULL; }
                o = zhc_newv(ZHC_T_REC);
                for (c = 0; c < tab->ncol; c++) zhc_rec_put(o, tab->col[c], zhc_coerce(r->it[c], tab->cty[c], tab->col[c]));
                zhc_push(tab, o);
            }
            return tab;
        }
        return rec;
    }
    if (*j->p == '[') {
        zhc_val* arr = zhc_newv(ZHC_T_ARR);
        j->p++;
        zhc_jp_ws(j);
        if (j->p < j->e && *j->p == ']') { j->p++; return arr; }
        for (;;) {
            zhc_val* v = zhc_jp_val(j);
            if (!j->ok) return NULL;
            zhc_push(arr, v);
            zhc_jp_ws(j);
            if (j->p < j->e && *j->p == ',') { j->p++; continue; }
            if (j->p < j->e && *j->p == ']') { j->p++; break; }
            j->ok = 0;
            return NULL;
        }
        return arr;
    }
    if (*j->p == '"') {
        char* s = zhc_jp_str(j);
        if (!s) return NULL;
        return zhc_mkstr(s);
    }
    if (j->e - j->p >= 4 && strncmp(j->p, "true", 4) == 0) { j->p += 4; return zhc_mkbool(1); }
    if (j->e - j->p >= 5 && strncmp(j->p, "false", 5) == 0) { j->p += 5; return zhc_mkbool(0); }
    if (j->e - j->p >= 4 && strncmp(j->p, "null", 4) == 0) { j->p += 4; return zhc_mknull(); }
    {
        const char* st = j->p;
        int isflt = 0;
        char buf[64];
        size_t n;
        if (j->p < j->e && (*j->p == '-' || *j->p == '+')) j->p++;
        while (j->p < j->e && ((*j->p >= '0' && *j->p <= '9') || *j->p == '.' || *j->p == 'e'
               || *j->p == 'E' || *j->p == '-' || *j->p == '+')) {
            if (*j->p == '.' || *j->p == 'e' || *j->p == 'E') isflt = 1;
            j->p++;
        }
        n = (size_t)(j->p - st);
        if (n == 0 || n >= sizeof buf) { j->ok = 0; return NULL; }
        memcpy(buf, st, n);
        buf[n] = 0;
        if (isflt) return zhc_mkflt(atof(buf));
        return zhc_mkint((int64_t)strtoll(buf, NULL, 10));
    }
}

static zhc_val* zhc_fromjson(const char* s) {
    zhc_jp j;
    zhc_val* v;
    j.p = s ? s : "";
    j.e = j.p + strlen(j.p);
    j.ok = 1;
    v = zhc_jp_val(&j);
    if (!j.ok || v == NULL) {
        zhc_rt_err("E405", "解JSON", "文本不是合法 JSON");
        return zhc_mknull();
    }
    zhc_jp_ws(&j);
    if (j.p != j.e) {
        zhc_rt_err("E405", "解JSON", "JSON 之后还有多余内容");
        return zhc_mknull();
    }
    return v;
}

/* ---- 任意值 -> 具体类型的取值适配：供 遍历 绑定变量与容器赋值给标量时使用 ----
   口径：能无损转换就直接转；容器当标量用属于用户写法错误，报 E402 而不是静默取地址。 */
static zhc_val* zhc_iter(zhc_val* v, int64_t i) {
    if (!v || i < 0) return zhc_mknull();
    if (v->t == ZHC_T_TAB) {
        if (i >= (int64_t)v->nrow) return zhc_mknull();
        return v->row[i];
    }
    if (v->t == ZHC_T_ARR) {
        if (i >= (int64_t)v->nit) return zhc_mknull();
        return v->it[i];
    }
    if (v->t == ZHC_T_REC) {
        if (i >= (int64_t)v->nkv) return zhc_mknull();
        return zhc_mkstr(v->kv[i].k);
    }
    zhc_rt_err("E401", "遍历", "目标必须是 表／记录／列表");
    return zhc_mknull();
}

static int64_t zhc_as_int(zhc_val* v) {
    if (!v) return 0;
    if (v->t == ZHC_T_INT) return v->i;
    if (v->t == ZHC_T_BOOL) return (int64_t)(v->b != 0);
    if (v->t == ZHC_T_FLT) return (int64_t)v->d;
    if (v->t == ZHC_T_STR) return (int64_t)strtoll(v->s ? v->s : "", NULL, 10);
    if (v->t == ZHC_T_NULL) return 0;
    zhc_rt_err("E402", "转整数", "容器不能直接当整数用，请先 取元素 到具体元素");
    return 0;
}

static double zhc_as_flt(zhc_val* v) {
    if (!v) return 0.0;
    if (v->t == ZHC_T_FLT) return v->d;
    if (v->t == ZHC_T_INT) return (double)v->i;
    if (v->t == ZHC_T_BOOL) return (double)(v->b != 0);
    if (v->t == ZHC_T_STR) return strtod(v->s ? v->s : "", NULL);
    if (v->t == ZHC_T_NULL) return 0.0;
    zhc_rt_err("E402", "转浮点", "容器不能直接当浮点用，请先 取元素 到具体元素");
    return 0.0;
}

static int zhc_as_bool(zhc_val* v) {
    if (!v) return 0;
    if (v->t == ZHC_T_BOOL) return v->b != 0;
    if (v->t == ZHC_T_INT) return v->i != 0;
    if (v->t == ZHC_T_FLT) return v->d != 0.0;
    if (v->t == ZHC_T_NULL) return 0;
    if (v->t == ZHC_T_STR) {
        const char* s = v->s ? v->s : "";
        if (s[0] == 0) return 0;
        if (strcmp(s, "假") == 0 || strcmp(s, "0") == 0) return 0;
        return 1;
    }
    return zhc_len(v) > 0;
}

/* 任意值 -> 文本：标量按 输出 的口径给可读文本，容器给单行 JSON（与 转JSON 同口径）。
   4 格环形缓冲，允许同一次 输出 里连写几个不同的动态值而不被覆盖。 */
static const char* zhc_as_str(zhc_val* v) {
    static char bufs[4][512];
    static int slot = 0;
    char* b;
    if (!v) return "";
    if (v->t == ZHC_T_STR) return v->s ? v->s : "";
    if (v->t == ZHC_T_NULL) return "空";
    if (v->t == ZHC_T_BOOL) return v->b ? "真" : "假";
    slot = (slot + 1) & 3;
    b = bufs[slot];
    if (v->t == ZHC_T_INT) {
        sprintf_s(b, 512, "%lld", (long long)v->i);
        return b;
    }
    if (v->t == ZHC_T_FLT) {
        zhc_fmt_d(b, 512, v->d);
        return b;
    }
    return zhc_tojson(v);
}

/* 桥：本版本未接后端（BRIDGE-1.0 在 4.1 落地），恒不可用，调用一律返回失败报文 */
/* ================= JSON 桥：常驻子进程，一行一报文 =================
   协议 BRIDGE-1.0：请求 {"版本","模块","方法","参数"}，响应 {"成功","结果"|"错误"}。
   铁律：桥只负责把结构化 IR 落地成文件，编译与运行不依赖桥；
   桥启不起来就返回 B001，让上层走降级路径（xlsx→csv / 文档直接报错），绝不静默吞。 */
#define ZHC_BR_MAX 131072
static HANDLE zhc_br_in = NULL;      /* 写子进程 stdin */
static HANDLE zhc_br_out = NULL;     /* 读子进程 stdout */
static int zhc_br_state = 0;         /* 0 未启动 / 1 就绪 / -1 不可用 */
static PROCESS_INFORMATION zhc_br_pi;
static char zhc_br_req[ZHC_BR_MAX];
static char zhc_br_res[ZHC_BR_MAX];

static const char* zhc_br_home(void) {
    const char* e = getenv("ZHC_BRIDGE_HOME");
    if (e && e[0]) return e;
    return ZHC_BRIDGE_HOME_BURN;
}

static const char* zhc_br_python(void) {
    const char* e = getenv("ZHC_PY");
    if (e && e[0]) return e;
    return ZHC_PY_BURN;
}

static wchar_t* zhc_br_w(const char* s) {
    int n;
    wchar_t* w;
    if (!s) return NULL;
    n = MultiByteToWideChar(CP_UTF8, 0, s, -1, NULL, 0);
    if (n <= 0) return NULL;
    w = (wchar_t*)calloc((size_t)n, sizeof(wchar_t));
    if (!w) return NULL;
    if (MultiByteToWideChar(CP_UTF8, 0, s, -1, w, n) <= 0) { free(w); return NULL; }
    return w;
}

static int zhc_br_readline(char* dst, int cap, int timeout_ms);
static void zhc_br_stop(void);

static int zhc_br_start(void) {
    SECURITY_ATTRIBUTES sa;
    STARTUPINFOW si;
    HANDLE in_r = NULL, in_w = NULL, out_r = NULL, out_w = NULL;
    wchar_t wcmd[4096];
    wchar_t* wpy;
    wchar_t* whome;
    const char* home;
    const char* py;
    if (zhc_br_state != 0) return zhc_br_state == 1;
    zhc_br_state = -1;
    home = zhc_br_home();
    py = zhc_br_python();
    if (!home || !home[0] || !py || !py[0]) return 0;

    /* 桥脚本不存在就别白起进程：CreateProcessW 对「python + 不存在的脚本」照样成功，
       随后 python 立刻退出，会把 桥可用() 误报成真。这里先查文件，直接判不可用。 */
    {
        wchar_t wchk[4096];
        wchar_t* wh0 = zhc_br_w(home);
        DWORD attr;
        if (!wh0) return 0;
        _snwprintf_s(wchk, 4096, _TRUNCATE, L"%ls\\zhc_bridge.py", wh0);
        free(wh0);
        attr = GetFileAttributesW(wchk);
        if (attr == INVALID_FILE_ATTRIBUTES || (attr & FILE_ATTRIBUTE_DIRECTORY)) return 0;
    }

    ZeroMemory(&sa, sizeof(sa));
    sa.nLength = sizeof(sa);
    sa.bInheritHandle = TRUE;
    if (!CreatePipe(&in_r, &in_w, &sa, 65536)) return 0;
    if (!CreatePipe(&out_r, &out_w, &sa, 65536)) {
        CloseHandle(in_r); CloseHandle(in_w);
        return 0;
    }
    /* 只让子进程继承「读请求」和「写响应」两个端，父进程这两端不可继承 */
    SetHandleInformation(in_w, HANDLE_FLAG_INHERIT, 0);
    SetHandleInformation(out_r, HANDLE_FLAG_INHERIT, 0);

    /* 路径可能含中文（工作区目录、桥目录都可能是），一律 UTF-8 → UTF-16 走宽字符 API，
       用 A 版 API 会把 GBK 当命令行的解释规则，中文路径直接开不起来 */
    wpy = zhc_br_w(py);
    whome = zhc_br_w(home);
    if (!wpy || !whome) {
        if (wpy) free(wpy);
        if (whome) free(whome);
        CloseHandle(in_r); CloseHandle(in_w);
        CloseHandle(out_r); CloseHandle(out_w);
        return 0;
    }
    _snwprintf_s(wcmd, 4096, _TRUNCATE, L"\"%ls\" -X utf8 -u \"%ls\\zhc_bridge.py\"", wpy, whome);
    free(wpy);
    free(whome);

    ZeroMemory(&si, sizeof(si));
    si.cb = sizeof(si);
    si.dwFlags = STARTF_USESTDHANDLES;
    si.hStdInput = in_r;
    si.hStdOutput = out_w;
    si.hStdError = GetStdHandle(STD_ERROR_HANDLE);

    ZeroMemory(&zhc_br_pi, sizeof(zhc_br_pi));
    if (!CreateProcessW(NULL, wcmd, NULL, NULL, TRUE,
                        CREATE_NO_WINDOW, NULL, NULL, &si, &zhc_br_pi)) {
        CloseHandle(in_r); CloseHandle(in_w);
        CloseHandle(out_r); CloseHandle(out_w);
        return 0;
    }
    CloseHandle(in_r);
    CloseHandle(out_w);
    zhc_br_in = in_w;
    zhc_br_out = out_r;
    zhc_br_state = 1;
    /* 启动后握手：真发一次 桥.版本，能回协议 JSON 才算可用。否则「python 起来了但
       脚本语法错／解释器不匹配／立刻退出」会被误判成可用，上层就不会走降级。 */
    {
        static const char 探测[] = "{\"版本\":\"1.0\",\"模块\":\"桥\",\"方法\":\"版本\",\"参数\":{}}\n";
        DWORD wr = 0;
        int rr;
        if (!WriteFile(zhc_br_in, 探测, (DWORD)(sizeof(探测) - 1), &wr, NULL)) {
            zhc_br_stop();
            return 0;
        }
        FlushFileBuffers(zhc_br_in);
        rr = zhc_br_readline(zhc_br_res, (int)sizeof(zhc_br_res), 10000);
        if (rr < 0 || zhc_br_res[0] != '{' || strstr(zhc_br_res, "\"成功\"") == NULL) {
            zhc_br_stop();
            return 0;
        }
    }
    return 1;
}

static void zhc_br_stop(void) {
    if (zhc_br_in) { CloseHandle(zhc_br_in); zhc_br_in = NULL; }
    if (zhc_br_out) { CloseHandle(zhc_br_out); zhc_br_out = NULL; }
    if (zhc_br_pi.hProcess) {
        TerminateProcess(zhc_br_pi.hProcess, 0);
        CloseHandle(zhc_br_pi.hProcess);
        CloseHandle(zhc_br_pi.hThread);
        ZeroMemory(&zhc_br_pi, sizeof(zhc_br_pi));
    }
    zhc_br_state = -1;
}

/* 读一行：逐字节读，遇 \n 结束；超时到点抛 B006，不无限阻塞。
   PeekNamedPipe 先探再读，避免子进程卡死把整个程序拖住。 */
static int zhc_br_readline(char* dst, int cap, int timeout_ms) {
    int n = 0;
    DWORD t0 = GetTickCount();
    for (;;) {
        DWORD avail = 0;
        char ch;
        DWORD got = 0;
        if (!PeekNamedPipe(zhc_br_out, NULL, 0, NULL, &avail, NULL)) return -1;
        if (avail == 0) {
            DWORD used = GetTickCount() - t0;
            if ((int)used >= timeout_ms) return -2;
            if (WaitForSingleObject(zhc_br_pi.hProcess, 0) == WAIT_OBJECT_0) return -1;
            Sleep(2);
            continue;
        }
        if (!ReadFile(zhc_br_out, &ch, 1, &got, NULL) || got == 0) return -1;
        if (ch == '\n') break;
        if (ch != '\r') {
            if (n < cap - 1) dst[n++] = ch;
        }
    }
    dst[n] = '\0';
    return n;
}

static const char* zhc_br_fail(const char* code, const char* info) {
    zhc_sb b;
    zhc_sb_init(&b);
    if (!b.p) return "";
    zhc_sb_puts(&b, "{\"成功\":false,\"错误\":{\"码\":\"");
    zhc_sb_puts(&b, code);
    zhc_sb_puts(&b, "\",\"信息\":\"");
    zhc_sb_puts(&b, info);
    zhc_sb_puts(&b, "\"}}");
    return b.p;
}

static int zhc_bridge_ok(void) {
    if (zhc_br_state == 1) return 1;
    if (zhc_br_state == -1) return 0;
    return zhc_br_start();
}

static const char* zhc_bridge_call(const char* mod, const char* meth, const char* args) {
    zhc_sb b;
    DWORD wr = 0;
    int r;
    if (!zhc_bridge_ok()) return zhc_br_fail("B001", "后端不存在或无法启动");
    if (!args || !args[0]) args = "{}";
    zhc_sb_init(&b);
    if (!b.p) return zhc_br_fail("B005", "内存不足");
    zhc_sb_puts(&b, "{\"版本\":\"1.0\",\"模块\":");
    zhc_json_str(&b, mod ? mod : "");
    zhc_sb_puts(&b, ",\"方法\":");
    zhc_json_str(&b, meth ? meth : "");
    zhc_sb_puts(&b, ",\"参数\":");
    zhc_sb_puts(&b, args);
    zhc_sb_putc(&b, '}');
    if (!b.p) return zhc_br_fail("B005", "内存不足");
    _snprintf_s(zhc_br_req, sizeof(zhc_br_req), _TRUNCATE, "%s\n", b.p);
    if (!WriteFile(zhc_br_in, zhc_br_req, (DWORD)strlen(zhc_br_req), &wr, NULL)) {
        zhc_br_stop();
        return zhc_br_fail("B001", "后端已断开");
    }
    FlushFileBuffers(zhc_br_in);
    r = zhc_br_readline(zhc_br_res, (int)sizeof(zhc_br_res), 30000);
    if (r == -2) return zhc_br_fail("B006", "调用超时（30s）");
    if (r < 0) { zhc_br_stop(); return zhc_br_fail("B001", "后端已退出"); }
    /* 契约 3.3：后端返回非协议 JSON 一律判 B002，绝不把垃圾文本当结果往上抛 */
    if (zhc_br_res[0] != '{' || strstr(zhc_br_res, "\"成功\"") == NULL)
        return zhc_br_fail("B002", "报文非法：后端响应不是协议 JSON");
    return zhc_br_res;
}

/* ---- 导出降级（OFFICE-WEB 契约 2.4 硬性条款）----
   桥不可用且目标为「表.导出xlsx」时，ZHC 自身写 CSV 顶替并返回 降级:true，
   保证无桥环境仍能出数据产物；文档／页面 不降级，原样透传 B001，绝不静默吞。
   单元格文本口径与桥侧 _单元文本 完全一致：空→""、布尔→true/false、
   浮点→最短往返表示（整数样值补 .0）、整数→十进制。 */
static void zhc_fmt_d_rt(double v, char* out, size_t cap) {
    char s[64];
    char dig[32];
    char fin[80];
    char es[16];
    const char* p;
    int prec, i, k, n, neg = 0, ex = 0, exp10, point, dlen;
    if (v != v) { sprintf_s(out, cap, "nan"); return; }
    if (v > 1.7976931348623157e308) { sprintf_s(out, cap, "inf"); return; }
    if (v < -1.7976931348623157e308) { sprintf_s(out, cap, "-inf"); return; }
    /* IR 口径对齐：JSON 落地用 %.15g，桥侧拿到的是该文本解析出的 double。
       降级写盘必须先做一次同样的往返，否则同一份 IR 经桥与经降级两条路的字节不一致。 */
    {
        char ir[64];
        sprintf_s(ir, sizeof(ir), "%.15g", v);
        v = strtod(ir, NULL);
    }
    if (v == 0.0) { sprintf_s(out, cap, (1.0 / v < 0.0) ? "-0.0" : "0.0"); return; }
    /* 第一步：找出能整值往返的最短有效位数（等价 Python 的 shortest repr 搜索） */
    for (prec = 1; prec <= 17; prec++) {
        sprintf_s(s, sizeof(s), "%.*e", prec - 1, v);
        if (strtod(s, NULL) == v) break;
    }
    /* 第二步：把 d.dddde±XX 拆成 数字串 dig 与十进制指数 exp10，再按 Python 规则重排。
       Python 的判据：-4 <= exp10 < 16 用定点（整数值补 .0），否则用 d.ddde±XX。 */
    p = s;
    if (*p == '-') { neg = 1; p++; }
    k = 0;
    for (; *p && *p != 'e' && *p != 'E'; p++) {
        if (*p == '.') continue;
        if (k < (int)sizeof(dig) - 1) dig[k++] = *p;
    }
    dig[k] = 0;
    if (*p == 'e' || *p == 'E') ex = atoi(p + 1);
    while (k > 1 && dig[k - 1] == '0') dig[--k] = 0;
    exp10 = ex;
    dlen = k;
    fin[0] = 0;
    if (exp10 >= -4 && exp10 < 16) {
        point = exp10 + 1;
        if (point <= 0) {
            k = 0;
            fin[k++] = '0'; fin[k++] = '.';
            for (i = 0; i < -point; i++) fin[k++] = '0';
            for (i = 0; i < dlen; i++) fin[k++] = dig[i];
            fin[k] = 0;
        } else if (point >= dlen) {
            k = 0;
            for (i = 0; i < dlen; i++) fin[k++] = dig[i];
            for (i = 0; i < point - dlen; i++) fin[k++] = '0';
            fin[k++] = '.'; fin[k++] = '0'; fin[k] = 0;
        } else {
            k = 0;
            for (i = 0; i < dlen; i++) {
                if (i == point) fin[k++] = '.';
                fin[k++] = dig[i];
            }
            fin[k] = 0;
        }
    } else {
        k = 0;
        fin[k++] = dig[0];
        if (dlen > 1) {
            fin[k++] = '.';
            for (i = 1; i < dlen; i++) fin[k++] = dig[i];
        }
        fin[k] = 0;
    }
    if (exp10 >= -4 && exp10 < 16) {
        sprintf_s(out, cap, "%s%s", neg ? "-" : "", fin);
    } else {
        sprintf_s(es, sizeof(es), "e%+03d", exp10);
        sprintf_s(out, cap, "%s%s%s", neg ? "-" : "", fin, es);
    }
}

static void zhc_cell_txt(zhc_val* v, char* out, size_t cap) {
    if (!v || v->t == ZHC_T_NULL) { out[0] = 0; return; }
    switch (v->t) {
    case ZHC_T_BOOL: sprintf_s(out, cap, "%s", v->b ? "true" : "false"); return;
    case ZHC_T_INT:  sprintf_s(out, cap, "%lld", (long long)v->i); return;
    case ZHC_T_FLT:  zhc_fmt_d_rt(v->d, out, cap); return;
    case ZHC_T_STR:  sprintf_s(out, cap, "%s", v->s ? v->s : ""); return;
    default:         sprintf_s(out, cap, "%s", zhc_tojson(v)); return;
    }
}

static void zhc_csv_fld(zhc_sb* b, const char* s) {
    int need, i, n;
    if (!s) s = "";
    need = (strpbrk(s, ",\"\r\n") != NULL);
    if (need) zhc_sb_putc(b, '"');
    n = (int)strlen(s);
    for (i = 0; i < n; i++) {
        if (s[i] == '"') zhc_sb_putc(b, '"');
        zhc_sb_putc(b, s[i]);
    }
    if (need) zhc_sb_putc(b, '"');
}

/* 逐级建父目录：路径统一 UTF-8 → UTF-16 走宽字符 API，中文目录名不会失真 */
static void zhc_mkpath_u(const char* path) {
    char tmp[2048];
    int i, n;
    wchar_t* w;
    if (!path) return;
    n = (int)strlen(path);
    if (n <= 0 || n >= (int)sizeof(tmp)) return;
    memcpy(tmp, path, (size_t)n + 1);
    for (i = 0; i < n; i++) {
        if (tmp[i] == '/' || tmp[i] == '\\') {
            char c;
            if (i == 0) continue;
            if (i == 2 && tmp[1] == ':') continue;
            c = tmp[i];
            tmp[i] = 0;
            w = zhc_br_w(tmp);
            if (w) { CreateDirectoryW(w, NULL); free(w); }
            tmp[i] = c;
        }
    }
}

/* 表 IR 落地成 utf-8-sig CSV，行尾 CRLF（与桥侧 csv.writer 默认一致）
   返回写盘字节数；任何一步写不进去就返回 -1，绝不假报成功。 */
static int zhc_tab_csv(zhc_val* t, const char* path) {
    zhc_sb b;
    char cell[16384];
    int i, j, bytes, w;
    if (!t || t->t != ZHC_T_TAB) return -1;
    zhc_sb_init(&b);
    if (!b.p) return -1;
    for (i = 0; i < t->ncol; i++) {
        if (i) zhc_sb_putc(&b, ',');
        zhc_csv_fld(&b, (t->col && t->col[i]) ? t->col[i] : "");
    }
    zhc_sb_puts(&b, "\r\n");
    for (i = 0; i < t->nrow; i++) {
        zhc_val* r = t->row[i];
        for (j = 0; j < t->ncol; j++) {
            zhc_val* v = NULL;
            int k;
            if (j) zhc_sb_putc(&b, ',');
            if (r && r->t == ZHC_T_REC) {
                k = zhc_rec_find(r, (t->col && t->col[j]) ? t->col[j] : "");
                if (k >= 0) v = r->kv[k].v;
            }
            zhc_cell_txt(v, cell, sizeof(cell));
            zhc_csv_fld(&b, cell);
        }
        zhc_sb_puts(&b, "\r\n");
    }
    bytes = (int)b.n + 3;
    zhc_mkpath_u(path);
    w = zhc_write_file(path, "\xEF\xBB\xBF", 0);
    if (w != 3) { free(b.p); return -1; }
    w = zhc_write_file(path, b.p, 1);
    if (w != (int)b.n) { free(b.p); return -1; }
    free(b.p);
    return bytes;
}

static int zhc_json_false(const char* s, const char* key) {
    char pat[64];
    const char* p;
    if (!s || !key) return 0;
    sprintf_s(pat, sizeof(pat), "\"%s\"", key);
    p = strstr(s, pat);
    if (!p) return 0;
    p += strlen(pat);
    while (*p == ' ' || *p == '\t' || *p == '\r' || *p == '\n') p++;
    if (*p != ':') return 0;
    p++;
    while (*p == ' ' || *p == '\t' || *p == '\r' || *p == '\n') p++;
    return (*p == 'f' || *p == 'F') ? 1 : 0;
}

static const char* zhc_export_call(const char* mod, const char* meth, const char* args) {
    const char* r;
    const char* m = mod ? mod : "";
    const char* f = meth ? meth : "";
    zhc_val* req;
    zhc_val* tab = NULL;
    zhc_val* pv = NULL;
    char csv[1024];
    char tail[128];
    zhc_sb out;
    int n, k, bytes;

    r = zhc_bridge_call(m, f, args);
    if (strcmp(m, "表") != 0 || strcmp(f, "导出xlsx") != 0) return r;
    if (!zhc_json_false(r, "成功")) return r;
    /* 只对「后端不可用(B001)」与「缺依赖(B003)」降级；参数错/写盘错/超时属于
       调用方或环境问题，必须原样暴露，严禁用 CSV 掩盖真实故障。 */
    if (strstr(r, "B001") == NULL && strstr(r, "B003") == NULL) return r;
    req = zhc_fromjson((args && args[0]) ? args : "{}");
    if (!req || req->t != ZHC_T_REC) return r;
    k = zhc_rec_find(req, "表");
    if (k >= 0) tab = req->kv[k].v;
    k = zhc_rec_find(req, "路径");
    if (k >= 0) pv = req->kv[k].v;
    if (!tab || tab->t != ZHC_T_TAB) return r;
    if (!pv || pv->t != ZHC_T_STR || !pv->s || !pv->s[0]) return r;
    sprintf_s(csv, sizeof(csv), "%s", pv->s);
    n = (int)strlen(csv);
    if (n > 4 && _stricmp(csv + n - 4, ".csv") == 0) {
        /* 已是 csv 后缀，直接沿用，绝不叠成 .csv.csv */
    } else {
        if (n > 5 && _stricmp(csv + n - 5, ".xlsx") == 0) { csv[n - 5] = 0; }
        strcat_s(csv, sizeof(csv), ".csv");
    }
    bytes = zhc_tab_csv(tab, csv);
    if (bytes < 0) return zhc_br_fail("B005", "降级写盘失败：目录不可创建或磁盘不可写");
    zhc_sb_init(&out);
    if (!out.p) return r;
    zhc_sb_puts(&out, "{\"成功\":true,\"降级\":true,\"实际格式\":\"csv\",\"原因\":");
    zhc_json_str(&out, r);
    zhc_sb_puts(&out, ",\"结果\":{\"路径\":");
    zhc_json_str(&out, csv);
    sprintf_s(tail, sizeof(tail), ",\"行数\":%d,\"列数\":%d,\"字节\":%d}}", tab->nrow, tab->ncol, bytes);
    zhc_sb_puts(&out, tail);
    return out.p;
}
'''

class Mxh_K0_Compiler:
    def __init__(self, tokens, target="x86-64"):
        global Mxh_K4_定位锚, Mxh_K4_语句锚
        self.toks = tokens
        self.target = target
        self.p = 0
        self.lines = []           # main 函数体 C 行
        self.funcs = []           # FuncSig 列表（定义顺序）
        self.func_bodies = {}     # cname -> [C 行]
        self.scopes = [{}]        # 名字 -> (cname, 类型)
        self.var_seq = 0
        self.label_seq = 0
        self.cur_func = None
        self.cur_buf = self.lines
        # 同一进程内可能多次编译（LSP 复用），每次编译重置定位锚，避免上一轮残留
        Mxh_K4_定位锚 = tokens[0] if tokens else None
        Mxh_K4_语句锚 = tokens[0] if tokens else None

    # ---------------- 词法辅助
    def peek(self, k=0):
        t = self.toks[min(self.p + k, len(self.toks) - 1)]
        if k == 0:
            global Mxh_K4_定位锚
            Mxh_K4_定位锚 = t
        return t

    def next(self):
        t = self.toks[self.p]
        self.p += 1
        return t

    def is_kw(self, val, k=0):
        t = self.peek(k)
        return t.kind == "KW" and t.val == val

    def accept_kw(self, val):
        if self.is_kw(val):
            self.p += 1
            return True
        return False

    def expect_kw(self, val):
        if not self.accept_kw(val):
            t = self.peek()
            raise Mxh_K4_编译错误(f"第 {t.line} 行：[E204] 此处应为「{val}」，实际是 {t.val!r}",
                         码="E204", 行=t.line, 列=t.col,
                         期望=f"关键字「{val}」", 实际=f"{t.val!r}" if t.val else "空")

    def is_op(self, val, k=0):
        t = self.peek(k)
        return t.kind == "OP" and t.val == val

    def accept_op(self, val):
        if self.is_op(val):
            self.p += 1
            return True
        return False

    def expect_op(self, val):
        if not self.accept_op(val):
            t = self.peek()
            raise Mxh_K4_编译错误(f"第 {t.line} 行：[E204] 此处应为「{val}」，实际是 {t.val!r}",
                         码="E204", 行=t.line, 列=t.col,
                         期望=f"符号「{val}」", 实际=f"{t.val!r}" if t.val else "空")

    def expect_id(self):
        t = self.peek()
        if t.kind != "ID":
            if t.kind == "KW":
                _n = t.val
                if _n in TYPE_KW:
                    raise Mxh_K4_编译错误(
                        f"第 {t.line} 行：[E012] 变量名不能与类型词「{_n}」同名，"
                        f"而且类型词只能写在「为」之后、不能前置：要声明整数请写"
                        f" 定义 计数 为 整数 48（写成 定义 整数 计数 为 48 就会撞上本条）；"
                        f"变量名请另起（如「{_n}值」「我的{_n}」）",
                        码="E012", 行=t.line, 列=t.col, 期望="标识符（非类型词）", 实际=f"类型词「{_n}」")
                if _n in BUILTINS:
                    raise Mxh_K4_编译错误(
                        f"第 {t.line} 行：[E011] 变量名不能与内置函数「{_n}」相同，"
                        f"请改名（如「{_n}值」「我的{_n}」）",
                        码="E011", 行=t.line, 列=t.col, 期望="标识符（非内置函数名）", 实际=f"内置函数名「{_n}」")
                raise Mxh_K4_编译错误(
                    f"第 {t.line} 行：[E010] 变量名不能与关键字「{_n}」相同，"
                    f"请改名（如「{_n}值」「我的{_n}」）",
                    码="E010", 行=t.line, 列=t.col, 期望="标识符（非关键字）", 实际=f"关键字「{_n}」")
            raise Mxh_K4_编译错误(f"第 {t.line} 行：[E001] 此处应为标识符，实际是 {t.val!r}",
                         码="E001", 行=t.line, 列=t.col, 期望="标识符", 实际=f"{t.val!r}")
        self.p += 1
        return t.val

    def expect_type(self):
        t = self.peek()
        if t.kind == "KW" and t.val in TYPE_KW:
            self.p += 1
            return TYPE_KW[t.val]
        if t.kind in ("INT", "FLT", "STR") or t.val in ("真", "假", "空"):
            _例 = ("定义 没缺考 为 逻辑 真", "定义 没缺考 为 真") if t.val in ("真", "假") else (
                "定义 姓名 为 文本 \"老孟\"", "定义 姓名 为 \"老孟\"") if t.kind == "STR" else (
                "定义 计数 为 整数 48", "定义 计数 为 48")
            raise Mxh_K4_编译错误(
                f"第 {t.line} 行：[E205] 这里要写的是类型词，你写的是值 {t.val!r}。"
                f"顺序固定为「定义 名字 为 类型词 值」，值必须写在类型词后面："
                f"应写 {_例[0]}（不是 {_例[1]}）。"
                f"类型词：整数、浮点、文本、逻辑、字节、无符号、指针、表、记录、列表、任意值",
                码="E205", 行=t.line, 列=t.col,
                期望="类型词", 实际=f"值 {t.val!r}")
        raise Mxh_K4_编译错误(
            f"第 {t.line} 行：[E205] 此处应为类型词（整数/浮点/文本/逻辑/表/记录/列表），"
            f"实际是 {t.val!r}；顺序固定为「定义 名字 为 类型词 值」",
            码="E205", 行=t.line, 列=t.col,
            期望="类型词", 实际=f"{t.val!r}")

    # ---------------- 作用域
    def push_scope(self):
        self.scopes.append({})

    def pop_scope(self):
        self.scopes.pop()

    def declare(self, name, typ):
        self.var_seq += 1
        cname = f"v{self.var_seq}"
        self.scopes[-1][name] = (cname, typ)
        return cname

    def lookup(self, name, line):
        for sc in reversed(self.scopes):
            if name in sc:
                return sc[name]
        _可见 = []
        for sc in self.scopes:
            _可见.extend(sc.keys())
        _候选 = difflib.get_close_matches(name, _可见, n=3, cutoff=0.5)
        _提示 = ("，最接近的是 " + "、".join(f"「{c}」" for c in _候选)) if _候选 else ""
        raise Mxh_K4_编译错误(
            f"第 {line} 行：[E301] 未定义的变量「{name}」，请先用 定义 语句声明"
            f"（注意全角/半角与繁简写法）{_提示}",
            码="E301", 行=line, 列=Mxh_K4_列(line),
            期望="已声明的变量", 实际=f"未定义的「{name}」")

    def new_label(self, tag):
        self.label_seq += 1
        return f"{tag}{self.label_seq}"

    def emit(self, line=""):
        self.cur_buf.append("    " + line if line else "")

    # ---------------- 程序结构
    def scan_signatures(self):
        """第一遍：收集函数签名，供前置声明与调用检查。"""
        i = 0
        toks = self.toks
        while i < len(toks):
            t = toks[i]
            if t.kind == "KW" and t.val == "函数":
                j = i + 1
                if j >= len(toks) or toks[j].kind != "ID":
                    raise Mxh_K4_编译错误(f"第 {t.line} 行：[E207] 函数名缺失：函数 后面必须紧跟函数名，例如 函数 相加(甲:整数) 返回 整数",
                          码="E207", 行=t.line, 列=t.col, 期望="函数名", 实际=repr(t.val))
                name = toks[j].val
                j += 1
                if j >= len(toks) or not (toks[j].kind == "OP" and toks[j].val == "("):
                    raise Mxh_K4_编译错误(f"第 {t.line} 行：[E208] 函数参数列表缺失：函数名后面必须紧跟半角括号，例如 相加()",
                          码="E208", 行=t.line, 列=t.col)
                j += 1
                params = []
                if not (toks[j].kind == "OP" and toks[j].val == ")"):
                    while True:
                        if toks[j].kind != "ID":
                            raise Mxh_K4_编译错误(f"第 {t.line} 行：[E014] 参数名非法：参数位必须是标识符（不能是数字、关键字或运算符），例如 (甲:整数)",
                          码="E014", 行=t.line, 列=t.col)
                        pname = toks[j].val
                        j += 1
                        if not (toks[j].kind == "OP" and toks[j].val == ":"):
                            raise Mxh_K4_编译错误(f"第 {t.line} 行：[E210] 参数缺少类型标注：每个参数写成 名字:类型，例如 (甲:整数)",
                              码="E210", 行=t.line, 列=t.col)
                        j += 1
                        if not (toks[j].kind == "KW" and toks[j].val in TYPE_KW):
                            raise Mxh_K4_编译错误(f"第 {t.line} 行：[E211] 参数类型非法：类型须为 整数／浮点／文本／逻辑（扩展类型 字节／无符号／指针 同样合法）",
                              码="E211", 行=t.line, 列=t.col)
                        ptype = TYPE_KW[toks[j].val]
                        j += 1
                        params.append((pname, ptype))
                        if toks[j].kind == "OP" and toks[j].val == ",":
                            j += 1
                            continue
                        break
                if not (toks[j].kind == "OP" and toks[j].val == ")"):
                    raise Mxh_K4_编译错误(f"第 {t.line} 行：[E209] 参数列表未闭合：缺少右半角括号 )",
                          码="E209", 行=t.line, 列=t.col)
                j += 1
                ret = None
                if toks[j].kind == "KW" and toks[j].val == "返回":
                    j += 1
                    if not (toks[j].kind == "KW" and toks[j].val in TYPE_KW):
                        raise Mxh_K4_编译错误(f"第 {t.line} 行：[E212] 返回类型非法：返回 后面必须跟合法类型，例如 返回 整数",
                          码="E212", 行=t.line, 列=t.col)
                    ret = TYPE_KW[toks[j].val]
                sig = Mxh_K2_FuncSig(name, params, ret)
                sig.line = t.line
                sig.col = t.col
                if i > 0 and toks[i - 1].kind == "KW" and toks[i - 1].val == "外部":
                    # 外部函数：直接使用 C 侧原始符号名（需为 ASCII 合法标识符）
                    sig.extern = True
                    sig.cname = name
                else:
                    sig.cname = f"f{len(self.funcs) + 1}"
                self.funcs.append(sig)
            i += 1
        # 重名检查
        seen = set()
        for f in self.funcs:
            if f.name in seen:
                raise Mxh_K4_编译错误(
                    f"第 {f.line} 行：[E305] 函数「{f.name}」重复定义，同一个函数名只能定义一次，请改名或删除其中一个",
                    码="E305", 行=f.line, 列=f.col)
            seen.add(f.name)

    def find_func(self, name):
        for f in self.funcs:
            if f.name == name:
                return f
        return None

    def compile(self):
        self.scan_signatures()
        self.parse_block(stop=set())
        if self.peek().kind != "EOF":
            t = self.peek()
            raise Mxh_K4_编译错误(f"第 {t.line} 行：[E213] 多余内容 {t.val!r}：此处已超出可归属的语句结构，请检查是否缺少关键字或括号",
                          码="E213", 行=t.line, 列=t.col)
        return self.assemble()

    # ---------------- 语句
    def parse_block(self, stop):
        while True:
            t = self.peek()
            if t.kind == "EOF":
                if stop:
                    raise Mxh_K4_编译错误(f"[E201] 第 {t.line} 行附近：文件在块结束前到达末尾，缺少「结束」：每个 如果／否则如果／当／循环／函数 块都必须有配对的「结束」",
                          码="E201", 行=t.line, 列=t.col, 期望="结束", 实际="文件末尾")
                return
            if t.kind == "KW" and t.val in stop:
                return
            if t.kind == "KW" and t.val == "结束":
                # 无对应块的孤立结束
                raise Mxh_K4_编译错误(f"第 {t.line} 行：[E206] 多余的「结束」：这里没有与之配对的 如果／当／循环／函数 块",
                          码="E206", 行=t.line, 列=t.col)
            self.parse_stmt()

    def parse_stmt(self):
        global Mxh_K4_语句锚
        t = self.peek()
        Mxh_K4_语句锚 = t
        if t.kind == "KW":
            v = t.val
            if v in BUILTINS:
                self.stmt_call()
                return
            if v == "外部":
                return self.stmt_extern()
            if v == "定义":
                return self.stmt_define()
            if v == "设":
                return self.stmt_assign()
            if v == "输出":
                return self.stmt_output()
            if v == "如果":
                return self.stmt_if()
            if v == "当":
                return self.stmt_while()
            if v == "循环":
                return self.stmt_for()
            if v == "遍历":
                return self.stmt_iter()
            if v == "函数":
                return self.stmt_func()
            if v == "返回":
                return self.stmt_return()
            raise Mxh_K4_编译错误(f"第 {t.line} 行：[E214] 此处不应出现关键字「{v}」：该关键字不能作为语句开头",
                          码="E214", 行=t.line, 列=t.col)
        if t.kind == "ID" and self.is_op("(", 1):
            self.stmt_call()
            return
        raise Mxh_K4_编译错误(f"第 {t.line} 行：[E202] 无法识别的语句起始 {t.val!r}：语句须以 定义／设／输出／输入／如果／当／循环／函数／返回 等关键字开头，或是一个已知的函数调用",
                          码="E202", 行=t.line, 列=t.col, 实际=repr(t.val))

    def stmt_define(self):
        line = self.next().line
        name = self.expect_id()
        self.expect_kw("为")
        typ = self.expect_type()
        cname = self.declare(name, typ)
        # 契约语句形态：定义 x 为 类型 [=初值]
        # 等号是可选的显式分隔符（契约运算符表含 "="），与不带等号的旧写法并存。
        _has_eq = self.accept_op("=")
        # 无显式等号时，有初值的判据（两条都满足才算）：
        #   1) 后一个记号不是语句关键字——保持 P0/P1 既有行为，
        #      定义 x 为 整数 如果 ... 这种写法仍按"无初值 + 新语句"处理；
        #   2) 后一个记号与类型词同一行—— 定义 t 为 表 换行写 造列(t,...) 是更常见的写法，
        #      不能被当成"表 的初值是造列(...)"。
        # 反过来 定义 x 为 整数 转文本(1) 同行，仍按有初值处理。
        _nxt = self.peek()
        if not _has_eq and (self.at_stmt_boundary() or _nxt.line != self.toks[self.p - 1].line):
            # 允许只声明不给初值（系统编程里常先声明后填充），统一按零值初始化
            zero = {"int": "0", "double": "0.0", "str": '""', "bool": "0",
                    "u8": "0", "u64": "0", "ptr": "((void*)0)",
                    "table": 'zhc_newof("表")', "record": 'zhc_newof("记录")',
                    "list": 'zhc_newof("列表")', "any": "zhc_mknull()"}[typ]
            self.emit(f"{C_TYPE[typ]} {cname} = {zero};")
            return
        code, etyp = self.parse_expr()
        if typ != etyp:
            code = self.cast(code, etyp, typ)
        self.emit(f"{C_TYPE[typ]} {cname} = {code};")

    STMT_KW = {"定义", "设", "输出", "如果", "当", "循环", "函数",
               "返回", "结束", "外部", "否则", "否则如果", "遍历"}

    def at_stmt_boundary(self):
        t = self.peek()
        if t.kind == "EOF":
            return True
        return t.kind == "KW" and t.val in self.STMT_KW

    def stmt_assign(self):
        line = self.next().line
        name = self.expect_id()
        self.expect_kw("为")
        cname, typ = self.lookup(name, line)
        code, etyp = self.parse_expr()
        if typ != etyp:
            code = self.cast(code, etyp, typ)
        self.emit(f"{cname} = {code};")

    def 禁空值(self, typ, code, line, 场景):
        """无返回值函数不产生值：出现在取值位置就报 E307，
        否则会被塞进 printf 的三目或实参位，生成的 C 必然编译失败（C2155）。"""
        if typ != "void":
            return
        raise Mxh_K4_编译错误(
            f"第 {line} 行：[E307] 无返回值函数不能作为表达式使用：它没有返回值，"
            f"不能出现在{场景}里，请把它单独写成一行调用",
            码="E307", 行=line, 列=Mxh_K4_列(line),
            期望="有返回值的表达式", 实际="无返回值（void）")

    def stmt_output(self):
        line = self.next().line
        parts = [self.parse_expr()]
        while True:
            if self.accept_op(","):
                parts.append(self.parse_expr())
                continue
            t = self.peek()
            # 语句边界：不带逗号续行的裸参数必须与本语句同行。否则下一行开头的函数调用
            # 会被吞成本行参数——无返回值的调用还会被并进 printf 的三目，构建报 C2155。
            if t.line != line:
                break
            if t.kind in ("INT", "FLT", "STR") or (t.kind == "ID") or (t.kind == "OP" and t.val in ("(", "-")):
                parts.append(self.parse_expr())
                continue
            break
        for code, typ in parts:
            self.禁空值(typ, code, line, "「输出」的取值")
            if typ == "int":
                self.emit(f'printf("%lld", (long long)({code}));')
            elif typ == "double":
                self.emit(f'printf("%g", (double)({code}));')
            elif typ == "str":
                self.emit(f'printf("%s", (const char*)({code}));')
            elif typ == "u8":
                self.emit(f'printf("%lld", (long long)(unsigned char)({code}));')
            elif typ == "u64":
                self.emit(f'printf("%llu", (unsigned long long)({code}));')
            elif typ == "ptr":
                self.emit(f'printf("%s", zhc_addr((uintptr_t)({code})));')
            elif typ in CONTAINER_TYPES or typ == "any":
                # 容器与任意值统一按 JSON 输出（转JSON 的同一口径），便于直接落盘与比对
                self.emit(f'printf("%s", zhc_as_str({code}));')
            # void 已在取值处被 禁空值 拦为 E307；此处只收 bool，其余类型不得兜底生成可疑 C
            elif typ == "bool":
                self.emit(f'printf("%s", ({code}) ? "\\xe7\\x9c\\x9f" : "\\xe5\\x81\\x87");')
        self.emit('printf("\\n");')

    def stmt_if(self):
        line = self.next().line
        cond, _ctyp = self.parse_expr()
        self.禁空值(_ctyp, cond, line, "「如果」的条件")
        self.expect_kw("则")
        self.emit(f"if ({cond}) {{")
        self.parse_block(stop={"否则如果", "否则", "结束"})
        self.emit("}")
        while self.is_kw("否则如果"):
            self.next()
            cond2, _ctyp2 = self.parse_expr()
            self.禁空值(_ctyp2, cond2, line, "「否则如果」的条件")
            self.expect_kw("则")
            self.emit(f"else if ({cond2}) {{")
            self.parse_block(stop={"否则如果", "否则", "结束"})
            self.emit("}")
        if self.accept_kw("否则"):
            self.emit("else {")
            self.parse_block(stop={"结束"})
            self.emit("}")
        self.expect_kw("结束")

    def 中文名(self, cname):
        """由 C 名反查源码里的中文变量名，仅用于报错信息。"""
        for sc in reversed(self.scopes):
            for name, (c, _typ) in sc.items():
                if c == cname:
                    return name
        return cname

    def stmt_while(self):
        _起 = self.next()
        line = _起.line
        cond, _ctyp = self.parse_expr()
        self.禁空值(_ctyp, cond, line, "「当循环」的条件")
        self.expect_kw("则")
        # 静态检查：条件变量必须在循环体内被改写，否则一定是死循环
        需检查 = []
        if re.search(r"(<=|>=|==|!=|(?<![<>])<(?![<>=])|(?<![<>])>(?![<>=]))", cond):
            需检查 = sorted(set(re.findall(r"\bv\d+\b", cond)))
        起位置 = len(self.cur_buf)
        self.emit(f"while ({cond}) {{")
        self.parse_block(stop={"结束"})
        self.emit("}")
        if 需检查:
            循环体 = "\n".join(self.cur_buf[起位置:])
            有改写 = False
            for v in 需检查:
                模式 = re.compile(
                    rf"\b{v}\b\s*(?:\+=|-=|\*=|/=|%=|(?<![=!<>])=(?!=))"
                    rf"|(?:\+\+|--)\s*\b{v}\b|\b{v}\b\s*(?:\+\+|--)")
                if 模式.search(循环体):
                    有改写 = True
                    break
            if not 有改写:
                名 = "、".join(f"「{self.中文名(v)}」" for v in 需检查)
                raise Mxh_K4_编译错误(
                    f"第 {line} 行：[E304] 当循环的条件变量 {名} 在循环体内从未被修改，会无限循环；"
                    f"请在循环体内改写它（如 设 序 为 序 + 1），或改用 循环 序 从 … 到 … 步 …",
                    码="E304", 行=line, 列=_起.col)
        self.expect_kw("结束")

    def stmt_for(self):
        line = self.next().line
        name = self.expect_id()
        self.expect_kw("从")
        e_from, _ = self.parse_expr()
        self.expect_kw("到")
        e_to, _ = self.parse_expr()
        if self.accept_kw("步"):
            e_step, _ = self.parse_expr()
        else:
            e_step = "1LL"
        self.emit("{")
        self.push_scope()
        cname = self.declare(name, "int")
        self.emit(f"{C_TYPE['int']} _b = {e_from}, _e = {e_to}, _s = {e_step};")
        self.emit(f"for ({C_TYPE['int']} {cname} = _b; _s > 0 ? {cname} <= _e : {cname} >= _e; {cname} += _s) {{")
        self.parse_block(stop={"结束"})
        self.emit("}")
        self.pop_scope()
        self.emit("}")
        self.expect_kw("结束")

    def stmt_iter(self):
        """遍历 <容器> 记作 <变量> … 结束

        变量静态类型按容器声明类型决定，编译期就能定，不做运行期形状推断：
          表   -> 任意值，绑定「本行记录」（改它就改表，等价于 取(表, 下标) 的返回值）
          列表 -> 整数，绑定下标（元素请用 取(列表, 下标) 再取，元素类型运行期才知）
          记录 -> 文本，绑定键名
          任意值 -> 任意值，运行期按实际类型给出行记录或键名
        """
        _起 = self.next()
        line = _起.line
        self.emit("{")
        self.push_scope()
        seq = self.var_seq + 1
        it = f"_it{seq}"
        e_code, e_typ = self.parse_expr()
        if e_typ not in CONTAINER_TYPES and e_typ != "any":
            raise Mxh_K4_编译错误(
                f"第 {line} 行：[E401] 遍历 的目标必须是容器（表／记录／列表），实际是「{TYPE_CN.get(e_typ, e_typ)}」："
                f"文字请改用 循环 下标 从 0 到 文本长度-1 步 1",
                码="E401", 行=line, 列=_起.col,
                期望="容器（表／记录／列表）", 实际=TYPE_CN.get(e_typ, e_typ))
        self.emit(f"{C_TYPE['any']} {it} = {e_code};")
        self.emit(f"int64_t _ix{seq} = 0;")
        self.expect_kw("记作")
        name = self.expect_id()
        if e_typ == "list":
            vtyp, vexpr = "int", f"_ix{seq}"
        elif e_typ == "record":
            vtyp, vexpr = "str", f"zhc_as_str(zhc_iter({it}, _ix{seq}))"
        else:                       # 表 / 任意值
            vtyp, vexpr = "any", f"zhc_iter({it}, _ix{seq})"
        cname = self.declare(name, vtyp)
        # 上界每轮重算：循环体里 追加/置 改变了长度也能安全收敛
        self.emit(f"for (; _ix{seq} < zhc_len({it}); ++_ix{seq}) {{")
        self.emit(f"{C_TYPE[vtyp]} {cname} = {vexpr};")
        self.parse_block(stop={"结束"})
        self.emit("}")
        self.pop_scope()
        self.emit("}")
        self.expect_kw("结束")

    def stmt_func(self):
        line = self.next().line
        name = self.expect_id()
        sig = self.find_func(name)
        # 跳过签名部分（已在第一遍解析过）
        self.expect_op("(")
        if not self.is_op(")"):
            while True:
                self.expect_id()
                self.expect_op(":")
                self.expect_type()
                if self.accept_op(","):
                    continue
                break
        self.expect_op(")")
        if self.accept_kw("返回"):
            self.expect_type()

        saved_buf, saved_scopes, saved_func = self.cur_buf, self.scopes, self.cur_func
        body = []
        self.cur_buf = body
        self.scopes = [{}]
        self.cur_func = sig
        self.push_scope()
        params = []
        for pname, ptype in sig.params:
            cname = self.declare(pname, ptype)
            params.append(f"{C_TYPE[ptype]} {cname}")
        self.parse_block(stop={"结束"})
        self.cur_buf, self.scopes, self.cur_func = saved_buf, saved_scopes, saved_func
        self.func_bodies[sig.cname] = (sig, ",".join(params) or "void", body)
        self.expect_kw("结束")

    def stmt_return(self):
        line = self.next().line
        if self.cur_func is None:
            raise Mxh_K4_编译错误(f"第 {line} 行：[E306] 「返回」只能用于函数内部：顶层代码没有可返回的函数",
                          码="E306", 行=line, 列=Mxh_K4_列(line))
        t = self.peek()
        if t.kind == "KW" and (t.val in ("结束", "否则") or t.val in TYPE_KW):
            self.emit("return;")
            return
        code, etyp = self.parse_expr()
        want = self.cur_func.ret
        if want and etyp != want:
            code = self.cast(code, etyp, want)
        self.emit(f"return {code};")

    def stmt_call(self):
        code, _ = self.parse_expr()
        self.emit(f"{code};")

    def stmt_extern(self):
        """外部函数声明：外部 函数 GetTickCount64() 返回 整数

        仅登记签名（第一遍扫描时已完成），此处校验并消耗记号；
        C 侧声明由 assemble() 统一生成，符号名必须是 ASCII 标识符。
        """
        line = self.next().line          # 消费「外部」
        self.expect_kw("函数")
        name = self.expect_id()
        self.expect_op("(")
        if not self.is_op(")"):
            while True:
                self.expect_id()
                self.expect_op(":")
                self.expect_type()
                if self.accept_op(","):
                    continue
                break
        self.expect_op(")")
        if self.accept_kw("返回"):
            self.expect_type()
        sig = self.find_func(name)
        if sig is None or not sig.extern:
            raise Mxh_K4_编译错误(f"第 {line} 行：[E312] 外部函数「{name}」签名登记失败：外部 函数 声明须与第一遍解析一致（名字、参数、返回类型都要能重新识别）",
                          码="E312", 行=line, 列=Mxh_K4_列(line))
        if not re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", sig.cname):
            raise Mxh_K4_编译错误(
                f"第 {line} 行：[E313] 外部函数名必须是 ASCII 标识符（如 MessageBoxW / GetTickCount64）：C 符号名不能含中文",
                码="E313", 行=line, 列=Mxh_K4_列(line))

    def parse_builtin(self, name, line):
        lo, hi, gen = BUILTINS[name]
        self.expect_op("(")
        args = []
        if not self.is_op(")"):
            while True:
                # 类型词直接当文本实参：新建(表)、造列(t, 金额, 整数) 都能写，
                # 免去用户再记一遍引号。但只在"该函数该位置本来就收类型词"时才放行——
                # 否则 转文本(整数 ...) 这类写错的代码会从 E203（表达式错）降级成
                # 后面更晚的报错，等于把诊断改差。白名单按 (函数名, 参数下标) 钉死。
                t = self.peek()
                if (t.kind == "KW" and t.val in TYPE_KW
                        and (name, len(args)) in _TYPEWORD_ARG):
                    self.next()
                    args.append((f'"{t.val}"', "str"))
                else:
                    _ac, _at = self.parse_expr()
                    self.禁空值(_at, _ac, line, f"内置函数「{name}」的实参")
                    args.append((_ac, _at))
                if self.accept_op(","):
                    continue
                break
        self.expect_op(")")
        # 目标能力门禁（R-J）：wasm32-unknown-unknown 零 WASI import、无文件系统。
        # 文件 I/O 在此目标下必须在编译期就拒绝——若放行到运行期，用户拿到的是
        # 「写文件返回 -1、读文件返回空文本」的静默失败，比报错更难查。
        if self.target == "wasm32-unknown-unknown" and name in _NOOS_禁用内置:
            raise Mxh_K4_编译错误(
                f"第 {line} 行：[E314] 目标 wasm32-unknown-unknown 不支持文件 I/O："
                f"内置函数「{name}」在该目标下不可用（该目标零 WASI import、无文件系统与命令行环境）"
                f"；请改用 --target x86-64 或 --target wasm32-wasi",
                码="E314", 行=line, 列=Mxh_K4_列(line),
                期望="不依赖文件系统的表达式", 实际=f"文件 I/O 内置函数「{name}」")
        if not (lo <= len(args) <= hi):
            raise Mxh_K4_编译错误(
                f"第 {line} 行：[E303] 内置函数「{name}」需要 {lo if lo == hi else str(lo) + '~' + str(hi)} 个参数，实际 {len(args)} 个（运行 --api 查看该函数用法）",
                码="E303", 行=line, 列=Mxh_K4_列(line),
                期望=f"{lo if lo == hi else str(lo) + '~' + str(hi)} 个参数", 实际=f"{len(args)} 个参数")
        return gen(args)

    # ---------------- 表达式（Pratt 风格分层）
    def parse_expr(self):
        return self.parse_or()

    def parse_or(self):
        code, typ = self.parse_and()
        while self.accept_kw("或"):
            rc, rt = self.parse_and()
            code = f"(({code}) || ({rc}))"
            typ = "bool"
        return code, typ

    def parse_and(self):
        code, typ = self.parse_not()
        while self.accept_kw("且"):
            rc, rt = self.parse_not()
            code = f"(({code}) && ({rc}))"
            typ = "bool"
        return code, typ

    def parse_not(self):
        if self.accept_kw("非"):
            c, _ = self.parse_not()
            return f"(!({c}))", "bool"
        return self.parse_cmp()

    # ---------------- 标量收敛：any 参与算术/比较前先落成具体类型
    def _scal(self, code, typ, want, line, col=None):
        """any（运行期才知道类型）参与算术或比较时，按对侧类型收敛；
        容器直接参与算术/比较是类型错误，编译期就拦下，不留给运行期乱算。"""
        if typ == "any":
            if want == "double":
                return f"zhc_as_flt({code})", "double"
            if want == "str":
                return f"zhc_as_str({code})", "str"
            return f"zhc_as_int({code})", "int"
        if typ in CONTAINER_TYPES:
            raise Mxh_K4_编译错误(
                f"第 {line} 行：[E308] 容器（表／记录／列表）不能直接参与算术或比较，"
                f"请先用 取元素 取出里面的值",
                码="E308", 行=line, 列=Mxh_K4_列(line) if col is None else col)
        return code, typ

    def parse_cmp(self):
        left, lt = self.parse_bitor()
        t = self.peek()
        if t.kind == "OP" and t.val in ("<", ">", "<=", ">=", "==", "!="):
            op = self.next().val
            right, rt = self.parse_bitor()
            if lt == "str" and rt == "str":
                if op == "==":
                    return f"(strcmp({left},{right}) == 0)", "bool"
                if op == "!=":
                    return f"(strcmp({left},{right}) != 0)", "bool"
                raise Mxh_K4_编译错误(f"第 {t.line} 行：[E310] 文本仅支持 == 与 != 比较：其他比较请先取 长度 或转成数字后再比较",
                          码="E310", 行=t.line, 列=t.col)
            if "any" in (lt, rt):
                # 对侧是文本就按文本比，否则按整数比——任何比较里出现 any 都先落成标量，
                # 绝不让 zhc_val* 指针直接进 C 的比较运算（那样比的是地址）
                want = "str" if (lt == "str" or rt == "str") else (
                    "double" if (lt == "double" or rt == "double") else "int")
                left, lt = self._scal(left, lt, want, t.line)
                right, rt = self._scal(right, rt, want, t.line)
                if want == "str":
                    if op == "==":
                        return f"(strcmp({left},{right}) == 0)", "bool"
                    if op == "!=":
                        return f"(strcmp({left},{right}) != 0)", "bool"
                    raise Mxh_K4_编译错误(f"第 {t.line} 行：[E310] 文本仅支持 == 与 != 比较：其他比较请先取 长度 或转成数字后再比较",
                              码="E310", 行=t.line, 列=t.col)
            return f"(({left}) {op} ({right}))", "bool"
        return left, lt

    # ---- 位运算层（C 优先级：| < ^ < & < 移位），供系统级编程使用
    def parse_bitor(self):
        code, typ = self.parse_bitxor()
        while self.accept_kw("位或"):
            rc, _ = self.parse_bitxor()
            code = f"(({code}) | ({rc}))"
        return code, typ

    def parse_bitxor(self):
        code, typ = self.parse_bitand()
        while self.accept_kw("位异或"):
            rc, _ = self.parse_bitand()
            code = f"(({code}) ^ ({rc}))"
        return code, typ

    def parse_bitand(self):
        code, typ = self.parse_shift()
        while self.accept_kw("位与"):
            rc, _ = self.parse_shift()
            code = f"(({code}) & ({rc}))"
        return code, typ

    def parse_shift(self):
        code, typ = self.parse_add()
        while True:
            if self.accept_kw("左移"):
                c, _ = self.parse_add()
                code = f"((uint64_t)({code}) << (uint64_t)({c}))"
                typ = "u64"
                continue
            if self.accept_kw("右移"):
                c, _ = self.parse_add()
                code = f"((uint64_t)({code}) >> (uint64_t)({c}))"
                typ = "u64"
                continue
            break
        return code, typ

    def parse_add(self):
        code, typ = self.parse_mul()
        while True:
            t = self.peek()
            if t.kind == "OP" and t.val in ("+", "-"):
                op = self.next().val
                rc, rt = self.parse_mul()
                if typ == "str" or rt == "str":
                    raise Mxh_K4_编译错误(f"第 {t.line} 行：[E311] 文本不支持算术运算，请用逗号分隔输出：文本拼接请改用 连接 或在 输出 里用逗号分隔",
                          码="E311", 行=t.line, 列=t.col)
                want = "double" if "double" in (typ, rt) else "int"
                # 取元素／解JSON 的结果是 any（zhc_val*），直接进 + - * / 会变成指针算术，
                # 样本 s05 就此算出 9639177869194800。先收敛成标量再算。
                code, typ = self._scal(code, typ, want, t.line)
                rc, rt = self._scal(rc, rt, want, t.line)
                typ = want
                code = f"(({code}) {op} ({rc}))"
                continue
            break
        return code, typ

    def parse_mul(self):
        code, typ = self.parse_unary()
        while True:
            t = self.peek()
            if t.kind == "OP" and t.val in ("*", "/", "%"):
                op = self.next().val
                rc, rt = self.parse_unary()
                if typ == "str" or rt == "str":
                    raise Mxh_K4_编译错误(f"第 {t.line} 行：[E311] 文本不支持算术运算，请用逗号分隔输出：文本拼接请改用 连接 或在 输出 里用逗号分隔",
                          码="E311", 行=t.line, 列=t.col)
                want = "double" if "double" in (typ, rt) else "int"
                # 取元素／解JSON 的结果是 any（zhc_val*），直接进 + - * / 会变成指针算术，
                # 样本 s05 就此算出 9639177869194800。先收敛成标量再算。
                code, typ = self._scal(code, typ, want, t.line)
                rc, rt = self._scal(rc, rt, want, t.line)
                typ = want
                code = f"(({code}) {op} ({rc}))"
                continue
            break
        return code, typ

    def parse_unary(self):
        if self.accept_op("-"):
            c, t = self.parse_unary()
            return f"(-({c}))", t
        if self.accept_kw("取反"):
            c, _ = self.parse_unary()
            return f"(~(uint64_t)({c}))", "u64"
        return self.parse_primary()

    def parse_primary(self):
        t = self.peek()
        if t.kind == "INT":
            self.next()
            return f"{t.val}LL", "int"
        if t.kind == "FLT":
            self.next()
            return t.val, "double"
        if t.kind == "STR":
            self.next()
            return Mxh_R3_c_string(t.val), "str"
        if t.kind == "KW" and t.val in ("真", "假"):
            self.next()
            return ("1", "bool") if t.val == "真" else ("0", "bool")
        if t.kind == "KW" and t.val == "空":
            self.next()
            return "((void*)0)", "ptr"
        if t.kind == "KW" and t.val in BUILTINS:
            self.next()
            return self.parse_builtin(t.val, t.line)
        if t.kind == "ID":
            self.next()
            if self.is_op("("):
                if t.val in BUILTINS:
                    return self.parse_builtin(t.val, t.line)
                return self.parse_call(t.val, t.line)
            cname, typ = self.lookup(t.val, t.line)
            return cname, typ
        if self.is_op("("):
            self.next()
            c, typ = self.parse_expr()
            self.expect_op(")")
            return f"({c})", typ
        raise Mxh_K4_编译错误(f"第 {t.line} 行：[E203] 表达式处出现意外的 {t.val!r}：这里应是一个值（数字、文本、变量名或函数调用）",
                          码="E203", 行=t.line, 列=t.col, 期望="值或函数调用", 实际=repr(t.val))

    def parse_call(self, name, line):
        sig = self.find_func(name)
        if sig is None:
            _候选 = difflib.get_close_matches(
                name, list(BUILTINS) + [f.name for f in self.funcs], n=3, cutoff=0.5)
            _提示 = ("，最接近的是 " + "、".join(f"「{c}」" for c in _候选)) if _候选 else ""
            raise Mxh_K4_编译错误(
                f"第 {line} 行：[E302] 未定义的函数「{name}」{_提示}。"
                f"本语言共有 {len(BUILTINS)} 个内置函数，运行 --api 可查完整手册；"
                f"自定义函数须先用 函数 名字（参数）…结束 定义",
                    码="E302", 行=line, 列=Mxh_K4_列(line),
                    期望="已定义的函数", 实际=f"未定义的「{name}」")
        self.expect_op("(")
        args = []
        if not self.is_op(")"):
            while True:
                ac, at = self.parse_expr()
                self.禁空值(at, ac, line, f"函数「{name}」的实参")
                args.append((ac, at))
                if self.accept_op(","):
                    continue
                break
        self.expect_op(")")
        if len(args) != len(sig.params):
            raise Mxh_K4_编译错误(f"第 {line} 行：[E303] 函数「{name}」需要 {len(sig.params)} 个参数，实际 {len(args)} 个：请按函数定义时的参数个数与顺序传参",
                          码="E303", 行=line, 列=Mxh_K4_列(line),
                          期望=f"{len(sig.params)} 个参数", 实际=f"{len(args)} 个参数")
        final = []
        for (ac, at), (pname, ptype) in zip(args, sig.params):
            if at != ptype:
                ac = self.cast(ac, at, ptype)
            final.append(ac)
        return f"{sig.cname}({','.join(final)})", (sig.ret or "void")

    def cast(self, code, frm, to):
        if frm == to:
            return code
        # 隐式转换没有自己的 token，定位到当前语句起始（退回最近读取的记号）
        _a = Mxh_K4_定位()
        _行 = _a.line if _a is not None else 0
        _列 = _a.col if _a is not None else 0
        if frm == "void":
            raise Mxh_K4_编译错误(
                f"第 {_行} 行：[E307] 无返回值函数不能作为表达式使用：它没有返回值，请单独调用一行",
                码="E307", 行=_行, 列=_列, 期望="有返回值的表达式", 实际="无返回值（void）")
        # ---- 容器与任意值：共用同一运行期表示（zhc_val*），互相赋值恒等，
        #      越界、类型不合一律由运行期的 zhc_* 报 E401/E402，编译期不做形状推断
        if frm in CONTAINER_TYPES or to in CONTAINER_TYPES or frm == "any" or to == "any":
            _c_frm = frm in CONTAINER_TYPES or frm == "any"
            _c_to = to in CONTAINER_TYPES or to == "any"
            if _c_frm and _c_to:
                return code
            if frm == "any":
                if to in ("int", "u8", "u64"):
                    return f"zhc_as_int({code})"
                if to == "double":
                    return f"zhc_as_flt({code})"
                if to == "bool":
                    return f"zhc_as_bool({code})"
                if to == "str":
                    return f"zhc_as_str({code})"
                if to == "ptr":
                    return f"((void*)(intptr_t)zhc_as_int({code}))"
            if to == "any":
                return _wrap(code, frm)
            raise Mxh_K4_编译错误(
                f"第 {_行} 行：[E308] 无法把「{TYPE_CN.get(frm, frm)}」转换为「{TYPE_CN.get(to, to)}」："
                f"容器只能赋给 表／记录／列表／任意值，标量要装进容器请用 置／追加",
                码="E308", 行=_行, 列=_列, 期望=to, 实际=frm)
        if to == "double":
            return f"((double)({code}))"
        if to == "bool":
            return f"(({code}) != 0)"
        if to == "int":
            if frm == "ptr":
                return f"((int64_t)(intptr_t)({code}))"
            return f"((int64_t)({code}))"
        if to == "u64":
            if frm == "ptr":
                return f"((uint64_t)(uintptr_t)({code}))"
            return f"((uint64_t)({code}))"
        if to == "u8":
            return f"((uint8_t)({code}))"
        if to == "ptr":
            if frm in ("int", "u64", "u8", "bool"):
                return f"((void*)(intptr_t)({code}))"
            return f"((void*)({code}))"
        if to == "str":
            raise Mxh_K4_编译错误(
                f"第 {_行} 行：[E309] 只有文本可以赋给文本类型（指针需转文本请用「格式化地址」）",
                码="E309", 行=_行, 列=_列, 期望="文本", 实际=frm)
        raise Mxh_K4_编译错误(
            f"第 {_行} 行：[E308] 无法把 {frm} 转换为 {to}：请显式改用兼容类型，或先转成 整数／浮点 再转换",
            码="E308", 行=_行, 列=_列, 期望=to, 实际=frm)

    # ---------------- 装配
    def assemble(self):
        目标noos = (self.target == "wasm32-unknown-unknown")
        目标wasm = (self.target == "wasm32-wasi") or 目标noos
        out = []
        out.append("/* 由 zhc 中文编译器生成，请勿手工修改 */")
        if 目标noos:
            # 零 WASI import 目标：不接 libc，系统头由内联 zhc_noos.h 顶替。
            # 任一 <stdio.h>/<stdlib.h> 都会把 wasi-libc 对非 WASI 目标的 #error 逼出来，
            # 故此处一个系统头都不引（这是该目标能与 wasi-sdk 共存的前提）。
            out.append("/* 目标 wasm32-unknown-unknown：无 libc，系统头由内联 zhc_noos.h 顶替 */")
            out.append('#include "zhc_noos.h"')
        else:
            out.append("#include <stdio.h>")
            out.append("#include <stdint.h>")
            out.append("#include <string.h>")
            out.append("#include <stdlib.h>")
        if 目标wasm:
            # wasm32-wasi 与 wasm32-unknown-unknown 均无 windows.h：Win32 面由垫片映射，
            # 运行库源码不动。两目标共用同一份 Win32 面垫片。
            out.append("/* 目标 " + self.target + "：Win32 面由内联垫片提供，不依赖 windows.h */")
            out.append(Mxh_R2_noos_垫片() if 目标noos else Mxh_R2_WASM_SHIM)
        else:
            out.append("#include <windows.h>")
        out.append("")
        # 桥的落点与解释器路径在编译期烧进 C 源，运行时可用 ZHC_BRIDGE_HOME / ZHC_PY 覆盖。
        # 烧进去只是「默认值」，桥仍可整体不可用（B001），编译与运行不因此失败。
        out.append("#define ZHC_BRIDGE_HOME_BURN " + Mxh_R3_c_str(_桥目录()))
        out.append("#define ZHC_PY_BURN " + Mxh_R3_c_str(sys.executable or ""))
        out.append("")
        if not 目标wasm:
            out.append('#pragma comment(lib, "kernel32.lib")')
            out.append('#pragma comment(lib, "user32.lib")')
            out.append('#pragma comment(lib, "shell32.lib")')
        out.append(Mxh_R1_RUNTIME)
        out.append("")
        for sig in self.funcs:
            ret = C_TYPE[sig.ret] if sig.ret else "void"
            params = ", ".join(f"{C_TYPE[t]} a{i}" for i, (_, t) in enumerate(sig.params)) or "void"
            if sig.extern:
                out.append(f"extern {ret} {sig.cname}({params});")
            else:
                out.append(f"static {ret} {sig.cname}({params});")
        out.append("")
        for sig in self.funcs:
            entry = self.func_bodies.get(sig.cname)
            if entry is None:
                continue
            _, params, body = entry
            ret = C_TYPE[sig.ret] if sig.ret else "void"
            out.append(f"static {ret} {sig.cname}({params}) {{")
            if sig.ret and not any("return" in ln for ln in body):
                if sig.ret in ("int", "bool"):
                    default_val = "0"
                elif sig.ret == "double":
                    default_val = "0.0"
                else:
                    default_val = '""'
                out.append("    return " + default_val + ";")
            out.extend(body)
            out.append("}")
            out.append("")
        out.append("int main(void) {")
        out.append("    zhc_init_args();")
        out.append("    SetConsoleOutputCP(65001);")
        out.append("    SetConsoleCP(65001);")
        out.extend(self.lines)
        out.append("    return 0;")
        out.append("}")
        return "\n".join(out)


def Mxh_R3_c_string(text):
    """把中文按 UTF-8 逐字节转成 C 转义串，规避编码差异。"""
    data = text.encode("utf-8")
    body = "".join(f"\\x{b:02x}" for b in data)
    return f'"{body}"'


# ---------------------------------------------------------------- 驱动

def Mxh_R3_find_vcvars():
    cands = [
        r"C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat",
        r"C:\Program Files\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat",
        r"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat",
        r"C:\Program Files\Microsoft Visual Studio\2022\Professional\VC\Auxiliary\Build\vcvars64.bat",
        r"C:\Program Files\Microsoft Visual Studio\2022\Enterprise\VC\Auxiliary\Build\vcvars64.bat",
    ]
    for p in cands:
        if os.path.isfile(p):
            return p
    return None


def Mxh_原子落盘(源文件, 目标路径):
    """把源文件落到目标路径：先写同目录临时名，再 os.replace 原子换名。

    R-E 原子落盘：构建或复制中途失败时，目标路径上要么仍是旧产物、要么是完整新产物，
    不会留下半截文件被下游当成有效产物。临时名残留由本函数自身清理。
    """
    import shutil
    目标 = os.path.abspath(目标路径)
    目录 = os.path.dirname(目标)
    if 目录:
        os.makedirs(目录, exist_ok=True)
    临时 = 目标 + ".zhc_tmp"
    try:
        shutil.copy(源文件, 临时)
        os.replace(临时, 目标)
    except OSError:
        try:
            if os.path.isfile(临时):
                os.remove(临时)
        except OSError:
            pass
        raise


def Mxh_R3_build(c_path, exe_path):
    """在 ASCII 临时目录中调用 cl 构建，规避中文路径与 cmd 引号转义问题。"""
    import tempfile
    import hashlib
    import shutil

    vcvars = Mxh_R3_find_vcvars()
    if not vcvars:
        raise Mxh_K4_编译错误("[E901] 未找到 vcvars64.bat，请安装 Visual Studio Build Tools（或先设置 VSCMD 环境）",
                     码="E901", 行=0, 列=0, 类别="构建")

    tag = hashlib.md5(os.path.abspath(exe_path).encode("utf-8")).hexdigest()[:10]
    work = os.path.join(tempfile.gettempdir(), "zhc_build", tag)
    os.makedirs(work, exist_ok=True)

    shutil.copy(c_path, os.path.join(work, "prog.c"))
    bat = os.path.join(work, "build.bat")
    with open(bat, "w", encoding="mbcs", errors="replace") as f:
        f.write("@echo off\r\n")
        f.write(f'call "{vcvars}" >nul 2>&1\r\n')
        f.write(f'cd /d "{work}"\r\n')
        # R-C 确定性可复现：/Brepro 让链接器用内容哈希取代 PE 头里的时间戳与 PDB GUID，
        # 同一份 C 连编两次产物字节一致（否则每次构建哈希都漂移，产物完整性无从校验）。
        # VS2015 及更早不认识该开关，失败不留 prog.exe，自动回退为普通构建。
        f.write("del prog.exe >nul 2>&1\r\n")
        f.write("cl /nologo /utf-8 /O2 /Brepro prog.c /Fe:prog.exe /link /Brepro /SUBSYSTEM:CONSOLE\r\n")
        f.write("if not exist prog.exe (\r\n")
        f.write("echo [zhc] 当前工具链不支持 /Brepro，已回退普通构建（产物哈希不可复现）\r\n")
        f.write("cl /nologo /utf-8 /O2 prog.c /Fe:prog.exe /link /SUBSYSTEM:CONSOLE\r\n")
        f.write(")\r\n")

    try:
        r = subprocess.run([bat], capture_output=True, text=True, encoding="mbcs",
                           errors="replace", timeout=ZHC_构建限时)
    except subprocess.TimeoutExpired:
        return False, ("[构建失败] cl 超过 %d 秒未结束，已中止（宿主工具链或超大中间码），"
                       "中间 C 已保留：%s" % (ZHC_构建限时, c_path))
    log = (r.stdout or "") + (r.stderr or "")
    out_exe = os.path.join(work, "prog.exe")
    if os.path.isfile(out_exe):
        # 与 build_wasm 对齐：-o 可能指向尚不存在的目录，不先建目录会抛 FileNotFoundError；
        # 落盘走原子路径（R-E），中途失败不留半截 exe。
        try:
            Mxh_原子落盘(out_exe, exe_path)
        except OSError as e:
            return False, ("[构建失败] 无法写入输出文件 %s：%s"
                           "（检查目录权限，或同名文件正被占用）" % (exe_path, e))
        return True, log
    return False, log


def Mxh_R3_find_wasi_sdk():
    """定位 wasi-sdk（含 clang 与 wasi-sysroot）。返回 (clang 路径, sysroot 路径) 或 (None, 缺口说明)。

    查找顺序：环境变量 ZHC_WASI_SDK（指向 wasi-sdk 根目录，或直接指向 bin\clang.exe）
    > D:\ZHC-toolchain\wasi-sdk 下的任意解包目录 > 常见安装位置。
    本函数只读不写，找不到时如实报缺口，不下载、不改 PATH。
    """
    cands = []
    env = os.environ.get("ZHC_WASI_SDK")
    if env:
        cands.append(env)
    for root in (os.environ.get("ZHC_TOOLCHAIN_ROOT"), r"D:\ZHC-toolchain", r"C:\ZHC-toolchain"):
        if not root:
            continue
        pool = os.path.join(root, "wasi-sdk")
        if os.path.isdir(pool):
            try:
                for name in sorted(os.listdir(pool)):
                    cands.append(os.path.join(pool, name))
            except OSError:
                pass
    cands.append(os.path.join(os.path.expanduser("~"), "wasi-sdk"))

    tried = []
    for c in cands:
        if not c:
            continue
        base = c
        if os.path.isfile(base) and base.lower().endswith("clang.exe"):
            base = os.path.dirname(os.path.dirname(base))
        tried.append(base)
        clang = os.path.join(base, "bin", "clang.exe")
        sysroot = os.path.join(base, "share", "wasi-sysroot")
        if os.path.isfile(clang) and os.path.isdir(sysroot):
            return (clang, sysroot)
    return (None, "未找到 wasi-sdk（已查找：" + "；".join(tried) + "）。请设置环境变量 ZHC_WASI_SDK 指向 wasi-sdk 根目录")


def Mxh_R3_find_wasmtime():
    """定位 wasmtime 可执行文件。仅用于 --run 与门禁的行为比对。"""
    cands = []
    env = os.environ.get("ZHC_WASMTIME")
    if env:
        cands.append(env)
    for root in (os.environ.get("ZHC_TOOLCHAIN_ROOT"), r"D:\ZHC-toolchain", r"C:\ZHC-toolchain"):
        if not root:
            continue
        pool = os.path.join(root, "wasmtime")
        if os.path.isdir(pool):
            try:
                for name in sorted(os.listdir(pool)):
                    cands.append(os.path.join(pool, name, "wasmtime.exe"))
            except OSError:
                pass
    for p in cands:
        if p and os.path.isfile(p):
            return p
    return None


def Mxh_R3_build_wasm(c_path, wasm_path):
    """调用 wasi-sdk 的 clang 生成静态链接的 WASI 命令模块（无第三方运行时依赖）。

    与 build() 的差异：不经 cl，也不经 cmd 批处理；clang 直接吃 UTF-8 源码，
    因此不需要 ASCII 临时目录。返回 (是否成功, 日志)。
    """
    clang, sysroot_或缺口 = Mxh_R3_find_wasi_sdk()
    if not clang:
        return False, "[构建失败] wasi-sdk 不可用：" + str(sysroot_或缺口) + "（本项属宿主工具链前置条件，不占用语言错误码）"
    sysroot = sysroot_或缺口
    out_dir = os.path.dirname(os.path.abspath(wasm_path))
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    # 先输出到同目录临时名，成功后再原子换名：clang 中途失败不会在 -o 路径上留半截 wasm（R-E）
    产出 = os.path.abspath(wasm_path) + ".zhc_tmp"
    cmd = [clang, "--target=wasm32-wasip1", "--sysroot=" + sysroot, "-O2",
           "-frandom-seed=zhc",
           "-Wno-unknown-pragmas", "-fno-strict-aliasing",
           "-o", 产出, os.path.abspath(c_path)]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                           errors="replace", timeout=ZHC_构建限时)
    except subprocess.TimeoutExpired:
        return False, ("[构建失败] wasi-sdk clang 超过 %d 秒未结束，已中止（宿主工具链问题，"
                       "不占用语言错误码）" % ZHC_构建限时)
    except OSError as e:
        return False, "[构建失败] 调用 wasi-sdk clang 失败：" + str(e) + "（宿主工具链问题，不占用语言错误码）"
    log = (r.stdout or "") + (r.stderr or "")
    if os.path.isfile(产出) and os.path.getsize(产出) > 0:
        try:
            os.replace(产出, os.path.abspath(wasm_path))
        except OSError as e:
            try:
                os.remove(产出)
            except OSError:
                pass
            return False, ("[构建失败] 无法写入输出文件 %s：%s"
                           "（检查目录权限，或同名文件正被占用）" % (wasm_path, e))
        return True, log
    try:
        if os.path.isfile(产出):
            os.remove(产出)
    except OSError:
        pass
    return False, log or "[构建失败] clang 未产出 wasm 文件（宿主工具链问题，不占用语言错误码）"


def Mxh_R3_find_node():
    """定位 node 可执行文件。仅用于 wasm32-unknown-unknown 目标的 --run（线性内存宿主）。"""
    env = os.environ.get("ZHC_NODE")
    cands = []
    if env:
        cands.append(env)
    try:
        cands.append(shutil.which("node") or "")
    except (OSError, AttributeError):
        pass
    for root in (os.environ.get("ProgramFiles"), os.environ.get("ProgramFiles(x86)"),
                 os.environ.get("LOCALAPPDATA")):
        if root:
            cands.append(os.path.join(root, "nodejs", "node.exe"))
    for p in cands:
        if p and os.path.isfile(p):
            return p
    return None


def Mxh_R3_build_noos(c_path, wasm_path):
    """生成零 WASI import 的 wasm32-unknown-unknown 模块（noos 目标）。

    与 Mxh_R3_build_wasm 的差异：
      1. 不引 wasi-sysroot：中间 C 只 #include "zhc_noos.h"，一个系统头都不碰，
         否则 wasi-libc 会对非 WASI 目标直接 #error；
      2. 中间 C 与 mini-libc 实现 zhc_noos_impl.c 一起编译，链接参数走 --no-entry
         并把 main / memory / zhc_out_* 显式导出给宿主；
      3. clang 在 Windows 上对非 ASCII 路径不稳，整条构建跑在 ASCII 临时目录内，
         产物再经同目录 .zhc_tmp 原子换名落到目标路径（R-E）。
    返回 (是否成功, 日志)。
    """
    clang, sysroot_或缺口 = Mxh_R3_find_wasi_sdk()
    if not clang:
        return False, ("[构建失败] wasi-sdk 的 clang 不可用：" + str(sysroot_或缺口) +
                       "（noos 目标只借 clang，不需要 wasi-sysroot；本项属宿主工具链前置条件，不占用语言错误码）")
    out_dir = os.path.dirname(os.path.abspath(wasm_path))
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    产出 = os.path.abspath(wasm_path) + ".zhc_tmp"
    work = tempfile.mkdtemp(prefix="zhc_noos_build_")
    try:
        # 垫片落地：头 + mini-libc 实现，均来自内核内联常量，不依赖分发包里的散文件
        for 名 in ("zhc_noos.h", "zhc_noos_impl.c"):
            with open(os.path.join(work, 名), "w", encoding="utf-8", newline="\n") as f:
                f.write(Mxh_R2_noos_text(名))
        with open(c_path, "r", encoding="utf-8") as f:
            src = f.read()
        with open(os.path.join(work, "prog.c"), "w", encoding="utf-8", newline="\n") as f:
            f.write(src)
        cmd = [clang, "--target=wasm32-unknown-unknown",
               "-nostdlib", "-ffreestanding", "-fno-builtin", "-fno-strict-aliasing",
               "-O2", "-frandom-seed=zhc", "-Wno-unknown-pragmas",
               "-I.", "-Wl,--no-entry", "-Wl,--export-memory",
               "-Wl,--export=main", "-Wl,--export=zhc_out_ptr",
               "-Wl,--export=zhc_out_len", "-Wl,--export=zhc_out_reset",
               "-Wl,--export=zhc_out_cap",
               "-o", "prog.wasm", "prog.c", "zhc_noos_impl.c"]
        try:
            r = subprocess.run(cmd, cwd=work, capture_output=True, text=True,
                               encoding="utf-8", errors="replace", timeout=ZHC_构建限时)
        except subprocess.TimeoutExpired:
            return False, ("[构建失败] noos 构建超过 %d 秒未结束，已中止（宿主工具链问题，"
                           "不占用语言错误码）" % ZHC_构建限时)
        log = (r.stdout or "") + (r.stderr or "")
        产物 = os.path.join(work, "prog.wasm")
        if os.path.isfile(产物) and os.path.getsize(产物) > 0:
            try:
                shutil.copyfile(产物, 产出)
                os.replace(产出, os.path.abspath(wasm_path))
            except OSError as e:
                try:
                    os.remove(产出)
                except OSError:
                    pass
                return False, ("[构建失败] 无法写入输出文件 %s：%s"
                               "（检查目录权限，或同名文件正被占用）" % (wasm_path, e))
            return True, log
        return False, log or "[构建失败] clang 未产出 wasm 文件（宿主工具链问题，不占用语言错误码）"
    except OSError as e:
        return False, "[构建失败] 调用 wasi-sdk clang 失败：" + str(e) + "（宿主工具链问题，不占用语言错误码）"
    finally:
        shutil.rmtree(work, ignore_errors=True)


def Mxh_R3_run_noos(node, wasm_path, 限时):
    """用 node 宿主加载 noos 模块并运行，返回 (状态, 码)。

    宿主脚本 run_noos.js 同样来自内联常量：落临时文件 → node 执行 → 清理，
    用完即删，不往用户目录留任何加载器残留。
    """
    work = tempfile.mkdtemp(prefix="zhc_noos_run_")
    try:
        loader = os.path.join(work, "run_noos.js")
        with open(loader, "w", encoding="utf-8", newline="\n") as f:
            f.write(Mxh_R2_noos_text("run_noos.js"))
        return Mxh_R4_限时运行([node, loader, os.path.abspath(wasm_path)], 限时)
    finally:
        shutil.rmtree(work, ignore_errors=True)


def Mxh_R4_杀进程树(pid):
    """按进程树强制结束。超时程序可能是 cmd/cl 的子孙进程，只 kill 直接子进程会留孤儿。"""
    if os.name == "nt":
        try:
            subprocess.run(["taskkill", "/F", "/T", "/PID", str(pid)],
                           capture_output=True, timeout=15)
        except (subprocess.TimeoutExpired, OSError):
            # 强杀失败也不阻断上层：上层随后 p.wait(5) 会再确认一次
            pass
    else:
        try:
            os.kill(pid, 9)
        except OSError:
            pass


def Mxh_R4_限时运行(cmd, 限时=20):
    """运行外部可执行文件，超时按进程树强杀。

    不用管道捕获输出：死循环程序会一直持有管道写端，一旦父进程被杀就会变成孤儿进程
    继续运行（实测可持续写盘数 MB）。让输出直接继承终端，wait 只等待进程本身，
    并在超时后 taskkill /T 连同子孙一并结束。
    """
    旗 = getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)
    p = subprocess.Popen(cmd, stdin=subprocess.DEVNULL, creationflags=旗)
    try:
        p.wait(timeout=限时)
    except subprocess.TimeoutExpired:
        Mxh_R4_杀进程树(p.pid)
        try:
            p.wait(timeout=5)
        except subprocess.TimeoutExpired:
            pass
        # taskkill 后若进程仍未退净，returncode 为 None；此处兜底成 -1，
        # 避免上层 "码 & 0xFFFFFFFF" 对 None 取位运算而抛 TypeError
        return "超时", (p.returncode if p.returncode is not None else -1)
    return "结束", p.returncode


def main():
    ap = argparse.ArgumentParser(description="zhc 纯中文编程语言编译器（x86-64 / wasm32-wasip1 / wasm32-unknown-unknown）")
    ap.add_argument("source", nargs="?", help="中文源码文件（.zc）")
    ap.add_argument("-o", "--output", default=None, help="输出 exe 路径")
    ap.add_argument("--emit-c", action="store_true", help="仅输出中间 C 代码")
    ap.add_argument("--run", action="store_true", help="编译后立即运行")
    ap.add_argument("--运行限时", type=int, default=20, dest="运行限时",
                    help="--run 时生成程序的最长运行秒数，超时按进程树强制终止（默认 20）")
    ap.add_argument("--keep-c", action="store_true", help="保留中间 C 文件")
    ap.add_argument("--api", action="store_true", help="打印系统级类型与内置函数手册")
    ap.add_argument("--关于", "--about", action="store_true", dest="关于",
                    help="打印版本、著作权与制作说明（产品身份的唯一声明位置）")
    ap.add_argument("--版本", "--version", action="store_true", dest="版本",
                    help="只打印版本号")
    ap.add_argument("--诊断", action="store_true", dest="诊断",
                    help="只做词法与语法检查，以 JSON 输出诊断（供编辑器/LSP 使用）")
    ap.add_argument("--target", default="auto",
                    choices=["auto", "x86-64", "wasm32-wasi", "wasm32-unknown-unknown"],
                    help="生成目标：auto（默认，按 -o 后缀推断：.wasm 走 wasm32-wasi，其余 x86-64）、"
                         "x86-64（cl 链接为 exe）、wasm32-wasi（wasi-sdk clang 生成静态链接 .wasm）或 "
                         "wasm32-unknown-unknown（零 WASI import 的纯计算子集，无文件 I/O，输出经线性内存交给 node 宿主）")
    args = ap.parse_args()

    if args.版本:
        print("ZHC-LANG " + ZHC_版本 + "（语言契约 " + ZHC_契约版 + "）")
        return 0
    if args.关于:
        print(ZHC_关于)
        return 0
    if args.api:
        print(api_manual())
        return 0
    if not args.source:
        ap.error("需要提供源码文件，或使用 --api 查看内置 API 手册")

    # utf-8-sig：自动吞掉 UTF-8 BOM（记事本/部分编辑器默认写入），避免首字符报非法
    with open(args.source, "r", encoding="utf-8-sig") as f:
        src = f.read()

    目标 = args.target
    if 目标 == "auto":
        后缀 = os.path.splitext(args.output or args.source)[1].lower()
        目标 = "wasm32-wasi" if 后缀 == ".wasm" else "x86-64"

    try:
        tokens = Mxh_K1_Lexer(src).run()
        c_code = Mxh_K0_Compiler(tokens, target=目标).compile()
    except Mxh_K4_编译错误 as e:
        if args.诊断:
            # 结构化诊断：码/行/列/期望/实际 供 LSP 与智能体直接取用，消息键保留原措辞
            print(json.dumps({"ok": False, **e.转字典()}, ensure_ascii=False))
            return 1
        print(f"[编译失败] {e}", file=sys.stderr)
        return 1

    if args.诊断:
        print(json.dumps({"ok": True, "消息": "", "码": None, "行": None, "列": None,
                          "期望": None, "实际": None, "类别": None}, ensure_ascii=False))
        return 0

    if args.emit_c:
        print(c_code)
        return 0

    base = os.path.splitext(os.path.abspath(args.source))[0]
    c_path = base + ".gen.c"
    exe_path = os.path.abspath(args.output or (base + ".exe"))
    with open(c_path, "w", encoding="utf-8") as f:
        f.write(c_code)

    if 目标 == "wasm32-unknown-unknown":
        ok, log = Mxh_R3_build_noos(c_path, exe_path)
    elif 目标 == "wasm32-wasi":
        ok, log = Mxh_R3_build_wasm(c_path, exe_path)
    else:
        ok, log = Mxh_R3_build(c_path, exe_path)
    if not ok:
        print("[本地构建失败] 中间 C 代码已保留，便于定位：", c_path, file=sys.stderr)
        print(log, file=sys.stderr)
        return 2
    if not args.keep_c and os.path.isfile(c_path):
        os.remove(c_path)
    print(f"[编译成功] {exe_path}" + (f"（目标 {目标}）" if 目标 != "x86-64" else ""))

    if args.run:
        if 目标 == "wasm32-unknown-unknown":
            node = Mxh_R3_find_node()
            if not node:
                print("[运行失败] 目标 wasm32-unknown-unknown 需要 node 宿主：未找到（可设置环境变量 ZHC_NODE）",
                      file=sys.stderr)
                return 1
            状态, 码 = Mxh_R3_run_noos(node, exe_path, args.运行限时)
        elif 目标 == "wasm32-wasi":
            wasmtime = Mxh_R3_find_wasmtime()
            if not wasmtime:
                print("[运行失败] 目标 wasm32-wasi 需要 wasmtime：未找到（可设置环境变量 ZHC_WASMTIME）",
                      file=sys.stderr)
                return 1
            状态, 码 = Mxh_R4_限时运行([wasmtime, "run", "--", exe_path], args.运行限时)
        else:
            状态, 码 = Mxh_R4_限时运行([exe_path], args.运行限时)
        if 状态 == "超时":
            print(f"[运行超时] 程序 {args.运行限时} 秒未结束，已按进程树强制终止"
                  f"（疑似死循环：当 条件 恒为真，或循环里漏写自增）", flush=True)
            return 1
        if 码 != 0:
            码值 = 码 if isinstance(码, int) else -1
            print(f"[运行崩溃] 程序返回码 {码值}"
                  f"（0x{码值 & 0xFFFFFFFF:08X}）", flush=True)
            return 1
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Mxh_K4_编译错误 as e:
        print(str(e), file=sys.stderr, flush=True)
        sys.exit(2)
    except KeyboardInterrupt:
        print("[已中断] 用户取消", file=sys.stderr, flush=True)
        sys.exit(130)
    except OSError as e:
        print("[运行环境错误] " + str(e), file=sys.stderr, flush=True)
        sys.exit(3)
