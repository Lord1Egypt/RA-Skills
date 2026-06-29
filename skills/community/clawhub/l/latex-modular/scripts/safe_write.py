"""
safe_write.py - 原子写入工具（tmp + os.replace）
确保 UTF-8 中文编码不损坏，适用于所有 .md 和 .tex 文件写入
"""
import os
import tempfile
import shutil
from pathlib import Path

def safe_write(filepath: str, content: str, encoding: str = "utf-8") -> dict:
    """
    原子写入文件，使用 tmp + os.replace 方式。
    返回: {"success": bool, "path": str, "backup": str|None, "error": str|None}
    """
    fp = Path(filepath)
    result = {"success": False, "path": str(fp), "backup": None, "error": None}
    tmp_fd = None
    tmp_path = None
    try:
        # 如果文件已存在，先备份
        if fp.exists():
            backup_dir = fp.parent / ".backup"
            backup_dir.mkdir(exist_ok=True)
            backup_name = fp.name + ".bak"
            backup_path = backup_dir / backup_name
            shutil.copy2(str(fp), str(backup_path))
            result["backup"] = str(backup_path)

        # 写入临时文件
        fp.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp_path = tempfile.mkstemp(dir=str(fp.parent), suffix=".tmp", prefix=fp.stem + "_")
        tmp_fd = fd
        with os.fdopen(fd, "w", encoding=encoding, errors="replace") as f:
            f.write(content)
        tmp_fd = None  # fd 已关闭

        # 原子替换
        os.replace(tmp_path, str(fp))
        tmp_path = None

        result["success"] = True
        return result
    except Exception as e:
        result["error"] = f"{type(e).__name__}: {e}"
        return result
    finally:
        # 清理临时文件
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.unlink(tmp_path)
            except:
                pass

def safe_patch_by_line(filepath: str, line_num: int, new_line: str, encoding: str = "utf-8") -> dict:
    """
    按行号精确替换（1-based line number）
    """
    fp = Path(filepath)
    if not fp.exists():
        return {"success": False, "error": f"File not found: {filepath}"}
    try:
        with open(fp, "r", encoding=encoding, errors="replace") as f:
            lines = f.readlines()
        if line_num < 1 or line_num > len(lines):
            return {"success": False, "error": f"Line {line_num} out of range (1-{len(lines)})"}
        # 确保新行有换行符
        if not new_line.endswith("\n"):
            new_line = new_line + "\n"
        lines[line_num - 1] = new_line
        content = "".join(lines)
        return safe_write(filepath, content, encoding)
    except Exception as e:
        return {"success": False, "error": f"{type(e).__name__}: {e}"}

def safe_patch_regex(filepath: str, pattern: str, replacement: str, encoding: str = "utf-8") -> dict:
    """
    按正则匹配替换（只替换第一个匹配，replace_all=True 时替换全部）
    """
    import re
    fp = Path(filepath)
    if not fp.exists():
        return {"success": False, "error": f"File not found: {filepath}"}
    try:
        with open(fp, "r", encoding=encoding, errors="replace") as f:
            content = f.read()
        new_content, n = re.subn(pattern, replacement, content)
        if n == 0:
            return {"success": False, "error": f"Pattern not found: {pattern}"}
        result = safe_write(filepath, new_content, encoding)
        result["replacements"] = n
        return result
    except Exception as e:
        return {"success": False, "error": f"{type(e).__name__}: {e}"}

def safe_insert_after(filepath: str, after_pattern: str, insert_text: str, encoding: str = "utf-8") -> dict:
    """
    在匹配行后插入文本
    """
    import re
    fp = Path(filepath)
    if not fp.exists():
        return {"success": False, "error": f"File not found: {filepath}"}
    try:
        with open(fp, "r", encoding=encoding, errors="replace") as f:
            lines = f.readlines()
        target_idx = -1
        for i, line in enumerate(lines):
            if re.search(after_pattern, line):
                target_idx = i
                break
        if target_idx == -1:
            return {"success": False, "error": f"Pattern not found: {after_pattern}"}
        new_lines = lines[:target_idx+1] + [insert_text if insert_text.endswith("\n") else insert_text+"\n"] + lines[target_idx+1:]
        content = "".join(new_lines)
        return safe_write(filepath, content, encoding)
    except Exception as e:
        return {"success": False, "error": f"{type(e).__name__}: {e}"}

def safe_delete(filepath: str, backup: bool = True) -> dict:
    """
    安全删除文件：先备份到 .backup 目录再删除。
    返回: {"success": bool, "path": str, "backup": str|None, "error": str|None}
    """
    fp = Path(filepath)
    result = {"success": False, "path": str(fp), "backup": None, "error": None}
    if not fp.exists():
        result["error"] = f"File not found: {filepath}"
        return result
    try:
        if backup:
            backup_dir = fp.parent / ".backup"
            backup_dir.mkdir(exist_ok=True)
            backup_name = fp.name + ".del." + fp.stem + ".bak"
            backup_path = backup_dir / backup_name
            shutil.copy2(str(fp), str(backup_path))
            result["backup"] = str(backup_path)
        os.unlink(str(fp))
        result["success"] = True
        return result
    except Exception as e:
        result["error"] = f"{type(e).__name__}: {e}"
        return result

if __name__ == "__main__":
    import sys
    if len(sys.argv) >= 3:
        cmd = sys.argv[1]
        path = sys.argv[2]
        if cmd == "write":
            content = sys.argv[3] if len(sys.argv) > 3 else ""
            result = safe_write(path, content)
            print(result)
        elif cmd == "patch-line":
            line_num = int(sys.argv[3])
            new_line = sys.argv[4]
            result = safe_patch_by_line(path, line_num, new_line)
            print(result)
        elif cmd == "patch-regex":
            pattern = sys.argv[3]
            replacement = sys.argv[4]
            result = safe_patch_regex(path, pattern, replacement)
            print(result)
        elif cmd == "insert-after":
            pattern = sys.argv[3]
            insert_text = sys.argv[4]
            result = safe_insert_after(path, pattern, insert_text)
            print(result)
        elif cmd == "delete":
            result = safe_delete(path)
            print(result)
        else:
            print(f"Unknown command: {cmd}")
    else:
        print("Usage: python safe_write.py <command> <filepath> [args...]")
        print("Commands: write, patch-line, patch-regex, insert-after, delete")
