#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
hekouwang-claude-skill-doctor-skill · Agent Skill 体检器（确定性机检层）
会勇禾口王的AI笔记 · @huiyonghkw —— 不聊 AI 会不会取代你，只聊先用 AI 的人怎么取代你。

零依赖（仅用 Python3 标准库）。对一个 Skill 目录里的 SKILL.md 做启发式检查，
按"按需加载的指令包，不是单文件巨石"的最佳实践打分，输出可读报告 + 修复线索。

核心判据一句话——
    SKILL.md 是模型"决定要不要加载、加载后照着做"的运行时指令包。
    description 决定它何时被唤醒；正文越精简越准；厚重细节要能"按需展开"
    （references/ 用到再读），而不是每次触发就全量进上下文。

用法:
    python3 check.py [skill目录]          # 默认当前目录；目录里要有 SKILL.md
    python3 check.py [skill目录] --json    # 机器可读 JSON
    python3 check.py [skill目录] --profile codex  # 叠加 Codex 严格基础契约
    python3 check.py --scan [skill根目录]  # 递归盘点多个 Skill、软链和重名
    python3 check.py --scan --direct [宿主根目录]  # 只盘点当前宿主直接入口
    python3 check.py --scan [skill根目录] --profile codex  # 批量执行 Codex Profile

退出码: 有 FAIL → 1，否则 0。

