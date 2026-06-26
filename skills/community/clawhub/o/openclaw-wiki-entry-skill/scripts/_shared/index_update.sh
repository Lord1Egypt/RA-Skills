#!/bin/bash
set -eu

VAULT="${OPENCLAW_VAULT:-$(pwd)}"
COMMAND="${1:-}"
WIKI=""
CATEGORY=""
SOURCES=""
DATE_VALUE=""
INDEX_REL="Knowledge/_INDEX.md"

usage() {
  cat <<'EOF'
用法:
  index_update.sh update --wiki <主题> --sources <N> --date <YYYY-MM-DD> [--index-file <path>] [--vault <path>]
  index_update.sh add --wiki <主题> --category <分类> --sources <N> --date <YYYY-MM-DD> [--index-file <path>] [--vault <path>]
  index_update.sh sync-count [--index-file <path>] [--vault <path>]
EOF
}

if [ -z "$COMMAND" ]; then
  usage
  exit 1
fi
shift

while [ "$#" -gt 0 ]; do
  case "$1" in
    --wiki)
      WIKI="$2"; shift 2 ;;
    --category)
      CATEGORY="$2"; shift 2 ;;
    --sources)
      SOURCES="$2"; shift 2 ;;
    --date)
      DATE_VALUE="$2"; shift 2 ;;
    --index-file)
      INDEX_REL="$2"; shift 2 ;;
    --vault)
      VAULT="$2"; shift 2 ;;
    *)
      echo "未知参数: $1"
      usage
      exit 1 ;;
  esac
done

case "$COMMAND" in
  update)
    if [ -z "$WIKI" ] || [ -z "$SOURCES" ] || [ -z "$DATE_VALUE" ]; then
      usage
      exit 1
    fi
    ;;
  add)
    if [ -z "$WIKI" ] || [ -z "$CATEGORY" ] || [ -z "$SOURCES" ] || [ -z "$DATE_VALUE" ]; then
      usage
      exit 1
    fi
    ;;
  sync-count)
    ;;
  *)
    echo "未知命令: $COMMAND"
    usage
    exit 1 ;;
esac

python3 - "$COMMAND" "$VAULT" "$INDEX_REL" "$WIKI" "$CATEGORY" "$SOURCES" "$DATE_VALUE" <<'PY'
from __future__ import annotations

from datetime import date
import os
from pathlib import Path
import re
import shutil
import sys
import tempfile

command, vault, index_rel, wiki, category, sources_raw, date_value = sys.argv[1:8]
rollback_dir_override = os.environ.get("INDEX_UPDATE_ROLLBACK_DIR", "")


def fail(message: str) -> None:
    print(f"❌ {message}", file=sys.stderr)
    raise SystemExit(1)


def resolve_path(vault_root: str, path_value: str) -> Path:
    path = Path(path_value)
    if path.is_absolute():
        return path
    return Path(vault_root) / path


index_path = resolve_path(vault, index_rel)
if not index_path.is_file():
    fail(f"_INDEX.md 不存在: {index_path}")

sources = None
if command in {"update", "add"}:
    if not re.fullmatch(r"[1-9][0-9]*", sources_raw):
        fail("--sources 必须是正整数")
    sources = int(sources_raw)
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", date_value):
        fail("--date 格式必须是 YYYY-MM-DD")
    try:
        date.fromisoformat(date_value)
    except ValueError:
        fail("--date 不是合法日期")

content = index_path.read_text(encoding="utf-8")
lines = content.splitlines(keepends=True)

TOPIC_ROW_RE = re.compile(
    r"^\|\s*(?P<wiki>[^|]+?)\s*\|\s*\[\[(?P<link>[^\]]+)\]\]\s*\|\s*(?P<sources>0|[1-9][0-9]*)\s*篇\s*\|\s*(?P<date>\d{4}-\d{2}-\d{2})\s*\|\s*active\s*\|\s*$"
)


def find_frontmatter_bounds(items: list[str]) -> tuple[int, int]:
    markers = [idx for idx, line in enumerate(items[:40]) if line.strip() == "---"]
    if len(markers) < 2 or markers[0] != 0:
        fail("frontmatter 格式异常")
    return markers[0], markers[1]


def read_topics_count(items: list[str]) -> tuple[int, int]:
    start, end = find_frontmatter_bounds(items)
    for idx in range(start + 1, end):
        match = re.match(r"^topics_count:\s*([0-9]+)\s*$", items[idx].strip())
        if match:
            return idx, int(match.group(1))
    fail("frontmatter 缺少 topics_count")


