#!/usr/bin/env bash

FRIDA_SCRIPT_DIR="$HOME/.claude/skills/mobile-master/scripts"
input="$1"
script="$2"

if [ -z "$input" ]; then
  echo "Usage: $0 <PID/包名/应用名> [脚本名]"
  exit 1
fi

# 检查是否是纯数字PID
if [[ "$input" =~ ^[0-9]+$ ]]; then
  pid="$input"
else
  # 通过包名或应用名查找PID
  pid=$(frida-ps -Uai | grep -i "$input" | head -1 | awk '{print $2}')
  if [ -z "$pid" ]; then
    echo "未找到进程: $input"
    exit 1
  fi
fi

cmd="frida -U -p $pid"

if [ -n "$script" ]; then
  cmd="$cmd -l $FRIDA_SCRIPT_DIR/$script"
fi

$cmd
