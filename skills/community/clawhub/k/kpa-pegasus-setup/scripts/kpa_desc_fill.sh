#!/usr/bin/env bash
# kpa_desc_fill.sh —— 把中文简介库回填进天马 metadata.pegasus.txt
#
# 用法：
#   ./kpa_desc_fill.sh --json zh_desc.json --meta-dir /path/to/Roms           # dry-run
#   ./kpa_desc_fill.sh --json zh_desc.json --meta-dir /path/to/Roms --apply    # 真写（自动 .bak）
#
# 简介库格式：{"PS": {"游戏名": "简介"}, "NDS": {...}}
# 只会替换 description 行，不动其它字段；--apply 前会对每个被改文件做 .bak 备份。
set -euo pipefail

JSON=""
DIR=""
APPLY=0
SUFFIX="bak$(date +%Y%m%d)"

while [ $# -gt 0 ]; do
  case "$1" in
    --json) JSON="$2"; shift 2 ;;
    --meta-dir) DIR="$2"; shift 2 ;;
    --suffix) SUFFIX="$2"; shift 2 ;;
    --apply) APPLY=1; shift ;;
    -h|--help) sed -n '2,12p' "$0"; exit 0 ;;
    *) echo "未知参数：$1" >&2; exit 2 ;;
  esac
done

[ -n "$JSON" ] && [ -n "$DIR" ] || { echo "缺少 --json 或 --meta-dir" >&2; exit 2; }

python3 - "$JSON" "$DIR" "$APPLY" "$SUFFIX" <<'PY'
import json, os, re, sys

lib_path, meta_dir, apply, suffix = sys.argv[1], sys.argv[2], sys.argv[3] == "1", sys.argv[4]
lib = json.load(open(lib_path, encoding="utf-8"))

total_replace = 0
missing = []
touched = []

for plat, mapping in lib.items():
    path = os.path.join(meta_dir, plat, "metadata.pegasus.txt")
    if not os.path.exists(path):
        missing.append(f"[文件不存在] {plat}")
        continue
    raw = open(path, encoding="utf-8").read()
    lines = raw.split("\n")
    idx = [i for i, l in enumerate(lines) if l.startswith("game:")]
    header = lines[:idx[0]] if idx else lines
    bounds = idx + [len(lines)]
    blocks = ["\n".join(lines[bounds[k]:bounds[k + 1]]).rstrip("\n") for k in range(len(idx))]

    tried, out_blocks, changed = set(), [], 0
    for b in blocks:
        bl = b.split("\n")
        title = bl[0][5:].strip()
        tried.add(title)
        if title in mapping:
            newd = "description: " + mapping[title]
            di = next((i for i, l in enumerate(bl) if l.startswith("description:")), -1)
            if di >= 0:
                if bl[di] != newd:
                    bl[di] = newd; changed += 1
            else:
                bl.append(newd); changed += 1
        out_blocks.append("\n".join(bl))

    for t in mapping:
        if t not in tried:
            missing.append(f"{plat}/{t}")

    if changed:
        total_replace += changed
        new = "\n".join(header) + "\n" + "\n".join(out_blocks)
        touched.append((path, changed))
        if apply:
            if not os.path.exists(path + "." + suffix):
                open(path + "." + suffix, "w", encoding="utf-8").write(raw)
            open(path, "w", encoding="utf-8").write(new)

print(("已写入" if apply else "将写入") + f" {total_replace} 条简介，涉及 {len(touched)} 个平台文件")
for p, n in touched:
    print(f"  {os.path.basename(os.path.dirname(p)):<12} {n} 条")
if missing:
    print(f"未匹配 {len(missing)} 条：")
    for m in missing:
        print("  -", m)
if apply and touched:
    print("\n提示：天马使用 /sdcard/pegasus-frontend/dataCache.json 缓存，改完必须删缓存并重启才会生效。")
PY
