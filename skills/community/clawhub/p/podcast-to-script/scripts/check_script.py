#!/usr/bin/env python3
"""script.md / notes.md format checker — self-contained (zero external deps).

Vendored copy of the podcast pipeline's validation rules (validate_podcast.py +
the parse semantics of script_md.py), so this skill closes its own loop without
depending on a downstream checkout. Rules here mirror references/script-spec.md
and references/notes-spec.md; when the spec changes, update THIS file too.

Usage:
  python3 check_script.py --script script.md
  python3 check_script.py --notes notes.md
  python3 check_script.py --script script.md --notes notes.md

Exit code: 0 = all pass, 1 = violations found.
"""

import argparse
import re
import sys
from pathlib import Path

# ===== speaker model (mirrors script_md.py) =====

KNOWN_SPEAKERS = {"主持人", "嘉宾", "旁白", "host", "guest", "narration", "narrator"}
NARRATION_NAMES = {"旁白", "narration", "narrator"}

SPEAKER_LINE_RE = re.compile(r'\*\*([^*]+?)\*\*[：:](.*)')
HEADING_SPEAKER_RE = re.compile(r'#{1,6}\s+(\*\*[^*]+?\*\*[：:].*)')
SEGMENT_RE = re.compile(r'^##\s+第\s*(\d+)\s*段\s*[·•・]\s*(.+)$')


def parse_turns(text: str) -> list[tuple[str, str]]:
    """Parse script.md into [(speaker, text)] — same semantics as the synthesizer:

    - `**role**: text` opens a turn (full- or half-width colon)
    - bare lines after a speaker line are continuations, joined into that turn
    - blank lines / headings / quotes / list items / --- end a turn
    - the H2 closing line (## **role**: ...) is stripped of '#' and synthesized
    """
    turns, cur_spk, cur_txt = [], None, []

    def flush():
        nonlocal cur_spk, cur_txt
        if cur_spk and cur_txt:
            turns.append((cur_spk, " ".join(cur_txt).strip()))
        cur_spk, cur_txt = None, []

    for line in text.split("\n"):
        s = line.strip()
        m_hs = HEADING_SPEAKER_RE.match(s)
        if m_hs:
            s = m_hs.group(1)
        elif SEGMENT_RE.match(s) or s.startswith(("#", ">", "* ")) or s == "---" or s == "":
            flush()
            continue
        m = SPEAKER_LINE_RE.match(s)
        if m:
            flush()
            cur_spk = m.group(1).strip()
            if m.group(2).strip():
                cur_txt.append(m.group(2).strip())
        elif cur_spk:
            cur_txt.append(s)
    flush()
    return [(sp, tx) for sp, tx in turns if tx]


# ===== script.md rules =====

TITLE_FORMAT_RE = re.compile(r'^#\s+.*[A-Za-z].*\s--\s.+')   # {English} -- {中文副标题}
OLD_TITLE_RE = re.compile(r'^#\s*播客脚本[：:]')
ANY_SPEAKER_RE = re.compile(r'^(?:#{1,6}\s+)?\*\*([^*]+?)\*\*[：:]')
OLD_SEGMENT_RE = re.compile(r'^##\s+第.+段[：:]')
SPEAKER_RE = re.compile(r'^\*\*(主持人|嘉宾|旁白|Host|Guest)\*\*[:：]\s*.+')
NARRATION_RE = re.compile(r'^\*\*旁白\*\*[:：]\s*.+')
CLOSING_RE = re.compile(r'感谢收听.*show\s*notes.*下期见|我们下期见')
NARRATION_CLOSING = "好，回到对话。"
MAX_NARRATIONS = 4