注意: 本脚本只做"机器能确定的部分"。description 触发质量、正文是不是"图书馆"、
是不是在替模型补它已会的知识——这些需人/模型读正文定夺，交给 SKILL.md 的定性复核。
默认跳过受保护文件名；入口文件若为越界软链则拒绝读取，不跟随到 skill 根外。
"""

import os
import re
import sys
import json
import glob as _glob
import argparse

DOCTOR_VERSION = "1.8.1"
REPORT_SCHEMA_VERSION = 3

# ---------- 终端着色 ----------
_TTY = sys.stdout.isatty()
def _c(code, s):
    return f"\033[{code}m{s}\033[0m" if _TTY else s
def bold(s):  return _c("1", s)
def dim(s):   return _c("2", s)
def green(s): return _c("32", s)
def yellow(s):return _c("33", s)
def red(s):   return _c("31", s)
def cyan(s):  return _c("36", s)

ICON = {"PASS": "✓", "WARN": "▲", "FAIL": "✗", "INFO": "·"}
COLOR = {"PASS": green, "WARN": yellow, "FAIL": red, "INFO": cyan}
WEIGHT = {"PASS": 1.0, "WARN": 0.5, "FAIL": 0.0}  # INFO 不计分

# ---------- 各检查项重要度权重（"减法优先 + 触发优先"）----------
# Skill 的命脉是两条：① description 让它在对的时候被唤醒；② 正文越精简、按需加载越准。
# 所以"触发质量 / 篇幅 / 渐进披露 / 可移植 / 别替模型补"权重拉满；
# "加内容"类（最小工具集、配套文档）缺了只算小扣分，别逼作者把 skill 做臃肿。
IMPORTANCE = {
    "secret": 1.5,                                   # 正文硬编码密钥 = 资损级（skill 常被分发）
    "frontmatter": 1.5, "trigger": 1.5, "length": 1.5,
    "disclosure": 1.5, "portable": 1.5, "noteach": 1.5,
    "pointers": 1.0, "scripts": 1.0, "desclen": 1.0,
    "pathscope": 1.0, "openclaw": 0.6,
    "tools": 0.6, "companion": 0.6, "readability": 1.0,
    "invocation": 0.6, "identity": 0.6, "codex": 1.5,
}

IGNORE_DIRS = {
    ".git", "node_modules", "vendor", "dist", "build", "__pycache__",
    ".venv", "venv", ".idea", ".vscode", ".cache",
}

TEXT_EXTENSIONS = (
    ".md", ".py", ".sh", ".bash", ".zsh", ".js", ".mjs", ".cjs",
    ".json", ".txt", ".yaml", ".yml", ".html", ".htm", ".css",
    ".ts", ".tsx", ".jsx", ".toml", ".xml", ".sql", ".rb", ".go",
    ".rs", ".java",
)

# 标准 frontmatter 字段（Anthropic Agent Skills 认得的）。其余字段无害但冗余（runtime 不读）。
STANDARD_FM_KEYS = {
    "name", "description", "allowed-tools", "license", "metadata",
    "paths", "globs", "requires", "install", "disable-model-invocation",
}

# Codex skill-creator 的严格入口契约。它与默认 Agent Profile 分开，
# 因为 Claude/跨宿主 Skill 合法地可能带 slug、version 或运行时扩展字段。
CODEX_FM_KEYS = {"name", "description", "license", "allowed-tools", "metadata"}
PROFILES = {"agent", "codex"}

# ---------- description 里的"何时用/触发"信号（#2 的判据）----------
# description 必须回答两问：做什么 + 何时用。只写"做什么"会让模型不知道何时唤醒。
WHEN_SIGNALS = [
    "当需要", "当你", "当用户", "需要", "用于", "适用于", "触发", "想要", "要做",
    "在.*时", "use when", "use this when", "when you", "when the user",
    "when asked", "for when", "helps you", "to .*ing", "invoke", "trigger",
]

# ---------- 教学型措辞（#10：替模型补它"已经会"的通用知识 = 随模型升级很快过时）----------
TEACHING = [
    "使用教程", "入门教程", "新手教程", "如何使用", "怎么用", "怎样使用",
    "step by step", "step-by-step", "follow these steps", "how to use",
    "getting started tutorial", "基础语法", "语言入门",
]

# ---------- 硬编码绝对路径（#6 可移植性：别人装了就废）----------
# ~ / $HOME / ${HOME} 是可移植的；家目录绝对路径才是踩坑。正则用拼接避免自检误报。
_ABS_HOME = "/" + "Users" + r"/[^/\s'\"`)]+|" + "/home/" + r"[^/\s'\"`)]+|"
_ABS_WIN = r"[A-Za-z]:\\Users\\[^\\\s'\"`)]+"
ABS_PATH_RE = re.compile(r"(?<![\w~])(" + _ABS_HOME + _ABS_WIN + r")")

# ---------- 密钥指纹（正文里出现 = 资损级，直接 FAIL）----------
SECRET_PATTERNS = [
    ("私钥块",        re.compile(r"-----BEGIN (?:RSA |EC |DSA |OPENSSH |PGP )?PRIVATE KEY-----")),
    # \b 不可省：没有左词界时 `generate-ask-user-format` 里的 `ask-user-format` 会被当成 sk- 密钥
    ("OpenAI/Anthropic key", re.compile(r"\bsk-(?:ant-)?[A-Za-z0-9_\-]{20,}")),
    ("AWS Access Key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("Google API key", re.compile(r"\bAIza[0-9A-Za-z_\-]{35}\b")),
    ("GitHub token",   re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{36}\b|\bgithub_pat_[A-Za-z0-9_]{60,}")),
    ("Slack token",    re.compile(r"\bxox[baprs]-[A-Za-z0-9\-]{10,}")),
    ("JWT",            re.compile(r"\beyJ[A-Za-z0-9_\-]{10,}\.eyJ[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}")),
    ("硬编码口令/密钥赋值", re.compile(
        r"(?i)\b(?:password|passwd|pwd|secret|api[_\-]?key|access[_\-]?key|auth[_\-]?token|client[_\-]?secret)\b"
        r"\s*[:=]\s*['\"]([^'\"\s]{6,})['\"]")),
]
# 测试夹具目录：安全基准/回归夹具里的假密钥是刻意载荷，判 FAIL 会让红线失去意义（降级为 WARN）
FIXTURE_DIRS = {"test", "tests", "__tests__", "spec", "specs",
                "fixture", "fixtures", "snapshot", "snapshots", "golden"}
SCAN_IGNORE_DIRS = IGNORE_DIRS | FIXTURE_DIRS

PLACEHOLDER_RE = re.compile(
    r"(?i)(x{3,}|y{3,}|your[_\-]?|<[^>]*>|\$\{|\benv\b|process\.env|os\.environ|"
    r"example|changeme|placeholder|redacted|todo|n/a|\.\.\.|…|abc123|123456|test|dummy|sample)")
FILLER_RE = re.compile(r"(?i)(x{4,}|y{4,}|your|<|>|\.\.\.|…|example|placeholder|redacted|dummy|sample)")


def _redact(s):
    s = s.strip()
    if len(s) <= 8:
        return s[:2] + "***"
    return s[:4] + "***" + f"({len(s)} 字符)"


# ====================== 解析 ======================

def find_skill_md(root):
    p = os.path.join(root, "SKILL.md")
    if not os.path.isfile(p):
        return None
    root_real = os.path.realpath(root)
    real = os.path.realpath(p)
    if not (real == root_real or real.startswith(root_real + os.sep)):
        return None
    return p


def _split_yaml_items(value):
    """拆分行内 YAML list/dict，忽略引号和嵌套括号里的逗号。"""
    items, start, quote, depth = [], 0, None, 0
    for i, ch in enumerate(value):
        if quote:
            if ch == quote and (i == 0 or value[i - 1] != "\\"):
                quote = None
            continue
        if ch in ("'", '"'):
            quote = ch
        elif ch in "[{":
            depth += 1
        elif ch in "]}":
            depth = max(0, depth - 1)
        elif ch == "," and depth == 0:
            items.append(value[start:i].strip())
            start = i + 1
    items.append(value[start:].strip())
    return [item for item in items if item]


def _yaml_scalar_error(value):
    value = value.strip()
    if not value:
        return ""
    if value[0] in ("'", '"') and (len(value) < 2 or value[-1] != value[0]):
        return "引号未闭合"
    if value.startswith("[") and not value.endswith("]"):
        return "行内 list 未闭合"
    if value.startswith("{") and not value.endswith("}"):
        return "行内 mapping 未闭合"
    return ""


def _parse_yaml_scalar(value):
    """解析检查器需要的 YAML 标量子集；不引入第三方 YAML 依赖。"""
    value = value.strip()
    if not value:
        return ""
    if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
        return value[1:-1]
    lower = value.lower()
    if lower in ("true", "yes", "on"):
        return True
    if lower in ("false", "no", "off"):
        return False
    if lower in ("null", "~"):
        return None
    if value.startswith("[") and value.endswith("]"):
        return [_parse_yaml_scalar(item) for item in _split_yaml_items(value[1:-1])]
    if value.startswith("{") and value.endswith("}"):
        mapping = {}
        for item in _split_yaml_items(value[1:-1]):
            if ":" not in item:
                continue
            key, item_value = item.split(":", 1)
            mapping[key.strip().strip("'\"")] = _parse_yaml_scalar(item_value)
        return mapping
    return value


def _collect_flow_value(lines, start):
    """收集跨行的 flow mapping/list，返回 (拼接值, 下一行索引)。"""
    chunks = []
    depth = 0
    quote = None
    escaped = False
    started = False
    for index in range(start, len(lines)):
        line = lines[index]
        chunks.append(line.strip())
        for ch in line:
            if quote:
                if escaped:
                    escaped = False
                elif ch == "\\":
                    escaped = True
                elif ch == quote:
                    quote = None
                continue
            if ch in ("'", '"'):
                quote = ch
            elif ch in "[{":
                depth += 1
                started = True
            elif ch in "]}":
                depth -= 1
                if depth < 0:
                    return None, index + 1
        if started and depth == 0 and quote is None:
            return " ".join(chunks), index + 1
    return None, len(lines)


def _parse_yaml_mapping(text):
    """解析 frontmatter / openai.yaml 所需的缩进 mapping/list 子集。

    这是有意收窄的零依赖解析器：遇到无法确定的 YAML 语法会返回错误，
    不会把 malformed 配置静默当成空配置。
    """
    lines = text.splitlines()
    root = {}
    errors = []
    stack = [(-1, root)]
    key_re = re.compile(r"^([A-Za-z_][\w.-]*):(?:[ \t]*(.*))?$")
    i = 0
    while i < len(lines):
        raw = lines[i]
        if not raw.strip() or raw.lstrip().startswith("#"):
            i += 1
            continue
        if raw.startswith("\t"):
            errors.append(f"L{i + 1}: 不支持 tab 缩进")
            i += 1
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        while len(stack) > 1 and indent <= stack[-1][0]:
            stack.pop()
        parent = stack[-1][1]
        content = raw[indent:]

        if content.startswith("- "):
            if not isinstance(parent, list):
                errors.append(f"L{i + 1}: list 项没有对应的 list 字段")
            else:
                parent.append(_parse_yaml_scalar(content[2:].strip()))
            i += 1
            continue

        match = key_re.match(content)
        if not match:
            errors.append(f"L{i + 1}: 无法解析 YAML 字段")
            i += 1
            continue
        key, value = match.group(1), (match.group(2) or "").strip()
        if not isinstance(parent, dict):
            errors.append(f"L{i + 1}: mapping 字段没有对应的对象")
            i += 1
            continue
        if key in parent:
            errors.append(f"L{i + 1}: 重复字段 {key}")
            i += 1
            continue

        if value in ("|", "|-", "|+", ">", ">-", ">+"):
            block, j = [], i + 1
            while j < len(lines):
                candidate = lines[j]
                candidate_indent = len(candidate) - len(candidate.lstrip(" "))
                if candidate.strip() and candidate_indent <= indent:
                    break
                block.append(candidate)
                j += 1
            nonempty = [
                len(line) - len(line.lstrip(" "))
                for line in block if line.strip()
            ]
            base = min(nonempty) if nonempty else indent + 1
            normalized = [
                "" if not line.strip() else line[base:]
                for line in block
            ]
            if value.startswith(">"):
                parent[key] = " ".join(part.strip() for part in normalized if part.strip())
            else:
                parent[key] = "\n".join(normalized).rstrip("\n")
            i = j
            continue

        if value:
            scalar_error = _yaml_scalar_error(value)
            if scalar_error:
                errors.append(f"L{i + 1}: {scalar_error}")
            parent[key] = _parse_yaml_scalar(value)
            i += 1
            continue

        # 空值后面的第一行决定它是 mapping 还是 list；否则保留为空字符串。
        j = i + 1
        while j < len(lines) and not lines[j].strip():
            j += 1
        if j < len(lines):
            next_line = lines[j]
            next_indent = len(next_line) - len(next_line.lstrip(" "))
            if next_indent > indent:
                next_content = next_line[next_indent:]
                if next_content.startswith(("{", "[")):
                    flow_value, next_index = _collect_flow_value(lines, j)
                    if flow_value is None:
                        errors.append(f"L{j + 1}: 跨行 flow mapping/list 未闭合")
                    else:
                        parent[key] = _parse_yaml_scalar(flow_value)
                    i = next_index
                    continue
                child = [] if next_line[next_indent:].startswith("- ") else {}
                parent[key] = child
                stack.append((indent, child))
                i += 1
                continue
        parent[key] = ""
        i += 1
    return root, errors


def parse_frontmatter(text):
    """返回 (dict, raw_fm_text, body_text, body_offset, errors)。"""
    if text.startswith("\ufeff"):
        text = text[1:]
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, "", text, 0, ["缺少 frontmatter 起始分隔线 ---"]
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return {}, "", text, 0, ["缺少 frontmatter 结束分隔线 ---"]
    fm_lines = lines[1:end]
    body = "\n".join(lines[end + 1:])
    data, errors = _parse_yaml_mapping("\n".join(fm_lines))
    return data, "\n".join(fm_lines), body, end + 1, errors


def analyze_body(body, line_offset=0):
    """逐行分析正文，返回结构信息。line_offset：正文前的行数，用于把行号还原成文件绝对行号。"""
    lines = body.splitlines()
    info = {
        "lines": len(lines),
        "chars": len(body),
        "fences": 0,
        "code_lines": 0,
        "max_code_block": 0,
        "headings": [],
        "ref_pointers": [],   # [(path, line_no)]
    }
    in_code = False
    cur = 0
    resource = (
        r"(?:references?|scripts?|assets?|examples?|templates?)/"
        r"[A-Za-z0-9._*?{}\-/]+\.(?:md|py|sh|js|mjs|cjs|json|html|htm|yaml|yml|"
        r"txt|css|ts|tsx|jsx|toml|xml|svg|png|jpg|jpeg|webp|woff2|ttf|otf)"
        r"(?![A-Za-z0-9_\-])"  # 交替按顺序试，没有边界时 .json 会只匹配到 .js
    )
    # 只认 Markdown link destination 或明确的 doctor:resource；
    # 不把任意 prose/code 示例当指针，避免把目录树和教学示例误报成死链。
    md_link_re = re.compile(r"\]\(\s*<?(?P<path>" + resource + r")(?:[?#][^)\s>]*)?>?")
    explicit_re = re.compile(r"(?:doctor:resource|skill-doctor:resource)\s+(?P<path>" + resource + r")")

    def clean_pointer(path):
        path = path.strip("<>\"'")
        path = path.split("#", 1)[0].split("?", 1)[0]
        return path.rstrip(".,;:!?")
    for i, ln in enumerate(lines):
        st = ln.strip()
        if st.startswith("```"):
            if not in_code:
                in_code, cur = True, 0
            else:
                info["max_code_block"] = max(info["max_code_block"], cur)
                in_code = False
            info["fences"] += 1
            continue
        if in_code:
            cur += 1
            info["code_lines"] += 1
            continue
        if st.startswith("#"):
            info["headings"].append(st.lstrip("#").strip())
        seen = set()
        for pattern in (md_link_re, explicit_re):
            for m in pattern.finditer(ln):
                path = clean_pointer(m.group("path"))
                if path and path not in seen:
                    seen.add(path)
                    info["ref_pointers"].append((path, i + 1 + line_offset))
    return info


def unfinished_todo_lines(body, line_offset=0):
    """返回正文中不在代码围栏内的未完成 TODO 占位符行号。"""
    todo_lines = []
    fence_marker = None
    fence_length = 0
    fence_re = re.compile(r"^[ \t]*(?:(?:[-+*]|\d+[.)])[ \t]+)?(`{3,}|~{3,})(.*)$")
    todo_re = re.compile(r"[ ]{0,3}\[TODO:[^\n]*\][ \t]*$")
    for index, line in enumerate(body.splitlines()):
        fence = fence_re.match(line)
        if fence:
            marker = fence.group(1)
            if fence_marker is None:
                fence_marker = marker[0]
                fence_length = len(marker)
            elif (marker[0] == fence_marker and len(marker) >= fence_length
                  and not fence.group(2).strip()):
                fence_marker = None
                fence_length = 0
            continue
        if fence_marker is None and todo_re.fullmatch(line):
            todo_lines.append(index + 1 + line_offset)
    return todo_lines


def _path_inside_root(root, path):
    root_real = os.path.realpath(root)
    real = os.path.realpath(path)
    return real == root_real or real.startswith(root_real + os.sep)


def _read_text_inside(root, path):
    """只读 skill 根内普通文件；拒绝越界软链与受保护文件名。"""
    if os.path.islink(path) and not _path_inside_root(root, path):
        raise OSError("refuses symlink outside skill root")
    if not _path_inside_root(root, path):
        raise OSError("refuses path outside skill root")
    target = os.path.realpath(path)
    if _protected_filename(target) or _protected_filename(path):
        raise OSError("refuses protected filename")
    with open(path, encoding="utf-8", errors="replace") as fh:
        return fh.read()


def list_skill_files(root):
    """返回 skill 目录里的相关文件（剔除 .git 等）。

    不跟随软链目录；越界或命中受保护文件名的软链跳过。
    """
    out = []
    root = os.path.abspath(root)
    for cur, dirs, files in os.walk(root, followlinks=False):
        # 不再按「. 开头」一刀切：.openclaw/.cursor/.agents 可能是宿主契约；
        # 只剔除明确的仓库/构建目录。
        dirs[:] = [
            d for d in dirs
            if d not in IGNORE_DIRS and not os.path.islink(os.path.join(cur, d))
        ]
        for f in files:
            full = os.path.join(cur, f)
            rel = os.path.relpath(full, root)
            if os.path.islink(full):
                if not _path_inside_root(root, full):
                    continue
                if _protected_filename(os.path.realpath(full)) or _protected_filename(rel):
                    continue
            elif _protected_filename(rel):
                continue
            out.append(rel)
    return out


def reference_files(allfiles):
    """正文之外、用于'渐进披露'的参考/资源文件。"""
    refs = []
    for rel in allfiles:
        low = rel.lower()
        base = os.path.basename(low)
        if base in ("skill.md", "readme.md", "readme.en.md", "changelog.md",
                    "contributing.md", "license", "license.md", ".gitignore", ".ds_store"):
            continue
        top = rel.split(os.sep)[0].lower()
        if top in ("references", "reference", "scripts", "assets", "examples", "templates"):
            refs.append(rel)
        elif low.endswith(".md"):           # 散落在根的额外 .md 也算下沉文件
            refs.append(rel)
    return refs


# ====================== 检查 ======================

def in_test_fixture(rel):
    parts = rel.replace("\\", "/").lower().split("/")
    return any(p in FIXTURE_DIRS for p in parts[:-1])


def _protected_filename(rel):
    """密钥文件永远不打开：扩展名规则 + 名称规则双保险。"""
    base = os.path.basename(rel).lower()
    return (
        base == ".env" or base.startswith(".env.") or
        base.endswith((".key", ".pem")) or "secret" in base
    )


def scan_secret_and_paths(root, allfiles):
    """扫描文本文件，并返回 (secret_hits, path_hits, read_errors)。"""
    secret_hits, path_hits, read_errors = [], [], []
    targets = [
        f for f in allfiles
        if f.lower().endswith(TEXT_EXTENSIONS) and not _protected_filename(f)
    ]
    for rel in targets:
        p = os.path.join(root, rel)
        if os.path.islink(p) and (
            not _path_inside_root(root, p)
            or _protected_filename(os.path.realpath(p))
        ):
            continue
        if not _path_inside_root(root, p):
            continue
        try:
            with open(p, encoding="utf-8", errors="replace") as fh:
                text = fh.read()
        except OSError as exc:
            read_errors.append((rel, type(exc).__name__))
            continue
        for label, pat in SECRET_PATTERNS:
            for m in pat.finditer(text):
                frag = m.group(0)
                if m.groups() and m.lastindex:
                    if PLACEHOLDER_RE.search(m.group(1)):
                        continue
                    val = m.group(1)
                else:
                    if FILLER_RE.search(frag):
                        continue
                    val = frag
                ln_no = text[:m.start()].count("\n") + 1
                secret_hits.append((rel, ln_no, label, _redact(val)))
        for m in ABS_PATH_RE.finditer(text):
            frag = m.group(1)
            if "某人" in frag or frag.endswith("..."):
                continue
            ln_no = text[:m.start()].count("\n") + 1
            if in_test_fixture(rel):
                continue
            line = text.splitlines()[ln_no - 1] if ln_no <= len(text.splitlines()) else ""
            if os.path.basename(p) == "check.py" and ("ABS_PATH" in line or "家目录" in line or "Users/..." in line):
                continue
            path_hits.append((rel, ln_no, frag))
    return secret_hits, path_hits, read_errors


def _path_inside(root_real, candidate):
    try:
        return os.path.commonpath([root_real, candidate]) == root_real
    except ValueError:
        return False


def _brace_expand(pattern):
    """提供 glob 没有的最小 brace expansion，避免把 {a,b} 静默跳过。"""
    match = re.search(r"\{([^{}]+)\}", pattern)
    if not match:
        return [pattern]
    choices = match.group(1).split(",")
    expanded = []
    for choice in choices:
        expanded.extend(_brace_expand(
            pattern[:match.start()] + choice + pattern[match.end():]
        ))
    return expanded


def _resolve_pointer(root, path):
    """返回 (matches, error_reason)，并拒绝越过 skill 根目录的引用。"""
    root_real = os.path.realpath(root)
    full = os.path.abspath(os.path.join(root, path))
    if not _path_inside(root_real, os.path.realpath(full)):
        return [], "路径越过 skill 根目录"

    if not set("*?[]{}") & set(path):
        if not os.path.exists(full):
            return [], "文件不存在"
        return [full], None

    matches = []
    try:
        for pattern in _brace_expand(full):
            matches.extend(_glob.glob(pattern))
    except (OSError, re.error) as exc:
        return [], f"glob 解析失败（{type(exc).__name__}）"
    if not matches:
        return [], "glob 没有匹配文件"
    unsafe = [item for item in matches if not _path_inside(root_real, os.path.realpath(item))]
    if unsafe:
        return [], "glob 匹配结果越过 skill 根目录"
    return matches, None


def _invocation_policy(root, fm):
    """读取 frontmatter 与 agents/openai.yaml 的调用策略，返回可审计结果。"""
    modes = []
    errors = []
    front_value = fm.get("disable-model-invocation")
    if front_value is not None and front_value != "":
        if isinstance(front_value, bool):
            modes.append(("frontmatter", "user" if front_value else "model"))
        elif isinstance(front_value, str) and front_value.lower() in ("true", "false"):
            modes.append(("frontmatter", "user" if front_value.lower() == "true" else "model"))
        else:
            errors.append("disable-model-invocation 必须是布尔值")

    yaml_path = os.path.join(root, "agents", "openai.yaml")
    if os.path.islink(yaml_path) and not os.path.exists(yaml_path):
        errors.append("agents/openai.yaml 是断开的软链")
    elif os.path.isfile(yaml_path):
        try:
            yaml_text = _read_text_inside(root, yaml_path)
            yaml_data, yaml_errors = _parse_yaml_mapping(yaml_text)
            errors.extend(f"agents/openai.yaml {item}" for item in yaml_errors)
            policy = yaml_data.get("policy")
            allow = policy.get("allow_implicit_invocation") if isinstance(policy, dict) else None
            if isinstance(allow, bool):
                modes.append(("agents/openai.yaml", "model" if allow else "user"))
            elif allow is not None:
                errors.append("agents/openai.yaml 的 allow_implicit_invocation 必须是布尔值")
        except OSError as exc:
            errors.append(f"无法读取 agents/openai.yaml（{type(exc).__name__}）")

    unique_modes = {mode for _source, mode in modes}
    if len(unique_modes) > 1:
        errors.append("frontmatter 与 agents/openai.yaml 的调用策略冲突")
    mode = next(iter(unique_modes), None)
    sources = [source for source, _mode in modes]
    return mode, sources, errors, os.path.isfile(yaml_path)


def check(root, profile="agent"):
    if profile not in PROFILES:
        raise ValueError(f"未知 Profile：{profile}")
    results = []
    def add(key, title, status, detail, fix=""):
        results.append({"key": key, "title": title, "status": status,
                        "detail": detail, "fix": fix, "imp": IMPORTANCE.get(key, 1.0)})

    root = os.path.abspath(root)
    root_real = os.path.realpath(root)
    md_path = find_skill_md(root)

    if not md_path:
        # 给个友好提示：是不是父目录、子目录里才有 skill
        nested = []
        if os.path.isdir(root):
            for d in sorted(os.listdir(root)):
                if os.path.isfile(os.path.join(root, d, "SKILL.md")):
                    nested.append(d)
        add("frontmatter", "存在 SKILL.md", "FAIL",
            f"目录里没有 SKILL.md：{root}",
            ("该目录下这些子目录才是 skill，请逐个指定：" + ", ".join(nested[:10]))
            if nested else "确认传入的是单个 skill 目录（里面要有 SKILL.md）。")
        return {
            "root": root, "root_real": root_real, "profile": profile, "results": results,
            "info": {}, "fm": {}, "fm_errors": [], "refs": [], "allfiles": [],
            "read_errors": [], "name": "",
        }

    try:
        text = _read_text_inside(root, md_path)
    except OSError as exc:
        add("readability", "SKILL.md 可读取", "FAIL",
            f"SKILL.md 无法读取（{exc}）。",
            "修正文件权限或去掉越界软链；检查器不能把入口文件读取失败当成通过。")
        return {
            "root": root, "root_real": root_real, "profile": profile, "results": results,
            "info": {}, "fm": {}, "fm_errors": [], "refs": [], "allfiles": [],
            "read_errors": [("SKILL.md", type(exc).__name__)], "name": "",
        }
    fm, _fm_raw, body, body_offset, fm_errors = parse_frontmatter(text)
    info = analyze_body(body, body_offset)
    allfiles = list_skill_files(root)
    refs = reference_files(allfiles)

    secret_hits, path_hits, read_errors = scan_secret_and_paths(root, allfiles)

    if read_errors:
        show = "; ".join(f"{rel}（{reason}）" for rel, reason in read_errors[:6])
        if len(read_errors) > 6:
            show += " …"
        add("readability", "可扫描文件可读取", "FAIL",
            f"{len(read_errors)} 个文本文件无法读取：{show}",
            "修正文件权限或移除不应随 Skill 分发的文件；不要让检查器把读取失败当成未发现问题。")
    else:
        add("readability", "可扫描文件可读取", "PASS",
            "纳入扫描的文本文件均可读取；密钥文件按规则跳过，未打开。")

    # ---------- #0 安全红线：硬编码密钥 ----------
    live_hits = [h for h in secret_hits if not in_test_fixture(h[0])]
    fixture_hits = [h for h in secret_hits if in_test_fixture(h[0])]
    if live_hits:
        sample = "; ".join(f"{r}:L{n} {lab}={v}" for r, n, lab, v in live_hits[:6])
        tail = f"（另有 {len(fixture_hits)} 处在测试夹具里，已降级）" if fixture_hits else ""
        add("secret", "无硬编码密钥（安全红线）", "FAIL",
            f"检出 {len(live_hits)} 处疑似密钥：{sample}{tail}",
            "立刻移出——skill 经常被打包分发/上传 GitHub，泄露面比私有代码更大。"
            "命中即视为已泄露，请轮换该凭据并检查 git 历史。")
    elif fixture_hits:
        sample = "; ".join(f"{r}:L{n} {lab}={v}" for r, n, lab, v in fixture_hits[:6])
        add("secret", "无硬编码密钥（安全红线）", "WARN",
            f"仅在测试夹具里检出 {len(fixture_hits)} 处疑似密钥：{sample}",
            "夹具里的假密钥通常是刻意载荷，不判红线；仍请翻一眼确认不是把真凭据当样本粘进来了。")
    else:
        add("secret", "无硬编码密钥（安全红线）", "PASS",
            "SKILL.md 及捆绑文件未检出 key / token / 私钥 / 口令赋值。")

    # ---------- #1 frontmatter 必填且格式合法 ----------
    raw_name = fm.get("name", "")
    raw_desc = fm.get("description", "")
    type_errors = []
    if raw_name and not isinstance(raw_name, str):
        type_errors.append("name 必须是字符串")
    if raw_desc and not isinstance(raw_desc, str):
        type_errors.append("description 必须是字符串或块标量")
    name = raw_name if isinstance(raw_name, str) else ""
    desc = raw_desc if isinstance(raw_desc, str) else ""
    name_ok = bool(re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name)) and len(name) <= 64
    if fm_errors or type_errors:
        details = "; ".join(fm_errors + type_errors)
        add("frontmatter", "frontmatter 必填齐全且合法", "FAIL",
            f"frontmatter 解析失败：{details}",
            "修正 YAML 缩进、重复字段和字段类型，再重新运行 Doctor。")
    elif not name or not desc:
        miss = [k for k in ("name", "description") if not fm.get(k)]
        add("frontmatter", "frontmatter 必填齐全且合法", "FAIL",
            f"缺少必填字段：{', '.join(miss)}（skill 无法被正确加载/触发）。",
            "补上 `name`（小写+连字符，≤64）和 `description`（写清做什么 + 何时用）。")
    elif not name_ok:
        add("frontmatter", "frontmatter 必填齐全且合法", "WARN",
            f"name=`{name}` 不符合规范（应全小写、用连字符、≤64 字符）。",
            "改成 kebab-case，如 `my-skill-name`；大写/下划线/空格会影响识别。")
    else:
        nonstd = [k for k in fm.keys() if k not in STANDARD_FM_KEYS]
        note = f"（另有非标准字段 {', '.join(nonstd)}，runtime 不读，可留可删）" if nonstd else ""
        add("frontmatter", "frontmatter 必填齐全且合法", "PASS",
            f"name/description 齐全，name 格式合规。{note}")

    # ---------- 可选 Codex Profile：迁入 skill-creator 的严格基础契约 ----------
    if profile == "codex":
        codex_errors = []
        unexpected = sorted(set(fm) - CODEX_FM_KEYS)
        if fm_errors:
            codex_errors.append("frontmatter 无法解析")
        if unexpected:
            codex_errors.append("不支持字段：" + ", ".join(unexpected))
        if not isinstance(raw_name, str) or not raw_name:
            codex_errors.append("name 必须是非空字符串")
        elif (not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", raw_name)
              or len(raw_name) > 64):
            codex_errors.append("name 必须是 ≤64 字符的 kebab-case，且不能连续连字符")
        if not isinstance(raw_desc, str) or not raw_desc:
            codex_errors.append("description 必须是非空字符串")
        elif raw_desc.startswith("[TODO:"):
            codex_errors.append("description 含未完成 TODO")
        elif "<" in raw_desc or ">" in raw_desc:
            codex_errors.append("description 不能含尖括号")
        elif len(raw_desc) > 1024:
            codex_errors.append("description 超过 1024 字符")
        todo_lines = unfinished_todo_lines(body, body_offset)
        if todo_lines:
            codex_errors.append("正文含未完成 TODO：" + ", ".join(f"L{line}" for line in todo_lines[:6]))
        if codex_errors:
            add("codex", "Codex 基础规范 Profile", "FAIL",
                "；".join(codex_errors),
                "仅保留 name/description/license/allowed-tools/metadata；清理 TODO、尖括号和不合规字段。")
        else:
            add("codex", "Codex 基础规范 Profile", "PASS",
                "通过 skill-creator 的零依赖基础契约：字段白名单、name、description 与 TODO 均合规。")

    # ---------- #2 description 写清「做什么 + 何时用」（触发质量）----------
    has_when = any(re.search(p, desc, re.I) for p in WHEN_SIGNALS)
    if not desc:
        add("trigger", "description 含「何时用」（触发质量）", "FAIL",
            "没有 description，模型无从判断何时加载本 skill。",
            "写成「做什么 + 何时/触发用」，例：'生成 X。当需要…时使用'。")
    elif len(desc) < 40:
        add("trigger", "description 含「何时用」（触发质量）", "WARN",
            f"description 仅 {len(desc)} 字符，太短，触发信号不足。",
            "扩写到能让模型判断「何时唤醒」：列出典型请求 / 触发词 / 适用场景。")
    elif has_when:
        add("trigger", "description 含「何时用」（触发质量）", "PASS",
            "description 同时写了「做什么」和「何时用」，触发信号清晰。")
    else:
        add("trigger", "description 含「何时用」（触发质量）", "WARN",
            "description 只说了「做什么」，没写「何时用」——模型可能在该用时没唤醒它。",
            "补一句触发场景：'当需要…时使用' / 'Use when …' / 列触发词。")

    # ---------- #2b description 长度上限 ----------
    if not desc:
        add("desclen", "description ≤ 1024 字符", "INFO", "无 description，长度不适用。")
    elif len(desc) <= 1024:
        add("desclen", "description ≤ 1024 字符", "PASS",
            f"{len(desc)} 字符，在上限内。")
    else:
        add("desclen", "description ≤ 1024 字符", "WARN",
            f"{len(desc)} 字符，超过 1024——可能被截断，触发不稳。",
            "精简到 1024 内：保留「做什么 + 何时用 + 关键触发词」，删修饰。")

    # ---------- #3 SKILL.md 篇幅（路由器不是图书馆）----------
    L, C = info["lines"], info["chars"]
    if L <= 500:
        add("length", "SKILL.md ≤ 500 行（按需加载的指令包）", "PASS",
            f"{L} 行 / {C} 字符，精简。")
    elif L <= 800:
        add("length", "SKILL.md ≤ 500 行（按需加载的指令包）", "WARN",
            f"{L} 行 / {C} 字符，偏长。",
            "把分版本/分平台/长流程的细节下沉到 references/，正文留路由指针。")
    else:
        add("length", "SKILL.md ≤ 500 行（按需加载的指令包）", "FAIL",
            f"{L} 行 / {C} 字符，远超——每次触发都把全部细节灌进上下文。",
            "拆成「精简路由 SKILL.md + references/ 多个专题文件」，用到哪个读哪个。")

    # ---------- #4 渐进披露：长内容是否拆了 references/ ----------
    # 只认"内容文档"(.md)：assets/字体/图片是捆绑资源，不算把正文内容下沉。
    content_refs = [r for r in refs if r.lower().endswith(".md")]
    nrefs = len(content_refs)
    if L <= 500:
        add("disclosure", "渐进披露（厚重细节下沉 references/）", "PASS",
            "SKILL.md 已足够精简，无需强制拆分。" + (f"（另带 {nrefs} 个参考文件）" if nrefs else ""))
    elif nrefs == 0:
        add("disclosure", "渐进披露（厚重细节下沉 references/）", "FAIL",
            f"正文 {L} 行却没有任何 references/ 拆分文件——全塞在单个 SKILL.md 里。",
            "建 references/ 目录，把各专题（分版本/分平台/分流程）抽成独立 .md，正文只留指针。")
    else:
        add("disclosure", "渐进披露（厚重细节下沉 references/）", "WARN",
            f"已拆出 {nrefs} 个参考文件，但 SKILL.md 仍 {L} 行，可继续下沉。",
            "把正文里仍然厚重的章节继续迁到 references/，正文回归「路由 + 硬规矩」。")

    # ---------- #4b 指针无死链 ----------
    dead = []
    for path, ln_no in info["ref_pointers"]:
        _matches, reason = _resolve_pointer(root, path)
        if reason:
            dead.append((path, ln_no, reason))
    uniq_ptr = {p for p, _ in info["ref_pointers"]}
    if not info["ref_pointers"]:
        add("pointers", "捆绑资源指针无死链", "INFO",
            "正文未引用 references/ scripts/ assets/ 等捆绑资源。")
    elif not dead:
        add("pointers", "捆绑资源指针无死链", "PASS",
            f"{len(uniq_ptr)} 个被引用的捆绑资源全部存在。")
    else:
        show = "; ".join(f"L{n}:{p}（{reason}）" for p, n, reason in dead[:6])
        show += " …" if len(dead) > 6 else ""
        # 死链是确定性事实，不是风格建议：判 FAIL 才能在 pre-push 快照里拦住漏提交。
        add("pointers", "捆绑资源指针无死链", "FAIL",
            f"{len(dead)} 处指针指向不存在的文件：{show}",
            "补上缺失文件，或修正/删除指针——模型按图索骥扑空比没指针更糟。")

    # ---------- #5 大段可执行代码是否外置 scripts/ ----------
    has_scripts = any(r.split(os.sep)[0].lower() in ("scripts", "script") for r in refs) \
        or any(r.lower().endswith((".py", ".sh", ".js")) and os.path.basename(r).lower() != "check.py"
               for r in allfiles)
    heavy_inline = info["code_lines"] >= 120 or info["fences"] >= 24 or info["max_code_block"] >= 40
    if not heavy_inline:
        add("scripts", "可执行代码已外置（不靠正文重打）", "PASS",
            f"内联代码量可控（{info['fences']//2} 块 / 共 {info['code_lines']} 行）。")
    elif has_scripts:
        add("scripts", "可执行代码已外置（不靠正文重打）", "PASS",
            f"内联代码偏多，但目录已带 scripts/ 文件，确定性可保。")
    else:
        add("scripts", "可执行代码已外置（不靠正文重打）", "WARN",
            f"内联代码偏重（{info['fences']//2} 块 / 共 {info['code_lines']} 行 / 最大单块 {info['max_code_block']} 行），"
            f"却没有 scripts/ 文件。",
            "把确定性脚本（构建/截图/合成/转换）抠成 scripts/ 真文件，正文只留一行'跑 scripts/xxx'。")

    # ---------- #6 可移植：无硬编码绝对路径 ----------
    if not path_hits:
        add("portable", "可移植（无硬编码绝对家目录路径）", "PASS",
            "未检出硬编码家目录绝对路径。")
    else:
        show = "; ".join(f"{r}:L{n} {p}" for r, n, p in path_hits[:5]) + (" …" if len(path_hits) > 5 else "")
        add("portable", "可移植（无硬编码绝对家目录路径）", "WARN",
            f"检出 {len(path_hits)} 处硬编码绝对路径：{show}",
            "换成 `~` / `$HOME` / 相对路径 / 「此 skill 目录」占位——别人装上后这些路径会失效。")

    # ---------- #7 allowed-tools 最小化（加内容项，低权重）----------
    raw_tools = fm.get("allowed-tools")
    if isinstance(raw_tools, list):
        tools = [str(t).strip() for t in raw_tools if str(t).strip()]
    elif isinstance(raw_tools, str):
        tools = [t.strip() for t in raw_tools.split(",") if t.strip()]
    else:
        tools = []
    invalid_tools = [
        tool for tool in tools
        if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_.:-]*(?:\([^)]*\))?", tool)
        and not tool.startswith("mcp__")
    ]
    if invalid_tools:
        add("tools", "声明 allowed-tools（最小权限）", "WARN",
            f"allowed-tools 含无法识别的工具名：{', '.join(invalid_tools[:5])}。",
            "确认工具名符合宿主语法；MCP 工具使用 mcp__ 前缀，避免把自然语言或整段命令写进权限字段。")
    elif tools:
        add("tools", "声明 allowed-tools（最小权限）", "PASS",
            f"已收敛工具集：{', '.join(tools[:8])}。")
    else:
        add("tools", "声明 allowed-tools（最小权限）", "INFO",
            "未声明 allowed-tools（继承会话全部工具）。",
            "可选：列出本 skill 真正需要的工具（如 Bash/Read/Write），减少越权面。")

    # ---------- #8 触发方式匹配（model vs user invoked）----------
    mode, policy_sources, policy_errors, has_openai_yaml = _invocation_policy(root, fm)
    if policy_errors:
        add("invocation", "触发方式与宿主策略一致", "FAIL",
            "；".join(policy_errors),
            "统一 disable-model-invocation 与 agents/openai.yaml 的 allow_implicit_invocation。")
    elif mode == "user":
        add("invocation", "触发方式与宿主策略一致", "PASS",
            f"已明确为仅手动触发（来源：{', '.join(policy_sources)}）。")
    elif mode == "model":
        add("invocation", "触发方式与宿主策略一致", "PASS",
            f"已明确允许模型自动触发（来源：{', '.join(policy_sources)}）。")
    elif has_openai_yaml:
        add("invocation", "触发方式与宿主策略一致", "INFO",
            "发现 agents/openai.yaml，但没有可判定的调用策略。",
            "若 Skill 只应手动调用，补 disable-model-invocation: true；否则在宿主元数据里明确策略。")
    else:
        add("invocation", "触发方式与宿主策略一致", "INFO",
            "未发现 disable-model-invocation 或 agents/openai.yaml，无法仅凭文件判定调用模式。",
            "手动触发型 Skill 建议声明 disable-model-invocation: true；模型触发型保留清晰 description。")

    # ---------- 目录名与 frontmatter name ----------
    entry_name = os.path.basename(root.rstrip(os.sep)).lower()
    if name and entry_name == name.lower():
        add("identity", "目录名与 frontmatter name 对齐", "PASS",
            f"目录名 {entry_name} 与 name 对齐。")
    elif name:
        add("identity", "目录名与 frontmatter name 对齐", "INFO",
            f"目录名 {entry_name} 与 name {name} 不同；软链别名或平台适配入口可接受。",
            "若不是有意的宿主别名，统一目录名和 frontmatter name，避免多宿主发现时重名。")
    else:
        add("identity", "目录名与 frontmatter name 对齐", "INFO",
            "frontmatter 没有可用于比对的 name。")

    # ---------- #11 paths / globs 文件作用域（Cursor 2.4+）----------
    paths_val = fm.get("paths") or fm.get("globs")
    if paths_val:
        if isinstance(paths_val, list) and paths_val:
            add("pathscope", "paths / globs 文件作用域", "PASS",
                f"已声明文件作用域：{', '.join(str(p) for p in paths_val[:4])}。")
        elif isinstance(paths_val, str) and paths_val.strip():
            add("pathscope", "paths / globs 文件作用域", "PASS",
                f"已声明文件作用域：{paths_val[:80]}。")
        else:
            add("pathscope", "paths / globs 文件作用域", "WARN",
                "paths/globs 字段存在但为空。",
                "删掉空字段，或写上 glob（如 src/**/*.ts）——只在匹配文件时加载 skill。")
    else:
        add("pathscope", "paths / globs 文件作用域", "INFO",
            "未声明 paths/globs（全项目可见，多数 skill 这样即可）。",
            "若 skill 只服务特定文件类型，可加 paths 减少误触发（Cursor 2.4+）。")

    # ---------- #12 OpenClaw / 安装声明（分发到 ClawHub 时）----------
    has_openclaw = False
    meta = fm.get("metadata")
    if isinstance(meta, dict) and any(k in meta for k in ("openclaw", "openclaw.compat")):
        has_openclaw = True
    elif isinstance(meta, str) and "openclaw" in meta.lower():
        has_openclaw = True
    has_install = bool(fm.get("requires") or fm.get("install"))
    has_scripts = any(r.split(os.sep)[0].lower() in ("scripts", "script") for r in refs)
    if has_openclaw or has_install:
        add("openclaw", "OpenClaw 兼容声明", "PASS",
            "检出 metadata.openclaw 或 requires/install 声明。")
    elif has_scripts:
        add("openclaw", "OpenClaw 兼容声明", "INFO",
            "有 scripts/ 但未声明 requires/install。",
            "若要发 ClawHub/OpenClaw，在 frontmatter 声明运行时依赖与安装方式。")
    else:
        add("openclaw", "OpenClaw 兼容声明", "INFO",
            "纯指令型 skill，无 OpenClaw 安装声明需求。")

    # ---------- #8 别替模型补它已经会的 ----------
    teach_hits = []
    body_lines = body.splitlines()
    for w in TEACHING:
        for m in re.finditer(re.escape(w), body, re.I):
            ln = body[:m.start()].count("\n")
            line = body_lines[ln] if ln < len(body_lines) else ""
            # 评分表/盲区里举例黑名单词 → 元层面，跳过
            if line.strip().startswith("|") or any(x in line for x in ("黑名单", "检查项", "待检测", "误报", "会误伤")):
                continue
            teach_hits.append((w, ln + 1 + body_offset))
    if not teach_hits:
        add("noteach", "别替模型补它已经会的（无教学冗余）", "PASS",
            "未检出「教通用写法/语言入门」类措辞。")
    else:
        sample = "; ".join(f"L{n}:'{w}'" for w, n in teach_hits[:5])
        add("noteach", "别替模型补它已经会的（无教学冗余）", "WARN",
            f"检出 {len(teach_hits)} 处教学型措辞：{sample}。",
            "读上下文确认：若在教模型通用知识就删——skill 只装「模型不可能自己知道」的项目/品牌私有事实。")

    # ---------- #9 配套文档（分发友好，加内容项低权重）----------
    has_readme = any(os.path.basename(r).lower().startswith("readme") for r in allfiles)
    has_changelog = any(os.path.basename(r).lower().startswith("changelog") for r in allfiles)
    if has_readme and has_changelog:
        add("companion", "配套文档齐全（README + CHANGELOG）", "PASS",
            "README 与 CHANGELOG 都在，分发/维护友好。")
    elif has_readme or has_changelog:
        add("companion", "配套文档齐全（README + CHANGELOG）", "INFO",
            f"有 {'README' if has_readme else 'CHANGELOG'}，缺另一个。",
            "可选：补齐 README（给人看）+ CHANGELOG（记版本），方便分发与回溯。")
    else:
        add("companion", "配套文档齐全（README + CHANGELOG）", "INFO",
            "缺 README / CHANGELOG。",
            "可选：要对外分发就补上；纯自用可忽略。")

    return {
        "root": root, "root_real": root_real, "profile": profile, "results": results,
        "info": info, "fm": fm, "fm_errors": fm_errors,
        "refs": refs, "allfiles": allfiles, "name": name,
        "read_errors": read_errors,
    }


def score(results):
    scored = [r for r in results if r["status"] in WEIGHT]
    if not scored:
        return 0, "—"
    num = sum(WEIGHT[r["status"]] * r.get("imp", 1.0) for r in scored)
    den = sum(r.get("imp", 1.0) for r in scored)
    s = round(num / den * 100)
    if s >= 85:   grade = "A · 优秀"
    elif s >= 70: grade = "B · 良好"
    elif s >= 50: grade = "C · 及格"
    else:         grade = "D · 建议重构"
    return s, grade


def result_summary(results):
    counts = {status: sum(1 for item in results if item["status"] == status)
              for status in ("PASS", "WARN", "FAIL", "INFO")}
    counts["gate"] = "FAIL" if counts["FAIL"] else "PASS"
    return counts


def print_report(data):
    print()
    print(bold("  SKILL DOCTOR  ") + dim(" · Agent Skill 体检报告"))
    print(dim("  会勇禾口王的AI笔记 · @huiyonghkw"))
    print(dim("  Doctor: " + DOCTOR_VERSION + " · 报告 schema: " + str(REPORT_SCHEMA_VERSION)
              + " · Profile: " + data.get("profile", "agent")))
    print(dim("  目标: " + data["root"]))
    if data.get("name"):
        info = data["info"]
        print(dim(f"  skill: {data['name']}  ·  SKILL.md {info.get('lines','?')} 行 / "
                  f"{len(data['refs'])} 个参考文件"))
    print(dim("  " + "─" * 58))
    print()

    for r in data["results"]:
        ico = COLOR[r["status"]](ICON[r["status"]])
        tag = COLOR[r["status"]](f"[{r['status']}]")
        print(f"  {ico} {tag} {bold(r['title'])}")
        print(dim(f"        {r['detail']}"))
        if r["fix"]:
            print(cyan(f"        → 建议: {r['fix']}"))
        print()

    if data.get("refs"):
        print(dim("  参考/资源文件（共 %d 个）:" % len(data["refs"])))
        for n in sorted(data["refs"])[:12]:
            print(dim("    · " + n))
        print()

    s, grade = score(data["results"])
    summary = result_summary(data["results"])
    bar_full = int(s / 5)
    bar = "█" * bar_full + "░" * (20 - bar_full)
    gcolor = green if s >= 85 else (yellow if s >= 50 else red)
    print(dim("  " + "─" * 58))
    print(f"  {bold('得分')}  {gcolor(bar)}  {gcolor(bold(str(s) + ' / 100'))}   {gcolor(grade)}")
    gate_color = red if summary["gate"] == "FAIL" else green
    print(f"  {bold('门禁')}  {gate_color(summary['gate'])}  "
          f"（FAIL {summary['FAIL']} · WARN {summary['WARN']} · INFO {summary['INFO']}）")
    print(dim("  注: 机检为启发式；'触发质量''是否图书馆''是否替模型补'需读正文复核。"))
    if not os.environ.get("HEKOUWANG_CONTENT_FACTORY"):
        print(dim("  可视化报告卡（付费增值）→ ClawHub/GitHub @huiyonghkw · 免费 CLI 永不过期"))
    print(dim("  " + "─" * 58))
    print(dim("  —— 会勇禾口王的AI笔记 · @huiyonghkw"))
    print(dim("     不聊 AI 会不会取代你，只聊先用 AI 的人怎么取代你。"))
    print()


def _discover_skill_mds(root, recursive=True):
    """递归发现 SKILL.md，同时记录断链和遍历错误。"""
    root = os.path.abspath(root)
    broken = []
    errors = []
    candidates = []
    if os.path.islink(root) and not os.path.exists(root):
        return [], [root], ["扫描根目录是断开的软链"]
    if not os.path.isdir(root):
        return [], [], [f"扫描根目录不是目录：{root}"]

    visited_dirs = set()

    def onerror(exc):
        errors.append(f"{getattr(exc, 'filename', root)}（{type(exc).__name__}）")

    # followlinks=False：发现入口时不穿越软链目录。
    for current, dirs, files in os.walk(
        root, topdown=True, followlinks=False, onerror=onerror
    ):
        real_current = os.path.realpath(current)
        if real_current in visited_dirs:
            dirs[:] = []
        else:
            visited_dirs.add(real_current)
            kept_dirs = []
            for directory in dirs:
                full = os.path.join(current, directory)
                if directory in SCAN_IGNORE_DIRS:
                    continue
                if os.path.islink(full):
                    if not os.path.exists(full):
                        broken.append(os.path.abspath(full))
                    continue
                kept_dirs.append(directory)
            dirs[:] = kept_dirs

            for filename in files:
                full = os.path.join(current, filename)
                if os.path.islink(full) and not os.path.exists(full):
                    broken.append(os.path.abspath(full))
            if not recursive and current != root:
                dirs[:] = []

        md_path = os.path.join(current, "SKILL.md")
        if os.path.isfile(md_path) and not os.path.islink(md_path):
            candidates.append(os.path.abspath(md_path))
    return candidates, sorted(set(broken)), errors


def scan_skills(root, recursive=True, profile="agent"):
    """递归盘点 Skill 入口，按真实 SKILL.md 去重并检查重名。"""
    root = os.path.abspath(root)
    candidates, broken, errors = _discover_skill_mds(root, recursive=recursive)
    if not candidates and not errors:
        errors.append("未发现带 SKILL.md 的 Skill")
    groups = {}
    for path in candidates:
        groups.setdefault(os.path.realpath(path), []).append(path)

    skills = []
    names = {}
    for real_md, entry_paths in sorted(groups.items()):
        data = check(os.path.dirname(real_md), profile=profile)
        summary = result_summary(data["results"])
        item = {
            "path": os.path.dirname(real_md),
            "entry_paths": sorted(entry_paths),
            "name": data.get("name") or None,
            "score": score(data["results"])[0],
            "grade": score(data["results"])[1],
            "gate": summary["gate"],
            "fail_count": summary["FAIL"],
            "warn_count": summary["WARN"],
            "info_count": summary["INFO"],
        }
        skills.append(item)
        if data.get("name"):
            names.setdefault(data["name"].lower(), []).append(item)

    duplicate_names = [
        {
            "name": key,
            "skills": [
                {"path": item["path"], "entry_paths": item["entry_paths"]}
                for item in values
            ],
        }
        for key, values in sorted(names.items())
        if len(values) > 1
    ]
    skill_fail = any(item["gate"] == "FAIL" for item in skills)
    gate = "FAIL" if broken or errors or duplicate_names or skill_fail else "PASS"
    return {
        "kind": "skill-scan",
        "doctor_version": DOCTOR_VERSION,
        "schema_version": REPORT_SCHEMA_VERSION,
        "root": root,
        "profile": profile,
        "recursive": recursive,
        "gate": gate,
        "entry_count": len(candidates),
        "skill_count": len(skills),
        "unique_skill_count": len(skills),
        "broken_symlinks": broken,
        "duplicate_names": duplicate_names,
        "scan_errors": errors,
        "skills": skills,
    }


def print_scan_report(data):
    print()
    print(bold("  SKILL DOCTOR  ") + dim(" · 多 Skill 扫描"))
    mode = "递归" if data.get("recursive", True) else "宿主直接入口"
    print(dim("  Doctor: " + data["doctor_version"] + " · 报告 schema: "
              + str(data["schema_version"]) + " · 模式: " + mode
              + " · Profile: " + data.get("profile", "agent")))
    print(dim("  目标: " + data["root"]))
    print()
    gate_color = red if data["gate"] == "FAIL" else green
    print(f"  {bold('门禁')}  {gate_color(data['gate'])}  "
          f"（入口 {data['entry_count']} 个，按真实 SKILL.md 去重后 {data['unique_skill_count']} 个）")
    if data["broken_symlinks"]:
        print(red("  ✗ 断开的软链："))
        for path in data["broken_symlinks"][:12]:
            print(dim("    · " + path))
    if data["duplicate_names"]:
        print(yellow("  ▲ 重名："))
        for duplicate in data["duplicate_names"]:
            print(dim("    · " + duplicate["name"]))
            for item in duplicate["skills"]:
                print(dim("      - " + item["path"]))
    if data["scan_errors"]:
        print(red("  ✗ 扫描错误："))
        for error in data["scan_errors"][:12]:
            print(dim("    · " + error))
    print()
    for item in data["skills"]:
        status = red(item["gate"]) if item["gate"] == "FAIL" else green(item["gate"])
        name = item["name"] or "(无 name)"
        print(f"  {status}  {name}  · {item['score']} / 100  · {item['path']}")
    print()
    print(dim("  —— 会勇禾口王的AI笔记 · @huiyonghkw"))
    print()


def main():
    ap = argparse.ArgumentParser(description="Agent Skill (SKILL.md) 体检器")
    ap.add_argument("path", nargs="?", default=".", help="skill 目录（默认当前目录）")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    ap.add_argument("--scan", action="store_true", help="递归扫描目录下的多个 Skill")
    ap.add_argument("--direct", action="store_true", help="扫描时只看根目录下一层宿主入口")
    ap.add_argument("--profile", choices=sorted(PROFILES), default="agent",
                    help="规范 Profile：agent（默认）或 codex（严格基础契约）")
    ap.add_argument("--version", action="version", version=DOCTOR_VERSION)
    args = ap.parse_args()

    if args.scan:
        data = scan_skills(args.path, recursive=not args.direct, profile=args.profile)
        if args.json:
            print(json.dumps(data, ensure_ascii=False, indent=2))
        else:
            print_scan_report(data)
        sys.exit(1 if data["gate"] == "FAIL" else 0)

    data = check(args.path, profile=args.profile)
    summary = result_summary(data["results"])

    if args.json:
        s, grade = score(data["results"])
        out = {
            "kind": "skill-check",
            "doctor_version": DOCTOR_VERSION,
            "schema_version": REPORT_SCHEMA_VERSION,
            "profile": data.get("profile", args.profile),
            "root": data["root"],
            "root_real": data.get("root_real"),
            "name": data.get("name"),
            "score": s,
            "grade": grade,
            "gate": summary["gate"],
            "pass_count": summary["PASS"],
            "warn_count": summary["WARN"],
            "fail_count": summary["FAIL"],
            "info_count": summary["INFO"],
            "info": data["info"],
            "refs": data["refs"],
            "read_errors": data.get("read_errors", []),
            "fm_errors": data.get("fm_errors", []),
            "results": data["results"],
        }
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        print_report(data)

    sys.exit(1 if summary["gate"] == "FAIL" else 0)


if __name__ == "__main__":
    main()
