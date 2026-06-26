#!/home/linuxbrew/.linuxbrew/bin/python3
"""
Hermes风格记忆自检脚本
定时检查记忆系统健康度，提示整理建议
"""

import os
import time
import sys
from pathlib import Path

SELF_IMPROVING = Path.home() / "self-improving"
MEMORY_FILE = Path.home() / ".openclaw" / "workspace" / "MEMORY.md"
USER_FILE = Path.home() / ".openclaw" / "workspace" / "USER.md"
SOUL_FILE = Path.home() / ".openclaw" / "workspace" / "SOUL.md"
HEARTBEAT_FILE = Path.home() / ".openclaw" / "workspace" / "HEARTBEAT.md"

# 记忆文件大小限制（参考Hermes）
LIMITS = {
    "MEMORY.md": 2200,
    "USER.md": 1375,
}

def get_file_stats(path):
    """获取文件统计信息"""
    if not path.exists():
        return None
    content = path.read_text()
    lines = content.split('\n')
    chars = len(content)
    entries = [l for l in lines if l.strip() and not l.startswith('#')]
    return {
        "chars": chars,
        "lines": len(lines),
        "entries": len(entries),
        "path": path,
        "name": path.name
    }

def check_memory_health():
    """检查记忆系统健康度"""
    print("=" * 50)
    print(f"🧠 Hermes记忆自检 {time.strftime('%Y-%m-%d %H:%M')}")
    print("=" * 50)
    
    all_ok = True
    suggestions = []
    
    # 检查主要记忆文件
    files_to_check = [MEMORY_FILE, USER_FILE, SOUL_FILE, HEARTBEAT_FILE]
    
    for f in files_to_check:
        stats = get_file_stats(f)
        if stats:
            if f == MEMORY_FILE:
                usage = stats['chars'] / 2200 * 100
                status = "🟢" if usage < 70 else "🟡" if usage < 90 else "🔴"
                print(f"\n{status} {f.name}: {stats['chars']}字 / 2200字 ({usage:.0f}%)")
                if usage >= 90:
                    suggestions.append("MEMORY.md使用率达90%+，建议整理")
                    all_ok = False
                elif usage >= 70:
                    suggestions.append("MEMORY.md使用率偏高，可考虑精简")
            elif f == USER_FILE:
                usage = stats['chars'] / 1375 * 100
                status = "🟢" if usage < 70 else "🟡" if usage < 90 else "🔴"
                print(f"{status} {f.name}: {stats['chars']}字 / 1375字 ({usage:.0f}%)")
                if usage >= 90:
                    suggestions.append("USER.md使用率达90%+，建议整理")
                    all_ok = False
            else:
                print(f"🟢 {f.name}: {stats['chars']}字 {stats['lines']}行")
    
    # 检查self-improving目录
    print(f"\n📁 ~/self-improving/ 目录状态:")
    si_files = list(SELF_IMPROVING.glob("*"))
    file_counts = {}
    total_lines = 0
    for sf in si_files:
        if sf.is_file():
            lines = len(sf.read_text().split('\n'))
            total_lines += lines
            file_counts[sf.name] = lines
    
    for name, lines in sorted(file_counts.items()):
        print(f"  {name}: {lines}行")
    
    print(f"  总计: {total_lines}行")
    
    # 建议
    print("\n" + "=" * 50)
    if suggestions:
        print("💡 整理建议:")
        for i, s in enumerate(suggestions, 1):
            print(f"  {i}. {s}")
    else:
        print("✅ 记忆系统状态良好，无需整理")
    
    print("=" * 50)
    
    # 保存状态
    import json
    state_file = SELF_IMPROVING / "hermes-memory-state.json"
    state = {
        "last_check": time.strftime("%Y-%m-%d %H:%M"),
        "all_ok": all_ok,
        "suggestions": suggestions,
        "memory_chars": get_file_stats(MEMORY_FILE)['chars'] if get_file_stats(MEMORY_FILE) else 0,
        "user_chars": get_file_stats(USER_FILE)['chars'] if get_file_stats(USER_FILE) else 0,
    }
    state_file.write_text(json.dumps(state, ensure_ascii=False, indent=2))
    
    return 0 if all_ok else 1

def main():
    code = check_memory_health()
    sys.exit(code)

if __name__ == "__main__":
    main()
