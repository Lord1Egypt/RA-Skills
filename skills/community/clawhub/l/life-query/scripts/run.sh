#!/usr/bin/env bash
# 统一执行引擎：调度 apis/*.sh 脚本
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
API_DIR="$SCRIPT_DIR"

usage() {
  echo "用法:"
  echo "  bash run.sh list                        # 列出所有可用接口"
  echo "  bash run.sh call <接口名> [参数...]      # 调用指定接口"
  echo "  bash run.sh show <接口名>               # 查看接口源码"
  echo ""
  echo "参数格式: --key value 或 --flag（布尔）"
  echo "输出格式: --format table|json（默认 json）"
}

cmd="${1:-}"
case "$cmd" in
  list)
    echo "可用接口："
    python3 -c "
import os, sys, re
api_dir = sys.argv[1]
rows = []
for f in sorted(os.listdir(api_dir)):
    if not f.endswith('.sh') or f == 'run.sh':
        continue
    name = f[:-3]
    desc = ''
    with open(os.path.join(api_dir, f)) as fp:
        for line in fp:
            m = re.match(r'^#\s*description:\s*(.+)', line)
            if m:
                desc = m.group(1).strip()
                break
    rows.append((name, desc))
if rows:
    w0 = max(len(r[0]) for r in rows)
    for name, desc in rows:
        print(f'  {name:<{w0}}  {desc}')
" "$API_DIR"
    ;;

  show)
    name="${2:-}"
    [ -z "$name" ] && { echo "错误: 请指定接口名"; exit 1; }
    sh_file="$API_DIR/$name.sh"
    [ ! -f "$sh_file" ] && { echo "错误: 接口 '$name' 不存在"; exit 1; }
    cat "$sh_file"
    ;;

  call)
    name="${2:-}"
    [ -z "$name" ] && { echo "错误: 请指定接口名"; exit 1; }
    shift 2

    if [ -f "$API_DIR/$name.sh" ]; then
      bash "$API_DIR/$name.sh" "$@"
    else
      echo "错误: 接口 '$name' 不存在，运行 'bash run.sh list' 查看可用接口" >&2
      exit 1
    fi
    ;;

  *)
    usage
    ;;
esac
