#!/usr/bin/env bash

FRIDA_SCRIPT_DIR="$HOME/.claude/skills/mobile-master/scripts"
package="$1"
script="$2"

if [ -z "$package" ]; then
  echo "Usage: $0 <包名> [脚本名]"
  exit 1
fi

cmd="frida -U -f $package "

if [ -n "$script" ]; then
  cmd="$cmd -l $FRIDA_SCRIPT_DIR/$script"
fi

$cmd