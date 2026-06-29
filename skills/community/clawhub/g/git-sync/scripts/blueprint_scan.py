#!/usr/bin/env python3
"""
blueprint_scan.py — git-sync 蓝图扫描
输入: 目标技能目录
输出: blueprint.json（文件树 + 类型标注 + 内容采样）

不做判断，只罗列事实。LLM 据此 + blueprint_rules.md 做出排除/脱敏决策。
"""
import json, os, sys
from pathlib import Path

# ── 文件类型分类（仅基于扩展名和命名，不涉及功能判断）──
EXT_TYPE_MAP = {
    ".py": "python", ".md": "markdown", ".txt": "text",
    ".json": "json", ".yaml": "yaml", ".yml": "yaml",
    ".toml": "toml", ".ini": "ini", ".cfg": "config",
    ".html": "html", ".css": "css", ".js": "javascript",
    ".svg": "svg", ".png": "image", ".jpg": "image", ".jpeg": "image",
    ".ico": "image", ".zip": "archive",
    ".sh": "shell", ".bat": "batch", ".ps1": "powershell",
    ".drawio": "drawio",
}

def scan(skill_dir: str) -> dict:
    skill_path = Path(skill_dir).resolve()
    result = {
        "skill_root": str(skill_path),
        "files": [],
        "tree": [],
    }

    for root, dirs, files in os.walk(skill_path):
        rel_root = Path(root).relative_to(skill_path)
        for f in sorted(files):
            fp = Path(root) / f
            rel = str((rel_root / f).as_posix())
            stat = fp.stat()
            ext = fp.suffix.lower()

            entry = {
                "path": rel,
                "ext": ext,
                "type": EXT_TYPE_MAP.get(ext, "other"),
                "size": stat.st_size,
                "lines": 0,
                "is_hidden": any(part.startswith(".") for part in fp.relative_to(skill_path).parts),
                "samples": [],
            }

            # 行数 + 内容采样：只取含 = : @ http \\ / 的行（看起来不像是纯代码的）
            if stat.st_size > 0 and stat.st_size < 500_000:  # 跳过二进制/大文件
                try:
                    with open(fp, encoding="utf-8", errors="replace") as fh:
                        lines = fh.readlines()
                    entry["lines"] = len(lines)
                    for lineno, line in enumerate(lines, 1):
                        stripped = line.strip()
                        if not stripped or len(stripped) < 8:
                            continue
                        # "不像纯代码"的启发式采样
                        if any(kw in stripped.lower() for kw in ["token", "password", "secret", "api_key", "apikey"]):
                            entry["samples"].append({"line": lineno, "content": stripped[:120]})
                        elif "@" in stripped and "." in stripped.split("@")[-1]:
                            entry["samples"].append({"line": lineno, "content": stripped[:120]})
                        elif stripped.startswith(("http://", "https://", "git@")):
                            entry["samples"].append({"line": lineno, "content": stripped[:120]})
                        elif "\\" in stripped or (stripped[1:2] == ":" and stripped[2:3] == "\\"):
                            entry["samples"].append({"line": lineno, "content": stripped[:120]})
                        elif "=" in stripped and not stripped.strip().startswith(("#", "//", "/*", "*")):
                            # 赋值语句且不是注释
                            key = stripped.split("=")[0].strip()
                            val = stripped.split("=", 1)[1].strip()
                            if key and val and len(key) < 40 and len(val) < 100 and not val.startswith(("'", '"')):
                                entry["samples"].append({"line": lineno, "content": stripped[:120]})
                        elif ": " in stripped and not stripped.strip().startswith(("#", "//", "/*", "*")):
                            entry["samples"].append({"line": lineno, "content": stripped[:120]})
                except Exception:
                    pass

            result["files"].append(entry)

        # 目录树（只记录目录结构，方便 LLM 看层级）
        for d in sorted(dirs):
            rel_d = str((rel_root / d).as_posix()) if str(rel_root) != "." else d
            result["tree"].append({
                "path": rel_d + "/",
                "is_hidden": d.startswith("."),
            })

    return result


def main():
    if len(sys.argv) < 2:
        print("用法: python blueprint_scan.py <skill_dir> [output_path]")
        sys.exit(1)
    skill_dir = sys.argv[1]
    output = sys.argv[2] if len(sys.argv) > 2 else ""
    result = scan(skill_dir)
    content = json.dumps(result, ensure_ascii=False, indent=2)
    if output:
        Path(output).write_text(content, encoding="utf-8")
    else:
        print(content)


if __name__ == "__main__":
    main()
