#!/bin/bash
set -e
REPORT="$(date +%F)"
OUT_FILE="$(pwd)/memory/healthcheck-${REPORT}.md"
{
  echo "# 本地安全检查报告 ${REPORT}"
  echo "\n## 防火墙状态"
  if command -v firewallctl >/dev/null 2>&1; then
    firewallctl status || echo "无法获取防火墙状态"
  elif [[ "$OSTYPE" == "darwin"* ]]; then
    /usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate || echo "防火墙状态未知"
  else
    sudo ufw status || echo "防火墙状态未知"
  fi
  echo "\n## 打开的端口"
  if [[ "$OSTYPE" == "darwin"* ]]; then
    sudo lsof -nP -iTCP -sTCP:LISTEN | awk 'NR>1 {print $9}' | sort | uniq
  else
    sudo ss -tuln
  fi
  echo "\n## 系统软件更新"
  if [[ "$OSTYPE" == "darwin"* ]]; then
    softwareupdate -l || echo "更新检查失败"
  else
    sudo apt list --upgradable 2>/dev/null || echo "更新检查失败"
  fi
  echo "\n## SSH 服务状态"
  if pgrep -x sshd >/dev/null; then
    echo "sshd 正在运行"
  else
    echo "sshd 未运行"
  fi
} > "$OUT_FILE"

echo "报告已写入 $OUT_FILE"
