#!/usr/bin/env python3
"""check_frontmatter.py — Step 4: SKILL.md frontmatter 跨 agent 兼容校验

3 hard rules (hello-env v1.0.0→v1.0.2 实证):
  1. description 用 > folded scalar
  2. description ≤ 1024 字节
  3. frontmatter 只留 name + description（version/metadata/author/tags 都搬 body）

外加:
  4. Markdown body 顶部 4 行必加（Version/License/Author/Repository）
"""
import re
import sys
from pathlib import Path

ALLOWED_KEYS = {"name", "description"}
MAX_DESC_BYTES = 1024
REQUIRED_BODY_LINES = ["Version", "License", "Author", "Repository"]


def check(skill_path: Path) -> int:
    skill_md = skill_path / "SKILL.md" if skill_path.is_dir() else skill_path
    if not skill_md.exists():
        print(f"❌ SKILL.md not found: {skill_md}", file=sys.stderr)
        return 1

    text = skill_md.read_text(encoding="utf-8")
    errors, warnings = [], []

    # ─── frontmatter 提取 ──────────────────────────
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.DOTALL)
    if not m:
        errors.append("frontmatter 缺失或格式错误（缺 --- ... --- 块）")
        print_report(errors, warnings)
        return 1

    fm_raw, body = m.group(1), m.group(2)

    # 解析顶层 key（不用 yaml 库以避免依赖）
    top_keys = []
    for line in fm_raw.split("\n"):
        # 顶层 key 行不以空格开头
        km = re.match(r"^([a-zA-Z_][\w-]*)\s*:", line)
        if km:
            top_keys.append(km.group(1))

    # Rule 3: 只留 name + description
    extra = [k for k in top_keys if k not in ALLOWED_KEYS]
    if extra:
        errors.append(
            f"frontmatter 含禁止字段 {extra}（必须只留 name+description；"
            "version/metadata/author/tags 搬到 Markdown body）"
        )
    missing = ALLOWED_KEYS - set(top_keys)
    if missing:
        errors.append(f"frontmatter 缺必需字段 {missing}")

    # Rule 1: description 用 > folded scalar
    desc_m = re.search(r"^description\s*:\s*(.*)$", fm_raw, re.MULTILINE)
    if desc_m:
        first_token = desc_m.group(1).strip()
        if first_token not in (">", ">-", ">+", "|", "|-", "|+"):
            warnings.append(
                f"description 应该用 > folded scalar 风格（当前: '{first_token[:30]}...'），"
                "避免引号转义问题（hello-env v1.0.0→v1.0.2 实证）"
            )

    # Rule 2: description ≤ 1024 字节
    # 简单提取 description 整段（folded scalar）
    fm_lines = fm_raw.split("\n")
    desc_content = []
    in_desc = False
    for line in fm_lines:
        if re.match(r"^description\s*:", line):
            in_desc = True
            rest = line.split(":", 1)[1].strip()
            if rest and rest not in (">", ">-", ">+", "|", "|-", "|+"):
                desc_content.append(rest)
            continue
        if in_desc:
            if re.match(r"^[a-zA-Z_]", line):
                # 下一个顶层 key
                in_desc = False
                continue
            desc_content.append(line.strip())
    desc_full = " ".join(desc_content).strip()
    desc_bytes = len(desc_full.encode("utf-8"))
    if desc_bytes > MAX_DESC_BYTES:
        errors.append(
            f"description 长度 {desc_bytes} bytes 超 {MAX_DESC_BYTES} bytes 上限（Anthropic 限制）"
        )

    # Rule 4: body 顶部 4 行
    # 拿 body 头 30 行看
    body_head = "\n".join(body.split("\n")[:40])
    for key in REQUIRED_BODY_LINES:
        # 匹配 - **Key**: value 形式
        if not re.search(rf"-\s*\*\*{key}\*\*\s*:", body_head):
            warnings.append(
                f"Markdown body 顶部 4 行缺 `- **{key}**: ...`（clawhub 卡片只解析 SKILL.md 顶部）"
            )

    print_report(errors, warnings)
    return 1 if errors else 0


def print_report(errors, warnings):
    print(f"\n📋 SKILL.md frontmatter check")
    print("=" * 50)
    if errors:
        print(f"\n❌ ERR ({len(errors)}):")
        for e in errors:
            print(f"   - {e}")
    if warnings:
        print(f"\n⚠️  WARN ({len(warnings)}):")
        for w in warnings:
            print(f"   - {w}")
    if not errors and not warnings:
        print("\n✅ All 4 rules passed.")
    elif not errors:
        print(f"\n✅ 0 ERR（{len(warnings)} WARN 建议修但不阻断）")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <skill-path-or-SKILL.md>", file=sys.stderr)
        sys.exit(2)
    sys.exit(check(Path(sys.argv[1]).expanduser()))