def write_topics_count(items: list[str], value: int) -> None:
    idx, _ = read_topics_count(items)
    suffix = "\n" if items[idx].endswith("\n") else ""
    items[idx] = f"topics_count: {value}{suffix}"


def find_topic_section(items: list[str]) -> tuple[int, int]:
    start = None
    for idx, line in enumerate(items):
        if line.strip() == "## 主题目录":
            start = idx
            break
    if start is None:
        fail("找不到 ## 主题目录")

    end = len(items)
    for idx in range(start + 1, len(items)):
        if items[idx].startswith("## "):
            end = idx
            break
    return start, end


def count_topic_rows(items: list[str]) -> int:
    start, end = find_topic_section(items)
    total = 0
    for line in items[start + 1:end]:
        if TOPIC_ROW_RE.fullmatch(line.strip()):
            total += 1
    return total


def find_topic_matches(items: list[str], target_wiki: str) -> list[tuple[int, re.Match[str]]]:
    start, end = find_topic_section(items)
    matches: list[tuple[int, re.Match[str]]] = []
    for idx in range(start + 1, end):
        line = items[idx].strip()
        match = TOPIC_ROW_RE.fullmatch(line)
        if not match:
            continue
        if match.group("wiki") == target_wiki:
            matches.append((idx, match))
    return matches


def backup_file(path: Path) -> None:
    rollback_dir = Path(rollback_dir_override) if rollback_dir_override else Path(os.environ.get("TMPDIR", "/tmp")) / "openclaw_index_rollback"
    rollback_dir.mkdir(parents=True, exist_ok=True)
    timestamp = date.today().strftime("%Y%m%d")
    fd, tmp_name = tempfile.mkstemp(prefix=f"{path.name}.{timestamp}.", suffix=".bak", dir=str(rollback_dir))
    os.close(fd)
    shutil.copy2(path, tmp_name)


def write_atomic(path: Path, items: list[str]) -> None:
    fd, tmp_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write("".join(items))
        os.replace(tmp_name, path)
    except Exception:
        try:
            os.remove(tmp_name)
        except FileNotFoundError:
            pass
        raise


backup_file(index_path)

if command == "update":
    matches = find_topic_matches(lines, wiki)
    if not matches:
        fail(f"update 找不到匹配行: {wiki}")
    if len(matches) > 1:
        fail(f"update 匹配到多行，拒绝继续: {wiki}")

    row_idx, match = matches[0]
    old_sources = int(match.group("sources"))
    old_date = match.group("date")
    suffix = "\n" if lines[row_idx].endswith("\n") else ""
    lines[row_idx] = f"| {wiki} | [[{wiki}]] | {sources} 篇 | {date_value} | active |{suffix}"
    write_atomic(index_path, lines)
    print(f'✅ update: "{wiki}" sources {old_sources}→{sources}, date {old_date}→{date_value}')
elif command == "add":
    if find_topic_matches(lines, wiki):
        fail(f"add 主题已存在: {wiki}")

    start, end = find_topic_section(lines)
    category_idx = None
    for idx in range(start + 1, end):
        if lines[idx].strip() == f"### {category}":
            category_idx = idx
            break
    if category_idx is None:
        fail(f"add 找不到分类: {category}")

    insert_idx = None
    for idx in range(category_idx + 1, end):
        stripped = lines[idx].strip()
        if stripped.startswith("### "):
            fail(f"分类缺少 **关键词** 行: {category}")
        if stripped.startswith("**关键词**："):
            insert_idx = idx
            break
    if insert_idx is None:
        fail(f"分类缺少 **关键词** 行: {category}")

    _, old_topics_count = read_topics_count(lines)
    lines.insert(insert_idx, f"| {wiki} | [[{wiki}]] | {sources} 篇 | {date_value} | active |\n")
    write_topics_count(lines, old_topics_count + 1)
    write_atomic(index_path, lines)
    print(f'✅ add: "{wiki}" → "{category}", sources={sources}, topics_count {old_topics_count}→{old_topics_count + 1}')
else:
    _, old_topics_count = read_topics_count(lines)
    new_topics_count = count_topic_rows(lines)
    write_topics_count(lines, new_topics_count)
    write_atomic(index_path, lines)
    print(f"✅ sync-count: topics_count {old_topics_count}→{new_topics_count}")

final_lines = index_path.read_text(encoding="utf-8").splitlines(keepends=True)
_, final_topics_count = read_topics_count(final_lines)
actual_topics_count = count_topic_rows(final_lines)
if final_topics_count != actual_topics_count:
    print(
        f"⚠️ warning: topics_count {final_topics_count} != actual {actual_topics_count}",
        file=sys.stderr,
    )
PY
