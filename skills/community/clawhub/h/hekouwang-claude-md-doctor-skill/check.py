#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
hekouwang-claude-md-doctor-skill · CLAUDE.md 体检器（确定性机检层）
会勇禾口王的AI笔记 · @huiyonghkw —— 不聊 AI 会不会取代你，只聊先用 AI 的人怎么取代你。

零依赖（仅用 Python3 标准库）。对一个项目目录里的 CLAUDE.md 做启发式检查，
按"运行时配置而非项目说明书"的 10 条最佳实践打分，输出可读报告 + 修复线索。

用法:
    python3 check.py [项目目录]            # 默认当前目录
    python3 check.py [项目目录] --json     # 机器可读 JSON

退出码: 有 FAIL → 1，否则 0。

注意: 本脚本只做"机器能确定的部分"。是否真的是"图书馆内容""规则是否可执行"
这类判断需要人/模型读正文定夺——交给 SKILL.md 的定性复核环节。脚本绝不读取
任何 .env / *.key / *.pem 等密钥文件。
"""

import os
import re
import sys
import json
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

# ---------- 各检查项重要度权重（"减法优先"）----------
# 让"越短越准"类核心项更重；"加内容"类项（Hook/记忆/人格）缺了只算小扣分。
# 否则工具会一边喊"越短越好"，一边因为"没写工作风格块"扣人分，逼用户把文件写长。
IMPORTANCE = {
    # 安全红线：正文里有密钥 = 资损级，权重拉满
    "secret": 1.5,
    # 减法核心：短、可执行、路由不堆料、别替模型补它已会的
    "exist": 1.5, "length": 1.5, "actionable": 1.5, "router": 1.5, "noteach": 1.5,
    # 标准项
    "donot": 1.0, "local": 1.0, "thirtysec": 1.0, "pointers": 1.0,
    # 加内容项：有更好，但缺失不重罚（别逼用户做加法）
    "hooks": 0.6, "memory": 0.6, "persona": 0.6,
}

# ---------- 扫描时忽略的目录 ----------
IGNORE_DIRS = {
    ".git", "node_modules", "vendor", "dist", "build", ".next", "out",
    "target", ".venv", "venv", "__pycache__", ".idea", ".vscode",
    "coverage", ".cache", "tmp", ".turbo", ".gradle", "Pods",
}

# ---------- 敏感模块目录名（缺本地 CLAUDE.md 风险高）----------
# HIGH = 碰钱/碰密钥/碰数据迁移，强烈建议本地 CLAUDE.md（驱动 WARN）
SENSITIVE_HIGH = [
    "payment", "payments", "payout", "billing", "checkout", "wallet",
    "oauth", "credential", "credentials", "secret", "secrets", "crypto",
    "keystore", "auth", "authentication",
]
# SOFT = 相关但噪声大或更宜用 Hook 保护（migrations/admin/account 等），仅作提示
SENSITIVE_SOFT = [
    "login", "session", "account", "security", "token", "migrations",
    "migration", "permission", "permissions", "rbac", "admin", "iam",
    "infra", "deploy",
]
# 前端路由/资源段：命中这些路径段的目录不算"服务模块"，跳过
UI_SEGMENTS = {
    "views", "view", "pages", "page", "components", "component", "router",
    "routes", "store", "stores", "assets", "api", "utils", "hooks",
    "layouts", "styles", "mixins", "composables", "widgets",
}
CODE_EXT = {".php", ".js", ".ts", ".tsx", ".jsx", ".vue", ".py", ".go",
            ".java", ".rb", ".rs", ".cs", ".kt", ".swift", ".scala"}

# ---------- 模糊词（不可执行的"可感受"规则）----------
VAGUE = [
    "干净的代码", "代码要干净", "保持简洁", "简洁优雅", "优雅的代码", "清晰易懂",
    "高质量代码", "高质量的代码", "合理的命名", "规范的代码", "注重性能", "良好的",
    "易于维护", "可维护性", "遵循最佳实践", "最佳实践", "写好代码",
    "clean code", "keep it simple", "be concise", "write good code",
    "high quality", "high-quality", "follow best practices", "best practices",
    "readable code", "maintainable", "elegant", "well-written", "idiomatic code",
]

# ---------- 教学型措辞（#10：替模型补它"已经会"的通用知识 = 随模型升级很快过时的冗余）----------
# 命中这些 = 多半在教模型怎么写常规代码 / 怎么用主流框架，而不是写项目私有事实。
# 强信号、低误伤为主；最终是否冗余仍要读正文，脚本只 WARN 提示。
TEACHING = [
    "使用教程", "入门教程", "新手教程", "使用方法", "使用指南", "如何使用",
    "怎么用", "怎样使用", "教程：", "教程:", "示例教程",
    "step by step", "step-by-step", "follow these steps", "how to use",
    "getting started", "tutorial",
]

# 架构/流程图特征字符（箭头 + 方框角）。注意：├└│ 等"树连接符"不在此列——
# 目录树是路由地图，应保留在正文，不该被当成"图书馆图"建议下沉。
FLOW_CHARS = set("▼▲►◄→←↔╔╗╚╝═┌┐┘╭╮╯╰")

# ---------- 密钥指纹（正文里出现 = 资损级，直接 FAIL）----------
# 教程头号 Don't："Never store secrets in CLAUDE.md"。本脚本不读 .env，
# 但被体检的 CLAUDE.md 正文本身绝不该硬编码密钥。只收高置信度指纹，低误伤。
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
# 赋值型占位符（宽）：仅用于 password=/secret= 这类，值常是示范，需宽豁免。
PLACEHOLDER_RE = re.compile(
    r"(?i)(x{3,}|y{3,}|your[_\-]?|<[^>]*>|\$\{|\benv\b|process\.env|os\.environ|"
    r"example|changeme|placeholder|redacted|todo|n/a|\.\.\.|…|abc123|123456|test|dummy|sample)")
# 指纹型填充（窄）：sk-/AKIA/私钥等已高度具体，只豁免明显的文档占位，别误杀含数字串的真 key。
FILLER_RE = re.compile(r"(?i)(x{4,}|y{4,}|your|<|>|\.\.\.|…|example|placeholder|redacted|dummy|sample)")


def _redact(s):
    """脱敏：保留前 4 位 + 长度，其余打码，避免在报告里二次泄露。"""
    s = s.strip()
    if len(s) <= 8:
        return s[:2] + "***"
    return s[:4] + "***" + f"({len(s)} 字符)"


def find_target_md(root):
    """返回 (root_md_path or None, 'CLAUDE.md'|'CLAUDE.local.md')"""
    for name in ("CLAUDE.md", "CLAUDE.local.md"):
        p = os.path.join(root, name)
        if os.path.isfile(p):
            return p, name
    return None, None


def walk_dirs(root, maxdepth=5):
    root = os.path.abspath(root)
    base_depth = root.rstrip(os.sep).count(os.sep)
    for cur, dirs, files in os.walk(root):
        depth = cur.rstrip(os.sep).count(os.sep) - base_depth
        if depth >= maxdepth:
            dirs[:] = []
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS and not d.startswith(".")]
        yield cur, dirs, files


def scan_nested_claude(root):
    out = []
    for cur, dirs, files in walk_dirs(root):
        if cur == os.path.abspath(root):
            continue
        if "CLAUDE.md" in files:
            out.append(os.path.relpath(os.path.join(cur, "CLAUDE.md"), root))
    return out


def _basename_tokens(base):
    return set(re.split(r"[-_.\s]+", base.lower()))

def scan_sensitive(root):
    """返回 [(相对目录, 是否已有 CLAUDE.md, 是否 HIGH)]，已剔除前端路由/无代码目录。"""
    seen = {}
    for cur, dirs, files in walk_dirs(root):
        rel = os.path.relpath(cur, root)
        if rel == ".":
            continue
        segs = {s.lower() for s in rel.split(os.sep)}
        if segs & UI_SEGMENTS:          # 前端路由/资源段，跳过
            continue
        toks = _basename_tokens(os.path.basename(cur))
        is_high = bool(toks & set(SENSITIVE_HIGH))
        is_soft = bool(toks & set(SENSITIVE_SOFT))
        if not (is_high or is_soft):
            continue
        if not any(os.path.splitext(f)[1] in CODE_EXT for f in files):  # 无源码，多半不是模块
            continue
        seen[rel] = ("CLAUDE.md" in files, is_high)
    return sorted((rel, c, h) for rel, (c, h) in seen.items())


def analyze_body(text):
    """逐行分析正文，返回结构信息。"""
    lines = text.splitlines()
    info = {
        "lines": len(lines),
        "chars": len(text),
        "max_code_block": 0,
        "max_code_block_isdiagram": False,
        "max_table_rows": 0,
        "docs_pointers": 0,
        "pointers": [],   # [(path, line_no, kind)]  kind: 'docs' | 'import'
        "headings": [],
    }
    in_code = False
    cur_code_len = 0
    cur_code_diagram = False
    table_run = 0
    # 原生 @import 语法：@ 后跟一个含 / 或带扩展名的路径（排除 @邮箱、@提及）
    import_re = re.compile(r"(?:^|\s)@(~?[\w\-./]+\.[\w]+|~?[\w\-.]+/[\w\-./]+)")
    for i, ln in enumerate(lines):
        ln_no = i + 1
        st = ln.strip()
        if st.startswith("```"):
            if not in_code:
                in_code, cur_code_len, cur_code_diagram = True, 0, False
            else:
                if cur_code_len > info["max_code_block"]:
                    info["max_code_block"] = cur_code_len
                    info["max_code_block_isdiagram"] = cur_code_diagram
                in_code = False
            continue
        if in_code:
            cur_code_len += 1
            # 仅当出现箭头/方框角（真·架构或流程图）才标记；纯目录树(├└│──)不算
            if sum(ch in FLOW_CHARS for ch in ln) >= 2 or "->" in ln or "-->" in ln:
                cur_code_diagram = True
            continue
        # 表格行
        if st.startswith("|") and st.endswith("|"):
            table_run += 1
            info["max_table_rows"] = max(info["max_table_rows"], table_run)
        else:
            table_run = 0
        # 标题
        if st.startswith("#"):
            info["headings"].append(st.lstrip("#").strip())
        # docs/ 文本指针
        for m in re.finditer(r"docs/[\w\-./]+", ln):
            info["pointers"].append((m.group(0).rstrip("."), ln_no, "docs"))
            info["docs_pointers"] += 1
        # 原生 @import 指针
        for m in import_re.finditer(ln):
            info["pointers"].append((m.group(1), ln_no, "import"))
    return info


def check(root):
    results = []
    def add(key, title, status, detail, fix=""):
        results.append({"key": key, "title": title, "status": status,
                        "detail": detail, "fix": fix,
                        "imp": IMPORTANCE.get(key, 1.0)})

    root = os.path.abspath(root)
    md_path, md_name = find_target_md(root)

    if not md_path:
        add("exist", "存在 CLAUDE.md", "FAIL",
            "项目根目录没有 CLAUDE.md。",
            "在项目根创建 CLAUDE.md（用 #06 骨架起步：速览 / 工作风格 / 铁律 / 指针）。")
        return {"root": root, "md_name": None, "results": results, "info": {}, "nested": [], "sensitive": []}

    with open(md_path, encoding="utf-8", errors="replace") as f:
        text = f.read()
    info = analyze_body(text)
    low = text.lower()

    # #0 安全红线：正文里硬编码密钥 = 资损级，直接 FAIL
    secret_hits = []
    for label, pat in SECRET_PATTERNS:
        for m in pat.finditer(text):
            frag = m.group(0)
            if m.groups() and m.lastindex:   # 赋值型：判捕获的值，宽豁免
                val = m.group(1)
                if PLACEHOLDER_RE.search(val):
                    continue
            else:                            # 指纹型：判整段，仅窄豁免
                val = frag
                if FILLER_RE.search(val):
                    continue
            ln_no = text[:m.start()].count("\n") + 1
            secret_hits.append((label, ln_no, _redact(val)))
    if not secret_hits:
        add("secret", "无硬编码密钥（安全红线）", "PASS",
            "正文未检出 key / token / 私钥 / 口令赋值。")
    else:
        sample = "; ".join(f"L{n} {lab}：{red}" for lab, n, red in secret_hits[:6])
        add("secret", "无硬编码密钥（安全红线）", "FAIL",
            f"正文检出 {len(secret_hits)} 处疑似密钥：{sample}",
            "立刻移出 CLAUDE.md（它每次会话都进上下文、还可能被提交进 git）。"
            "改放 .env / 密钥管理器，正文最多写'见环境变量 XXX'。命中后请视为已泄露并轮换。")

    # #1 篇幅（越短越好，200 行经验上限）
    L, C = info["lines"], info["chars"]
    if L <= 200:
        add("length", "篇幅 ≤ 200 行（路由器不是图书馆）", "PASS",
            f"{L} 行 / {C} 字符，在经验上限内。")
    elif L <= 300:
        add("length", "篇幅 ≤ 200 行", "WARN",
            f"{L} 行 / {C} 字符，超过 200 行经验上限。",
            "把'图书馆'内容（架构图/大表/历史）下沉到 docs/，正文留指针。")
    else:
        add("length", "篇幅 ≤ 200 行", "FAIL",
            f"{L} 行 / {C} 字符，远超 200 行——每次会话都在为冗余付费。",
            "按'值不值得每次会话付费'逐段裁剪，大块迁移到 docs/。")

    # #2 禁止清单（Do NOT）
    neg_bullets = len(re.findall(r"(?m)^\s*[-*]\s.*(不要|禁止|不得|严禁|🚫|do not|don't|never)", text, re.I))
    has_neg_heading = bool(re.search(r"(?m)^#{1,4}\s.*(禁止|不要|do not|don't|never|约束)", text, re.I))
    if neg_bullets >= 3 or has_neg_heading:
        add("donot", "有禁止清单（Do NOT introduce）", "PASS",
            f"检出 {neg_bullets} 条禁止式条目" + ("，且有专门小节。" if has_neg_heading else "。"))
    elif neg_bullets >= 1:
        add("donot", "有禁止清单（Do NOT introduce）", "WARN",
            f"只有 {neg_bullets} 条禁止式条目。",
            "补一个'禁止/不要引入'清单：列出项目已淘汰/冲突的库与做法，挡住模型'好心'引入。")
    else:
        add("donot", "有禁止清单（Do NOT introduce）", "FAIL",
            "没有任何禁止式规则。",
            "新增 Do NOT 清单——这是防止模型引入不兼容依赖最省事的一招。")

    # #3 规则可操作（模糊词扫描）
    vague_hits = []
    for w in VAGUE:
        for m in re.finditer(re.escape(w), text, re.I):
            ln_no = text[:m.start()].count("\n") + 1
            vague_hits.append((w, ln_no))
    if not vague_hits:
        add("actionable", "规则可操作（非'写干净代码'式空话）", "PASS",
            "未检出常见模糊词。")
    else:
        sample = "; ".join(f"L{n}:'{w}'" for w, n in vague_hits[:5])
        add("actionable", "规则可操作（非'写干净代码'式空话）", "WARN",
            f"检出 {len(vague_hits)} 处模糊措辞：{sample}",
            "改成 5 秒内能判定的具体规则（如'组件≤200行''禁 any''async/await 替代 then 链'）。")

    # #4 路由器不是图书馆（大块内容 + 历史叙事）
    smells = []
    if info["max_code_block"] >= 25 and info["max_code_block_isdiagram"]:
        smells.append(f"一段 {info['max_code_block']} 行的 ASCII 图/框图")
    if info["max_table_rows"] >= 15:
        smells.append(f"一张 {info['max_table_rows']} 行的大表")
    if re.search(r"(?m)^#{1,4}\s.*(历史|history|背景故事|起源|愿景|价值观|公司|关于我们|story|origin)", text, re.I):
        smells.append("疑似项目历史/叙事小节")
    if smells:
        add("router", "路由器不是图书馆（无大块可下沉内容）", "WARN",
            "检出可能属于'图书馆'的大块：" + "；".join(smells) + "。",
            "迁移到 docs/architecture.md 等，正文只留一行指针（Tier 2 按需打开）。")
    else:
        npts = len(info["pointers"])
        note = f"（含 {npts} 处下沉指针 docs/ 或 @import，路由风格 👍）" if npts else ""
        add("router", "路由器不是图书馆（无大块可下沉内容）", "PASS",
            "未检出明显的大块图书馆内容。" + note)

    # #4b 指针/import 不能是死链（指向不存在的文件比没指针更糟）
    dead = []
    for path, ln_no, kind in info["pointers"]:
        if path.startswith("~"):
            target = os.path.expanduser(path)
        elif os.path.isabs(path):
            target = path
        else:
            target = os.path.join(root, path)
        if not os.path.exists(target):
            dead.append((path, ln_no, kind))
    if not info["pointers"]:
        add("pointers", "下沉指针均可解析（无死链）", "INFO",
            "正文没有 docs/ 或 @import 指针。")
    elif not dead:
        add("pointers", "下沉指针均可解析（无死链）", "PASS",
            f"{len(info['pointers'])} 处指针全部指向存在的文件。")
    else:
        show = "; ".join(f"L{n}:{p}" for p, n, k in dead[:6]) + (" …" if len(dead) > 6 else "")
        add("pointers", "下沉指针均可解析（无死链）", "WARN",
            f"{len(dead)} 处指针指向不存在的文件：{show}",
            "补上缺失的 docs 文件，或修正/删除死链——模型按图索骥扑空比没指针更费事。")

    # #5 敏感模块本地 CLAUDE.md（HIGH 驱动 WARN，SOFT 仅提示）
    sensitive = scan_sensitive(root)
    high_uncovered = [rel for rel, cov, hi in sensitive if hi and not cov]
    soft_uncovered = [rel for rel, cov, hi in sensitive if (not hi) and not cov]
    if not sensitive:
        add("local", "高危模块有本地 CLAUDE.md", "INFO",
            "未发现明显的高危服务模块（payment/auth/...）。")
    elif not high_uncovered:
        extra = f"（另有 {len(soft_uncovered)} 个 account/admin 类目录可酌情加）" if soft_uncovered else ""
        add("local", "高危模块有本地 CLAUDE.md", "PASS",
            f"碰钱/碰密钥/碰迁移的高危模块都已覆盖。{extra}")
    else:
        show = ", ".join(high_uncovered[:8]) + (" …" if len(high_uncovered) > 8 else "")
        add("local", "高危模块有本地 CLAUDE.md", "WARN",
            f"{len(high_uncovered)} 个高危模块缺本地 CLAUDE.md：{show}",
            "给碰钱/碰认证/碰迁移的服务目录各加一个本地 CLAUDE.md，写安全红线与已知陷阱。")

    # #6 Hook 强制层
    hook_found = False
    settings_files = []
    for sf in (".claude/settings.json", ".claude/settings.local.json"):
        p = os.path.join(root, sf)
        if os.path.isfile(p):
            settings_files.append(sf)
            try:
                with open(p, encoding="utf-8") as f:
                    data = json.load(f)
                if isinstance(data, dict) and data.get("hooks"):
                    hook_found = True
            except Exception:
                pass
    if hook_found:
        add("hooks", "关键规则有 Hook 强制（不靠模型记忆）", "PASS",
            "检出 .claude/settings.json 配置了 hooks。")
    elif settings_files:
        add("hooks", "关键规则有 Hook 强制（不靠模型记忆）", "WARN",
            "有 .claude/settings.json 但未配 hooks。",
            "把最不能漏的规则（格式化/跑测试/改 .env 提醒）升级成 Pre/PostToolUse Hook。")
    else:
        add("hooks", "关键规则有 Hook 强制（不靠模型记忆）", "WARN",
            "未发现 .claude/settings.json。",
            "可选：用 Hook 把'你必须'类规则变成强制执行，而非'请记住'。")

    # #7 MEMORY.md 跨会话回路
    mentions_mem = "memory.md" in low or re.search(r"记忆|memory", low) is not None
    mem_exists = os.path.isfile(os.path.join(root, "MEMORY.md"))
    if ("memory.md" in low) or (mentions_mem and mem_exists):
        add("memory", "跨会话记忆回路（MEMORY.md）", "PASS",
            "CLAUDE.md 提及记忆机制" + ("，且存在 MEMORY.md。" if mem_exists else "。"))
    else:
        add("memory", "跨会话记忆回路（MEMORY.md）", "WARN",
            "未发现 MEMORY.md 回路。",
            "加一条指令：任务前读 MEMORY.md、任务后写回新发现——一个文件实现跨会话记忆。")

    # #8 工作风格 / 人格块
    persona = re.search(
        r"(工作风格|working style|协作风格|你是谁|先给方案|先方案后代码|语气|tone of|"
        r"汇报用中文|回复用中文|偏好|preferences|persona|don't say|不要说|不要用.{0,8}(客套|废话))",
        text, re.I)
    if persona:
        add("persona", "工作风格块（你是谁 / 你讨厌什么）", "PASS",
            "检出工作风格 / 协作偏好相关内容。")
    else:
        add("persona", "工作风格块（你是谁 / 你讨厌什么）", "WARN",
            "没有工作风格 / 人格块。",
            "加一段'My Working Style'：先方案后代码、列选项不猜、讨厌的回复腔——省掉每次开场白。")

    # #9 30 秒三问信号
    sig_product = re.search(r"概述|overview|速览|简介|about|项目是|是一个", low) is not None
    sig_stack = re.search(r"技术栈|tech stack|stack|框架|framework|语言|runtime", low) is not None
    sig_where = re.search(r"目录结构|directory|structure|结构|放哪|新代码|where", low) is not None
    got = sum([sig_product, sig_stack, sig_where])
    if got == 3:
        add("thirtysec", "30 秒三问（产品 / 技术栈 / 新代码放哪）", "PASS",
            "三类信号齐全。")
    elif got == 2:
        miss = [n for n, s in (("产品定位", sig_product), ("技术栈", sig_stack), ("新代码放哪", sig_where)) if not s]
        add("thirtysec", "30 秒三问（产品 / 技术栈 / 新代码放哪）", "WARN",
            f"缺少信号：{'、'.join(miss)}。",
            "确认开头能让陌生人 30 秒答出：这是什么产品？技术栈？新代码放哪？")
    else:
        add("thirtysec", "30 秒三问（产品 / 技术栈 / 新代码放哪）", "FAIL",
            "三问信号不足。",
            "顶部补一段 30 秒速览：产品一句话 + 技术栈 + 目录/落点。")

    # #10 别替模型补它已经会的（教学型措辞 = 随模型升级很快过时的冗余）
    teach_hits = []
    for w in TEACHING:
        for m in re.finditer(re.escape(w), text, re.I):
            ln_no = text[:m.start()].count("\n") + 1
            teach_hits.append((w, ln_no))
    teach_heading = re.search(
        r"(?m)^#{1,4}\s.*(教程|tutorial|使用指南|使用说明|如何使用|how to use|getting started)",
        text, re.I)
    if not teach_hits and not teach_heading:
        add("noteach", "别替模型补它已经会的（无教学型冗余）", "PASS",
            "未检出'教模型写常规代码/用主流框架'的教学型措辞。")
    else:
        bits = []
        if teach_heading:
            bits.append(f"疑似教学小节：'{teach_heading.group(0).lstrip('#').strip()[:30]}'")
        if teach_hits:
            sample = "; ".join(f"L{n}:'{w}'" for w, n in teach_hits[:5])
            bits.append(f"{len(teach_hits)} 处教学型措辞（{sample}）")
        add("noteach", "别替模型补它已经会的（无教学型冗余）", "WARN",
            "；".join(bits) + "。这类内容随模型升级自动变强，写进常驻正文只是为'很快过时的东西'每次付费。",
            "读正文确认：若是教通用写法/框架用法，删掉——CLAUDE.md 只装模型不可能知道的"
            "项目私有事实（数据模型/命名约定/内部红线/版本环境）。")

    return {
        "root": root, "md_name": md_name, "results": results,
        "info": info, "nested": scan_nested_claude(root), "sensitive": sensitive,
    }


def score(results):
    scored = [r for r in results if r["status"] in WEIGHT]
    if not scored:
        return 0, "—"
    # 按重要度加权：减法核心项更重，加内容项缺失不重罚
    num = sum(WEIGHT[r["status"]] * r.get("imp", 1.0) for r in scored)
    den = sum(r.get("imp", 1.0) for r in scored)
    s = round(num / den * 100)
    if s >= 85:   grade = "A · 优秀"
    elif s >= 70: grade = "B · 良好"
    elif s >= 50: grade = "C · 及格"
    else:         grade = "D · 建议重写"
    return s, grade


def print_report(data):
    root = data["root"]
    print()
    print(bold("  CLAUDE.md DOCTOR  ") + dim(" · CLAUDE.md 体检报告"))
    print(dim("  会勇禾口王的AI笔记 · @huiyonghkw"))
    print(dim("  目标: " + root))
    if data["md_name"]:
        info = data["info"]
        print(dim(f"  文件: {data['md_name']}  ·  {info['lines']} 行 / {info['chars']} 字符"))
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

    if data.get("nested"):
        print(dim("  本地 CLAUDE.md（共 %d 个）:" % len(data["nested"])))
        for n in data["nested"][:12]:
            print(dim("    · " + n))
        print()

    s, grade = score(data["results"])
    bar_full = int(s / 5)
    bar = "█" * bar_full + "░" * (20 - bar_full)
    gcolor = green if s >= 85 else (yellow if s >= 50 else red)
    print(dim("  " + "─" * 58))
    print(f"  {bold('得分')}  {gcolor(bar)}  {gcolor(bold(str(s) + ' / 100'))}   {gcolor(grade)}")
    print(dim("  注: 机检为启发式；'图书馆 vs 路由器''规则是否可执行'需读正文复核。"))
    print(dim("  " + "─" * 58))
    print(dim("  —— 会勇禾口王的AI笔记 · @huiyonghkw"))
    print(dim("     不聊 AI 会不会取代你，只聊先用 AI 的人怎么取代你。"))
    print()


def main():
    ap = argparse.ArgumentParser(description="CLAUDE.md 体检器")
    ap.add_argument("path", nargs="?", default=".", help="项目目录（默认当前目录）")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    args = ap.parse_args()

    data = check(args.path)

    if args.json:
        s, grade = score(data["results"])
        out = {"root": data["root"], "md_name": data["md_name"],
               "score": s, "grade": grade,
               "info": data["info"], "nested": data["nested"],
               "sensitive": [{"dir": d, "covered": c, "high": h} for d, c, h in data["sensitive"]],
               "results": data["results"]}
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        print_report(data)

    has_fail = any(r["status"] == "FAIL" for r in data["results"])
    sys.exit(1 if has_fail else 0)


if __name__ == "__main__":
    main()
