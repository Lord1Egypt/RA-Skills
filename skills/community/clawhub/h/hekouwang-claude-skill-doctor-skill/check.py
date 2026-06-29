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

退出码: 有 FAIL → 1，否则 0。

注意: 本脚本只做"机器能确定的部分"。description 触发质量、正文是不是"图书馆"、
是不是在替模型补它已会的知识——这些需人/模型读正文定夺，交给 SKILL.md 的定性复核。
脚本绝不读取任何 .env / *.key / *.pem 等密钥文件。
"""

import os
import re
import sys
import json
import glob as _glob
import argparse

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
    "tools": 0.6, "companion": 0.6,                  # 加内容项：有更好，缺失不重罚
}

IGNORE_DIRS = {
    ".git", "node_modules", "vendor", "dist", "build", "__pycache__",
    ".venv", "venv", ".idea", ".vscode", ".cache",
}

# 标准 frontmatter 字段（Anthropic Agent Skills 认得的）。其余字段无害但冗余（runtime 不读）。
STANDARD_FM_KEYS = {"name", "description", "allowed-tools", "license", "metadata"}

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
# ~ / $HOME / ${HOME} 是可移植的，不算；/Users/某人、/home/某人、C:\Users\某人 才是踩坑。
ABS_PATH_RE = re.compile(r"(?<![\w~])(/Users/[^/\s'\"`)]+|/home/[^/\s'\"`)]+|[A-Za-z]:\\\\?Users\\\\?[^\\\s'\"`)]+)")

# ---------- 密钥指纹（正文里出现 = 资损级，直接 FAIL）----------
SECRET_PATTERNS = [
    ("私钥块",        re.compile(r"-----BEGIN (?:RSA |EC |DSA |OPENSSH |PGP )?PRIVATE KEY-----")),
    ("OpenAI/Anthropic key", re.compile(r"sk-(?:ant-)?[A-Za-z0-9_\-]{20,}")),
    ("AWS Access Key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("Google API key", re.compile(r"\bAIza[0-9A-Za-z_\-]{35}\b")),
    ("GitHub token",   re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{36}\b|\bgithub_pat_[A-Za-z0-9_]{60,}")),
    ("Slack token",    re.compile(r"\bxox[baprs]-[A-Za-z0-9\-]{10,}")),
    ("JWT",            re.compile(r"\beyJ[A-Za-z0-9_\-]{10,}\.eyJ[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}")),
    ("硬编码口令/密钥赋值", re.compile(
        r"(?i)\b(?:password|passwd|pwd|secret|api[_\-]?key|access[_\-]?key|auth[_\-]?token|client[_\-]?secret)\b"
        r"\s*[:=]\s*['\"]([^'\"\s]{6,})['\"]")),
]
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
    return p if os.path.isfile(p) else None


def parse_frontmatter(text):
    """极简 frontmatter 解析（零依赖）。返回 (dict, raw_fm_text, body_text, body_offset)。
    body_offset = 正文前的行数（frontmatter 占了多少行），用于把正文相对行号还原成文件绝对行号。
    支持: `key: value`、块标量 `key: |`/`key: >`、行内 list `[a, b]`、缩进 list `- x`。"""
    if not text.startswith("---"):
        return {}, "", text, 0
    lines = text.splitlines()
    # 找到第二个 '---'
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return {}, "", text, 0
    fm_lines = lines[1:end]
    body = "\n".join(lines[end + 1:])
    data = {}
    i = 0
    key_re = re.compile(r"^([A-Za-z_][\w\-]*):\s*(.*)$")
    while i < len(fm_lines):
        ln = fm_lines[i]
        m = key_re.match(ln)
        if not m:
            i += 1
            continue
        key, val = m.group(1), m.group(2).strip()
        if val in ("|", ">", "|-", ">-", "|+", ">+"):           # 块标量
            blk = []
            i += 1
            while i < len(fm_lines) and (fm_lines[i].startswith((" ", "\t")) or fm_lines[i].strip() == ""):
                blk.append(fm_lines[i].strip())
                i += 1
            data[key] = " ".join(x for x in blk if x)
            continue
        if val.startswith("[") and val.endswith("]"):          # 行内 list
            data[key] = [x.strip().strip("'\"") for x in val[1:-1].split(",") if x.strip()]
            i += 1
            continue
        if val == "":                                          # 可能是缩进 list 或空
            items = []
            j = i + 1
            while j < len(fm_lines) and re.match(r"^\s*-\s+", fm_lines[j]):
                items.append(re.sub(r"^\s*-\s+", "", fm_lines[j]).strip().strip("'\""))
                j += 1
            if items:
                data[key] = items
                i = j
                continue
            data[key] = ""
            i += 1
            continue
        data[key] = val.strip().strip("'\"")                   # 普通标量
        i += 1
    return data, "\n".join(fm_lines), body, end + 1


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
    # 引用到的捆绑资源（相对路径）：references/ scripts/ assets/ reference/ examples/
    # 字符类含通配符 *?{}，让 deck-engine-*.html 这类 glob 被整体捕获（死链检查里再 glob 解析）。
    ptr_re = re.compile(r"(?<![\w./])((?:references?|scripts?|assets?|examples?|templates?)/[\w\-./*?{}]+)")
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
        for m in ptr_re.finditer(ln):
            info["ref_pointers"].append((m.group(1).rstrip(".`"), i + 1 + line_offset))
    return info


def list_skill_files(root):
    """返回 skill 目录里的相关文件（剔除 .git 等）。"""
    out = []
    for cur, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS and not d.startswith(".")]
        for f in files:
            rel = os.path.relpath(os.path.join(cur, f), root)
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

def scan_secret_and_paths(root, allfiles):
    """对 SKILL.md + 所有 .md/.py/.sh/.js 做密钥与硬编码绝对路径扫描。"""
    secret_hits, path_hits = [], []
    targets = [f for f in allfiles if f.lower().endswith((".md", ".py", ".sh", ".js", ".json", ".txt"))]
    for rel in targets:
        p = os.path.join(root, rel)
        try:
            with open(p, encoding="utf-8", errors="replace") as fh:
                text = fh.read()
        except Exception:
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
            ln_no = text[:m.start()].count("\n") + 1
            path_hits.append((rel, ln_no, m.group(1)))
    return secret_hits, path_hits


def check(root):
    results = []
    def add(key, title, status, detail, fix=""):
        results.append({"key": key, "title": title, "status": status,
                        "detail": detail, "fix": fix, "imp": IMPORTANCE.get(key, 1.0)})

    root = os.path.abspath(root)
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
        return {"root": root, "results": results, "info": {}, "fm": {}, "refs": [], "allfiles": []}

    with open(md_path, encoding="utf-8", errors="replace") as f:
        text = f.read()
    fm, _fm_raw, body, body_offset = parse_frontmatter(text)
    info = analyze_body(body, body_offset)
    allfiles = list_skill_files(root)
    refs = reference_files(allfiles)

    secret_hits, path_hits = scan_secret_and_paths(root, allfiles)

    # ---------- #0 安全红线：硬编码密钥 ----------
    if not secret_hits:
        add("secret", "无硬编码密钥（安全红线）", "PASS",
            "SKILL.md 及捆绑文件未检出 key / token / 私钥 / 口令赋值。")
    else:
        sample = "; ".join(f"{r}:L{n} {lab}={v}" for r, n, lab, v in secret_hits[:6])
        add("secret", "无硬编码密钥（安全红线）", "FAIL",
            f"检出 {len(secret_hits)} 处疑似密钥：{sample}",
            "立刻移出——skill 经常被打包分发/上传 GitHub，泄露面比私有代码更大。"
            "命中即视为已泄露，请轮换该凭据并检查 git 历史。")

    # ---------- #1 frontmatter 必填且格式合法 ----------
    name = fm.get("name", "")
    desc = fm.get("description", "")
    name_ok = bool(re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name or "")) and len(name) <= 64
    if not name or not desc:
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
    GLOB_CHARS = set("*?[]{}")
    dead = []
    for path, ln_no in info["ref_pointers"]:
        full = os.path.join(root, path)
        if GLOB_CHARS & set(path):
            # 通配/模板指针（如 deck-engine-*.html）：用 glob 解析，能匹配到就算存在；
            # brace 扩展 {a,b} glob 不支持，跳过不误报（典型是"两套模板"的简写）。
            try:
                if _glob.glob(full):
                    continue
            except Exception:
                pass
            if "{" in path or "}" in path:
                continue
            dead.append((path, ln_no))
        elif not os.path.exists(full):
            dead.append((path, ln_no))
    uniq_ptr = {p for p, _ in info["ref_pointers"]}
    if not info["ref_pointers"]:
        add("pointers", "捆绑资源指针无死链", "INFO",
            "正文未引用 references/ scripts/ assets/ 等捆绑资源。")
    elif not dead:
        add("pointers", "捆绑资源指针无死链", "PASS",
            f"{len(uniq_ptr)} 个被引用的捆绑资源全部存在。")
    else:
        show = "; ".join(f"L{n}:{p}" for p, n in dead[:6]) + (" …" if len(dead) > 6 else "")
        add("pointers", "捆绑资源指针无死链", "WARN",
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
            "未检出 /Users/... 或 /home/... 这类换台机器就废的硬路径。")
    else:
        show = "; ".join(f"{r}:L{n} {p}" for r, n, p in path_hits[:5]) + (" …" if len(path_hits) > 5 else "")
        add("portable", "可移植（无硬编码绝对家目录路径）", "WARN",
            f"检出 {len(path_hits)} 处硬编码绝对路径：{show}",
            "换成 `~` / `$HOME` / 相对路径 / 「此 skill 目录」占位——别人装上后这些路径会失效。")

    # ---------- #7 allowed-tools 最小化（加内容项，低权重）----------
    # 两种合法写法都认：YAML 列表（- a / [a,b]）与官方 frontmatter 的逗号字符串（allowed-tools: Bash, Read）。
    raw_tools = fm.get("allowed-tools")
    if isinstance(raw_tools, list):
        tools = [str(t).strip() for t in raw_tools if str(t).strip()]
    elif isinstance(raw_tools, str):
        tools = [t.strip() for t in raw_tools.split(",") if t.strip()]
    else:
        tools = []
    if tools:
        add("tools", "声明 allowed-tools（最小权限）", "PASS",
            f"已收敛工具集：{', '.join(tools[:8])}。")
    else:
        add("tools", "声明 allowed-tools（最小权限）", "INFO",
            "未声明 allowed-tools（继承会话全部工具）。",
            "可选：列出本 skill 真正需要的工具（如 Bash/Read/Write），减少越权面。")

    # ---------- #8 别替模型补它已经会的 ----------
    teach_hits = []
    for w in TEACHING:
        for m in re.finditer(re.escape(w), body, re.I):
            teach_hits.append((w, body[:m.start()].count("\n") + 1 + body_offset))
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

    return {"root": root, "results": results, "info": info, "fm": fm,
            "refs": refs, "allfiles": allfiles, "name": name}


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


def print_report(data):
    print()
    print(bold("  SKILL DOCTOR  ") + dim(" · Agent Skill 体检报告"))
    print(dim("  会勇禾口王的AI笔记 · @huiyonghkw"))
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
    bar_full = int(s / 5)
    bar = "█" * bar_full + "░" * (20 - bar_full)
    gcolor = green if s >= 85 else (yellow if s >= 50 else red)
    print(dim("  " + "─" * 58))
    print(f"  {bold('得分')}  {gcolor(bar)}  {gcolor(bold(str(s) + ' / 100'))}   {gcolor(grade)}")
    print(dim("  注: 机检为启发式；'触发质量''是否图书馆''是否替模型补'需读正文复核。"))
    print(dim("  " + "─" * 58))
    print(dim("  —— 会勇禾口王的AI笔记 · @huiyonghkw"))
    print(dim("     不聊 AI 会不会取代你，只聊先用 AI 的人怎么取代你。"))
    print()


def main():
    ap = argparse.ArgumentParser(description="Agent Skill (SKILL.md) 体检器")
    ap.add_argument("path", nargs="?", default=".", help="skill 目录（默认当前目录）")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    args = ap.parse_args()

    data = check(args.path)

    if args.json:
        s, grade = score(data["results"])
        out = {"root": data["root"], "name": data.get("name"),
               "score": s, "grade": grade,
               "info": data["info"], "refs": data["refs"], "results": data["results"]}
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        print_report(data)

    has_fail = any(r["status"] == "FAIL" for r in data["results"])
    sys.exit(1 if has_fail else 0)


if __name__ == "__main__":
    main()
