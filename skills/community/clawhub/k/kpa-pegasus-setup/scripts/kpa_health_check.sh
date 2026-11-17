#!/bin/bash
# 全库静态校验（只读，不改设备、不污染包目录）。
#   bash kpa_health_check.sh                 # 设备在线：拉取 36 平台 metadata 并核对 ROM/封面存在性
#   bash kpa_health_check.sh --local [DIR]  # 离线：分析本机 metadata 目录（默认 assets/meta_latest）
set -euo pipefail

MODE=device
OUTPATH=""
if [ "${1:-}" = "--local" ]; then
  MODE=local
  DIR="${2:-$(cd "$(dirname "$0")/.." && pwd)/assets/meta_latest}"
else
  source "$(dirname "$0")/kpa_env.sh"
  require_device
  DIR=$(mktemp -d)
  OUTPATH=$(mktemp /tmp/kpa_check_paths.XXXXXX)
  trap 'rm -rf "$DIR" "$OUTPATH"' EXIT
  echo "== 拉取设备 metadata =="
  sh "find $TF/Roms -name metadata.pegasus.txt" | tr -d '\r' | while IFS= read -r p; do
    [ -n "$p" ] || continue
    plat=$(basename "$(dirname "$p")")
    "$ADB" exec-out cat "$p" > "$DIR/$plat.txt" 2>/dev/null || true
  done
fi

python3 - "$DIR" "$MODE" "$OUTPATH" <<'PY'
import sys, os, glob, collections
d, mode, out = sys.argv[1], sys.argv[2], sys.argv[3]
files = sorted(glob.glob(os.path.join(d, "*.txt")))
total, issues, paths, per_platform = 0, collections.Counter(), [], []
for f in files:
    plat = os.path.basename(f)[:-4]
    lines = open(f, encoding='utf-8-sig').read().splitlines()
    head_launch = any(l.startswith('launch:') for l in lines[:12])
    blocks, cur = [], None
    for line in lines:
        if line.startswith('game: '):
            if cur: blocks.append(cur)
            cur = {'game': line[6:].strip(), 'lines': []}
        elif cur is not None:
            cur['lines'].append(line)
    if cur: blocks.append(cur)
    seen_file, seen_name = set(), set()
    for b in blocks:
        total += 1
        kv = {}
        for l in b['lines']:
            if ': ' in l:
                k, v = l.split(': ', 1)
                kv.setdefault(k.strip(), v.strip())
        if not kv.get('launch') and not head_launch: issues['no_launch'] += 1
        if not kv.get('description'): issues['no_description'] += 1
        if not kv.get('assets.box_front'): issues['no_cover'] += 1
        fn = kv.get('file')
        if not fn:
            issues['no_file'] += 1
        else:
            if fn in seen_file: issues['duplicate_file'] += 1
            seen_file.add(fn)
            paths.append(f"{plat}/{fn}")
        if kv.get('assets.box_front'): paths.append(f"{plat}/{kv['assets.box_front']}")
        if b['game'] in seen_name: issues['duplicate_game'] += 1
        seen_name.add(b['game'])
    per_platform.append((plat, len(blocks)))
print(f"MODE={mode}  platforms={len(files)}  games={total}")
print("  " + "  ".join(f"{p}:{n}" for p, n in per_platform))
print("ISSUES:", dict(issues) if issues else "none")
if out:
    open(out, "w", encoding="utf-8").write("\n".join(paths) + "\n")
PY

if [ "$MODE" = device ]; then
  cat > /tmp/kpa_check_dev.sh <<'EOS'
#!/system/bin/sh
ROOT="$1"
n=0; miss=0
while IFS= read -r p; do
  [ -n "$p" ] || continue
  n=$((n+1))
  [ -e "$ROOT/$p" ] || { miss=$((miss+1)); [ "$miss" -le 20 ] && echo "MISSING $p"; }
done < /sdcard/kpa_check_paths.txt
echo "RESULT checked=$n missing=$miss"
EOS
  "$ADB" push "$OUTPATH" /sdcard/kpa_check_paths.txt >/dev/null
  "$ADB" push /tmp/kpa_check_dev.sh /sdcard/kpa_check_dev.sh >/dev/null
  echo "== 设备端 ROM / 封面存在性 =="
  sh "sh /sdcard/kpa_check_dev.sh '$TF/Roms'"
  sh "rm -f /sdcard/kpa_check_dev.sh /sdcard/kpa_check_paths.txt" >/dev/null
  rm -f /tmp/kpa_check_dev.sh
fi
echo "提示：达标线为各项 ISSUES = 0、竖版 cfg 精确 219；改过 metadata 后必须清 dataCache.json 再重启。"
