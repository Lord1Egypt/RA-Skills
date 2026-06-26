#!/usr/bin/env python3
"""Generate execution checklist + status checklist files.

Usage:
    python checklist-generator.py <note_name> <step1> [step2...]

The first argument MUST be the note name only — no command prefix/suffix.
Example: for 'kg 检查 苏州', pass '苏州' not '苏州检查'.
The final step (delete checklist files) is auto-appended.

Output: prints === EXECUTION LIST === and === CHECK LIST === sections.
If OBSIDIAN_VAULT env var is set, also saves to _working/ directory.

Example:
    python checklist-generator.py 傻瓜 内容检查拆分 分类匹配 名称匹配
"""
import sys, os, re

VAULT = os.environ.get('OBSIDIAN_VAULT', '')
WORKING = os.path.join(VAULT, '_working') if VAULT else '_working'


def sanitize_filename(name: str) -> str:
    """Remove chars invalid in Windows filenames."""
    return re.sub(r'[<>:"/\\\\|?*]', '_', name).strip() or 'untitled'


def generate(note: str, steps: list[str]) -> tuple[str, str]:
    # Auto-append final cleanup step
    all_steps = steps + ["删除本任务2个清单文件"]
    n = len(all_steps)
    bitmask = ':'.join(['0'] * n)

    lines = [f"# {note} — 执行清单", "## 步骤"]
    for i, desc in enumerate(all_steps, 1):
        lines.append(f"### {i}. {desc}")
        lines.append("- 操作类型：(待定)")
        if desc == "删除本任务2个清单文件":
            lines.append("- 标识：最后一步＝删除清单文件")
    exec_list = '\n'.join(lines)

    return exec_list, bitmask


def save_to_file(note: str, exec_list: str, check_list: str) -> tuple[str, str]:
    """Save checklists to _working/ directory. Returns (exec_path, check_path)."""
    os.makedirs(WORKING, exist_ok=True)
    safe = sanitize_filename(note)
    exec_path = os.path.join(WORKING, f"{safe}_执行清单.md")
    check_path = os.path.join(WORKING, f"{safe}_检查清单.md")

    with open(exec_path, 'w', encoding='utf-8') as f:
        f.write(exec_list)
    with open(check_path, 'w', encoding='utf-8') as f:
        f.write(check_list)

    return exec_path, check_path


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print(f"USAGE: python {os.path.basename(__file__)} <note_name> <step1> [step2...]", file=sys.stderr)
        print("       First arg = note name only (e.g. '苏州', NOT '苏州检查')", file=sys.stderr)
        print("       The final step (删除本任务2个清单文件) is auto-appended.", file=sys.stderr)
        sys.exit(1)

    note = sys.argv[1]
    steps = sys.argv[2:]

    if not steps:
        print("ERROR: need at least 1 step", file=sys.stderr)
        sys.exit(1)

    exec_list, check_list = generate(note, steps)

    print("=== EXECUTION LIST ===")
    print(exec_list)
    print("\n=== CHECK LIST ===")
    print(check_list)

    if VAULT:
        exec_path, check_path = save_to_file(note, exec_list, check_list)
        print(f"\n=== SAVED ===")
        print(f"  exec: {exec_path}")
        print(f"  check: {check_path}")
