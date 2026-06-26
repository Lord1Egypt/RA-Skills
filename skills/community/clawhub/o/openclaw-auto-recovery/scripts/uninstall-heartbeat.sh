#!/bin/bash
# 卸载 infra-heartbeat
set -euo pipefail

SYSTEMD_DIR="${HOME}/.config/systemd/user"
SERVICE_FILE="${SYSTEMD_DIR}/heartbeat-daemon.service"
CONFIG_DIR="${HOME}/.config/infra-heartbeat"
LOG_DIR="${HOME}/.openclaw/workspace-infra"

echo "⚠️  即将卸载 infra-heartbeat"
echo ""
echo "将执行:"
echo "  1. 停止 systemd 服务"
echo "  2. 禁用服务"
echo "  3. 删除 service 文件"
echo "  4. 删除配置文件 (可选)"
echo ""
echo -n "是否删除配置文件和日志? [y/N]: "
read -r confirm_config

systemctl --user stop heartbeat-daemon.service 2>/dev/null || true
systemctl --user disable heartbeat-daemon.service 2>/dev/null || true
systemctl --user daemon-reload

rm -f "$SERVICE_FILE"
echo "✅ Service 文件已删除"

if [[ "$confirm_config" =~ ^[Yy]$ ]]; then
    rm -rf "$CONFIG_DIR"
    echo "✅ 配置目录已删除"
    rm -f "${LOG_DIR}/heartbeat.log" "${LOG_DIR}/alerts.log" "${LOG_DIR}/restart-fail-count"
    echo "✅ 日志文件已删除"
fi

echo ""
echo "✅ 卸载完成"
echo "注意: heartbeat-daemon.sh 仍在 skill 目录中，如需完全删除请手动移除"
