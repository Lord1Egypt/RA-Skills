#!/bin/sh
set -eu

script_dir="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
# 用 sh 显式调用，不依赖 bootstrap.sh 的执行位：有些宿主解压技能包时
# 不保留文件权限，直接执行会以“Permission denied”中断整个流程。
node_bin="$(sh "$script_dir/bootstrap.sh" --print-node)"
exec "$node_bin" "$script_dir/legal-skill.mjs" "$@"
