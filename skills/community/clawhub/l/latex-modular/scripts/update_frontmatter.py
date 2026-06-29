"""
update_frontmatter.py - 更新 SKILL.md 的 frontmatter
原子操作：读取 -> 修改 -> tmp 写入 -> os.replace
用法: python update_frontmatter.py <skill_dir> [--version x.y.z] [--description text]
"""
import os
import re
import sys
import tempfile
from pathlib import Path

def read_frontmatter(skill_md_path: str) -> dict:
    """读取 SKILL.md 的 frontmatter（YAML 格式）"""
    with open(skill_md_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    if not content.startswith("---"):
        return {"error": "No frontmatter found (missing ---)"}
    
    # 提取 --- 之间的内容
    m = re.match(r"---\n(.*?)\n---", content, re.DOTALL)
    if not m:
        return {"error": "Malformed frontmatter"}
    
    fm_text = m.group(1)
    fm = {}
    for line in fm_text.splitlines():
        line = line.strip()
        if ":" in line:
            key, _, val = line.partition(":")
            fm[key.strip()] = val.strip()
    
    fm["_body_start"] = content.find("---", 3) + 3
    fm["_raw_fm"] = fm_text
    fm["_full_content"] = content
    return fm

def update_frontmatter(skill_dir: str, updates: dict) -> dict:
    """
    更新 SKILL.md 的 frontmatter
    updates: {"version": "x.y.z", "description": "text", ...}
    """
    skill_md = Path(skill_dir) / "SKILL.md"
    if not skill_md.exists():
        return {"success": False, "error": f"SKILL.md not found in {skill_dir}"}
    
    fm = read_frontmatter(str(skill_md))
    if "error" in fm:
        return {"success": False, "error": fm["error"]}
    
    # 构建新的 frontmatter
    lines = fm["_raw_fm"].splitlines()
    new_lines = []
    updated_keys = set()
    
    for line in lines:
        matched = False
        for key, val in updates.items():
            # 匹配 "key: " 或 "key:val"
            if line.startswith(key + ":") or line.startswith(key + ": "):
                new_lines.append(f"{key}: {val}")
                updated_keys.add(key)
                matched = True
                break
        if not matched:
            new_lines.append(line)
    
    # 添加未找到的新键
    for key, val in updates.items():
        if key not in updated_keys:
            new_lines.append(f"{key}: {val}")
    
    new_fm = "\n".join(new_lines)
    new_content = "---\n" + new_fm + "\n---" + fm["_full_content"][fm["_body_start"]:]
    
    # 原子写入
    tmp_fd = None
    tmp_path = None
    try:
        fd, tmp_path = tempfile.mkstemp(
            dir=str(skill_md.parent),
            suffix=".tmp",
            prefix="skill_md_"
        )
        tmp_fd = fd
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(new_content)
        tmp_fd = None
        os.replace(tmp_path, str(skill_md))
        tmp_path = None
        return {"success": True, "path": str(skill_md)}
    except Exception as e:
        return {"success": False, "error": f"{type(e).__name__}: {e}"}
    finally:
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.unlink(tmp_path)
            except:
                pass

def main():
    if len(sys.argv) < 2:
        print("Usage: python update_frontmatter.py <skill_dir> [--version x.y.z] [--description text] [--key val]")
        sys.exit(1)
    
    skill_dir = sys.argv[1]
    updates = {}
    
    i = 2
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg.startswith("--"):
            key = arg[2:]
            if i + 1 < len(sys.argv) and not sys.argv[i + 1].startswith("--"):
                updates[key] = sys.argv[i + 1]
                i += 2
            else:
                updates[key] = "true"
                i += 1
        else:
            i += 1
    
    if not updates:
        print("No updates specified. Use --key val to update frontmatter.")
        sys.exit(1)
    
    print(f"[update_frontmatter] Updating {skill_dir}/SKILL.md ...")
    result = update_frontmatter(skill_dir, updates)
    
    if result["success"]:
        print(f"[update_frontmatter] ✓ Updated: {result['path']}")
        for k, v in updates.items():
            print(f"  {k}: {v}")
    else:
        print(f"[update_frontmatter] ✗ Failed: {result['error']}")
        sys.exit(1)

if __name__ == "__main__":
    main()
