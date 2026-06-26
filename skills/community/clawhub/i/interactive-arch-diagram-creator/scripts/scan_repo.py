"""
scan_repo.py
────────────────────────────────────────────────────────────────
扫描代码仓，输出每个代码文件的路径和内容，供 Claude 批量生成摘要。
同时统计文件数、按技术栈分布、总代码行数（LOC），写入 --stats-output。

用法：
  python scan_repo.py <repo_path> [--cache <cache_file>] [--skip-cache]
                      [--stats-output <stats_file>]

输出（stdout）：
  JSON 对象，source="scan"|"cache"，含 files 或 summary 字段
  如果 cache_file 存在且未指定 --skip-cache，则输出已有缓存并附带标记

--stats-output：
  将仓库元信息写入指定 JSON 文件，格式：
  {
    "repo_name": "项目名",
    "file_count": 42,
    "total_loc": 3800,
    "tech_stack": [{"lang": "Python", "count": 20, "loc": 1500}, ...]
  }

退出码：
  0 = 成功
  1 = 路径不存在或无代码文件
"""

import argparse
import json
import os
import sys
from collections import defaultdict
from pathlib import Path

CODE_FILE_EXTENSIONS = {
    "py", "js", "ts", "jsx", "tsx", "mjs", "cjs",
    "java", "kt", "scala", "c", "cpp", "cc", "cxx",
    "h", "hpp", "cs", "go", "rs", "rb", "php",
    "swift", "sh", "bash", "vue",
}

# 扩展名 → 显示语言名
EXT_TO_LANG = {
    "py": "Python",
    "js": "JavaScript", "mjs": "JavaScript", "cjs": "JavaScript",
    "ts": "TypeScript",
    "jsx": "React/JSX", "tsx": "React/TSX",
    "vue": "Vue",
    "java": "Java",
    "kt": "Kotlin",
    "scala": "Scala",
    "c": "C", "h": "C",
    "cpp": "C++", "cc": "C++", "cxx": "C++", "hpp": "C++",
    "cs": "C#",
    "go": "Go",
    "rs": "Rust",
    "rb": "Ruby",
    "php": "PHP",
    "swift": "Swift",
    "sh": "Shell", "bash": "Shell",
}

IGNORE_DIRS = {
    ".git", ".svn", "node_modules", "__pycache__", ".venv", "venv",
    "env", "dist", "build", "target", ".idea", ".vscode", "vendor",
    ".mypy_cache", ".pytest_cache", "coverage", ".tox",
}


def count_loc(content: str) -> int:
    """统计有效代码行数（非空、非纯注释行）"""
    count = 0
    for line in content.splitlines():
        stripped = line.strip()
        if stripped and not stripped.startswith(("#", "//", "*", "/*", "*/", "--", "<!--", "-->")):
            count += 1
    return count


def scan_repo(repo_path: str) -> tuple[list, dict]:
    """递归扫描代码文件，返回 (files列表, stats字典)"""
    root = Path(repo_path).resolve()
    if not root.is_dir():
        print(f"ERROR: 路径不存在或不是目录: {repo_path}", file=sys.stderr)
        sys.exit(1)

    results = []
    lang_file_count: dict[str, int] = defaultdict(int)
    lang_loc_count:  dict[str, int] = defaultdict(int)
    total_loc = 0

    for dirpath, dirnames, filenames in os.walk(root):
        # 过滤忽略目录（就地修改 dirnames 以阻止 os.walk 递归进去）
        dirnames[:] = [d for d in dirnames if d not in IGNORE_DIRS and not d.startswith(".")]

        for filename in sorted(filenames):
            ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
            if ext not in CODE_FILE_EXTENSIONS:
                continue

            full_path = Path(dirpath) / filename
            # 相对于 repo_path 的父目录（保留项目名作为前缀，与原项目一致）
            try:
                rel_path = full_path.relative_to(root.parent).as_posix()
            except ValueError:
                rel_path = full_path.relative_to(root).as_posix()

            try:
                content = full_path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                try:
                    content = full_path.read_text(encoding="gbk", errors="ignore")
                except Exception:
                    content = ""
            except Exception:
                content = ""

            loc = count_loc(content)
            lang = EXT_TO_LANG.get(ext, ext.upper())
            lang_file_count[lang] += 1
            lang_loc_count[lang]  += loc
            total_loc += loc

            results.append({"file_name": rel_path, "content": content})

    # 技术栈排序：按文件数降序，取前 8 个
    tech_stack = sorted(
        [{"lang": lang, "count": lang_file_count[lang], "loc": lang_loc_count[lang]}
         for lang in lang_file_count],
        key=lambda x: x["count"],
        reverse=True,
    )[:8]

    stats = {
        "repo_name": root.name,
        "file_count": len(results),
        "total_loc": total_loc,
        "tech_stack": tech_stack,
    }

    return results, stats


def main():
    parser = argparse.ArgumentParser(description="扫描代码仓，输出文件内容供 Claude 批量生成摘要")
    parser.add_argument("repo_path", help="代码仓目录路径")
    parser.add_argument("--cache", default="", help="缓存文件路径（已有摘要的 JSON）")
    parser.add_argument("--skip-cache", action="store_true", help="忽略已有缓存，重新扫描")
    parser.add_argument("--stats-output", default="", help="将仓库统计元信息写入指定 JSON 文件")
    args = parser.parse_args()

    # 如果缓存存在且未强制跳过，直接返回缓存（仍需扫描一次以生成 stats）
    if args.cache and not args.skip_cache:
        cache_path = Path(args.cache)
        if cache_path.exists():
            with open(cache_path, encoding="utf-8") as f:
                cached = json.load(f)
            # 缓存命中时也需要统计 stats（如有 --stats-output）
            if args.stats_output:
                _, stats = scan_repo(args.repo_path)
                stats_path = Path(args.stats_output)
                stats_path.parent.mkdir(parents=True, exist_ok=True)
                stats_path.write_text(json.dumps(stats, ensure_ascii=False, indent=2), encoding="utf-8")
            output = {
                "source": "cache",
                "cache_file": str(cache_path),
                "summary": cached,
            }
            print(json.dumps(output, ensure_ascii=False, indent=2))
            return

    # 扫描代码文件
    files, stats = scan_repo(args.repo_path)
    if not files:
        print("ERROR: 未找到任何代码文件，请检查路径或文件类型", file=sys.stderr)
        sys.exit(1)

    # 写入 stats 文件
    if args.stats_output:
        stats_path = Path(args.stats_output)
        stats_path.parent.mkdir(parents=True, exist_ok=True)
        stats_path.write_text(json.dumps(stats, ensure_ascii=False, indent=2), encoding="utf-8")

    output = {
        "source": "scan",
        "repo_path": args.repo_path,
        "file_count": len(files),
        "files": files,
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
