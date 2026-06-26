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
  echo "直接使用 PID: $pid"
else
  # 通过 frida-ps -Uai 根据输入查找包名
  # 输出格式: -  AppName  package.name
  package=$(frida-ps -Uai | grep -i "$input" | head -1 | awk '{print $NF}')
  if [ -z "$package" ]; then
    echo "未找到应用: $input"
    exit 1
  fi
  echo "找到包名: $package"

  # 通过 frida-ps -Ua 查找运行中的进程 PID
  pid=$(frida-ps -Ua | grep -i "$package" | head -1 | awk '{print $1}')

  if [ -z "$pid" ]; then
    # 进程未启动，尝试启动应用
    echo "进程未启动，正在启动..."

    # 先尝试找到 launcher activity
    launch_activity=$(adb shell dumpsys package "$package" 2>/dev/null | \
      grep -A 5 "android.intent.action.MAIN" | grep -m 1 "$package/" | awk '{print $1}')

    if [ -n "$launch_activity" ]; then
      adb shell am start -n "$launch_activity" > /dev/null 2>&1
    else
      # 使用 monkey 方式启动
      adb shell monkey -p "$package" -c android.intent.category.LAUNCHER 1 > /dev/null 2>&1
    fi

    # 等待进程启动
    echo "等待进程启动..."
    sleep 3

    # 重新获取 PID
    pid=$(frida-ps -Ua | grep -i "$package" | head -1 | awk '{print $1}')

    if [ -z "$pid" ]; then
      echo "无法获取进程 PID，应用可能启动失败"
      exit 1
    fi
  fi

  echo "使用 PID: $pid"
fi

mkdir -p "./dexdump/"

cmd="frida-dexdump -U -p $pid -o ./dexdump"

if [ -n "$script" ]; then
  cmd="$cmd -l $FRIDA_SCRIPT_DIR/$script"
fi

$cmd