def validate_script(filepath) -> list[str]:
    lines = Path(filepath).read_text(encoding="utf-8").splitlines(keepends=True)
    issues, has_title, has_closing = [], False, False
    segments = []
    narration_lines = []
    current_segment_line = -1

    for i, line in enumerate(lines):
        stripped = line.strip()

        if stripped.startswith("# ") and not stripped.startswith("## "):
            if OLD_TITLE_RE.match(stripped):
                issues.append(f"L{i+1}: 标题不应带'播客脚本:'前缀，直接用 '# {{标题}}'")
            elif not has_title and not TITLE_FORMAT_RE.match(stripped):
                issues.append(f"L{i+1}: 标题格式应为 '{{English title}} -- {{中文副标题}}'"
                              f"（' -- ' 分隔），当前: {stripped[:60]}")
            has_title = True

        m_any = ANY_SPEAKER_RE.match(stripped)
        if m_any and m_any.group(1).strip().lower() not in KNOWN_SPEAKERS:
            issues.append(f"L{i+1}: 未知角色 '**{m_any.group(1)}**'——只允许 主持人/嘉宾/旁白，"
                          f"否则会静默落到嘉宾音色")

        m = SEGMENT_RE.match(stripped)
        if m:
            segments.append((i + 1, stripped))
            current_segment_line = i

        if OLD_SEGMENT_RE.match(stripped) and not m:
            issues.append(f"L{i+1}: 分段格式应为 '## 第 N 段 · 子标题'（用中点·分隔），当前: {stripped}")

        if SPEAKER_RE.match(stripped) and NARRATION_RE.match(stripped):
            narration_lines.append((i + 1, current_segment_line))

        if CLOSING_RE.search(stripped):
            has_closing = True

    if not has_title:
        issues.append("缺少标题行（# {title}）")
    if not has_closing:
        issues.append("缺少固定收尾句（'感谢收听，完整原文列表在 show notes 里。我们下期见'）")
    if not segments:
        issues.append("未找到任何分段（## 第 N 段 · 子标题）")

    # 旁白必须在段落开头、对话开始之前
    for narr_line, seg_line in narration_lines:
        if seg_line < 0:
            issues.append(f"L{narr_line}: 旁白出现在分段标题之前，应放在段落开头")
        for j in range(seg_line, narr_line - 1):
            if SPEAKER_RE.match(lines[j].strip()) and not NARRATION_RE.match(lines[j].strip()):
                issues.append(f"L{narr_line}: 旁白应放在段落开头、对话开始之前，不应插在问答中间")
                break

    # 台词级检查（与合成器同一套解析语义）
    turns = parse_turns(Path(filepath).read_text(encoding="utf-8"))
    narrations = [t for s, t in turns if s.strip().lower() in NARRATION_NAMES]
    if len(narrations) > MAX_NARRATIONS:
        issues.append(f"旁白 {len(narrations)} 段，超过每期上限 {MAX_NARRATIONS} 段——多了节目会碎")
    for t in narrations:
        if not t.rstrip().endswith(NARRATION_CLOSING):
            issues.append(f"旁白缺统一收束句'{NARRATION_CLOSING}'：{t[:40]}...")
    for s, t in turns:
        if "http://" in t or "https://" in t:
            issues.append(f"台词包含 URL（会被逐字朗读）：{s}: {t[:60]}...")

    return issues


# ===== notes.md rules =====

NOTES_FIRST_LINE_RE = re.compile(r'^本期.+。.*一句话主线[：:].+')
TIMELINE_RE = re.compile(r'^-\s+\d{2}:\d{2}\s+.+')


def validate_notes(filepath) -> list[str]:
    lines = Path(filepath).read_text(encoding="utf-8").strip().split("\n")
    issues = []

    if lines:
        first_text_line = ""
        for line in lines:
            stripped = line.strip()
            if stripped and not stripped.startswith("!["):
                first_text_line = stripped
                break
        if not NOTES_FIRST_LINE_RE.match(first_text_line):
            issues.append(f"首行应为 '本期{{导语}}。一句话主线：{{主线}}'，当前: {first_text_line[:60]}...")

    has_summary = has_links = has_timeline = False
    for line in lines:
        stripped = line.strip()
        if stripped == "**内容速览**":
            has_summary = True
        elif stripped == "**时间轴**":
            has_timeline = True
        elif stripped in ("**原文链接**", "**延伸阅读**"):
            has_links = True

    if not has_summary:
        issues.append("缺少 **内容速览** section")
    if not has_links:
        issues.append("缺少 **原文链接** 或 **延伸阅读** section")

    if has_timeline:
        in_timeline, timeline_count = False, 0
        for line in lines:
            stripped = line.strip()
            if stripped == "**时间轴**":
                in_timeline = True
                continue
            if in_timeline:
                if stripped.startswith("**") or (stripped and not stripped.startswith("-")):
                    break
                if TIMELINE_RE.match(stripped):
                    timeline_count += 1
        if timeline_count == 0:
            issues.append("**时间轴** section 下没有有效的时间轴条目（格式: - MM:SS 段落名）")

    for i, line in enumerate(lines):
        if line.strip().startswith("# ") and not line.strip().startswith("## "):
            issues.append(f"L{i+1}: notes.md 不应有顶级标题（#），首行直接是导语")
            break

    return issues


def main() -> int:
    ap = argparse.ArgumentParser(description="script.md / notes.md 格式校验（自包含副本）")
    ap.add_argument("--script")
    ap.add_argument("--notes")
    args = ap.parse_args()
    if not args.script and not args.notes:
        ap.error("请至少指定 --script 或 --notes")

    all_issues = []
    for label, path, fn in (("script.md", args.script, validate_script),
                            ("notes.md", args.notes, validate_notes)):
        if not path:
            continue
        if not Path(path).exists():
            print(f"❌ 文件不存在: {path}", file=sys.stderr)
            return 1
        print(f"校验 {label}: {path}")
        issues = fn(path)
        for issue in issues:
            print(f"  ⚠️ {issue}")
        if not issues:
            print(f"  ✅ {label} 格式全部通过")
        print()
        all_issues.extend(issues)

    if all_issues:
        print(f"共 {len(all_issues)} 个不合规项", file=sys.stderr)
        return 1
    print("🎉 全部通过")
    return 0


if __name__ == "__main__":
    sys.exit(main())
