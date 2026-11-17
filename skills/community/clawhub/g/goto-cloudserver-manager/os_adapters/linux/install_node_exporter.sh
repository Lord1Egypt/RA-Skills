#!/bin/bash
# install_node_exporter.sh - 安装 Prometheus Node Exporter
set -euo pipefail

NODE_EXPORTER_VERSION="${1:-1.7.0}"
PORT="${2:-9100}"

log() { echo "[$(date '+%H:%M:%S')] $*"; }

# 检查是否已安装
if systemctl is-active node_exporter &>/dev/null; then
    log "node_exporter 已运行，跳过安装"
    exit 0
fi

log "下载 node_exporter v$NODE_EXPORTER_VERSION..."
ARCH=$(uname -m | sed 's/x86_64/amd64/;s/aarch64/arm64/')
DOWNLOAD_URL="https://github.com/prometheus/node_exporter/releases/download/v${NODE_EXPORTER_VERSION}/node_exporter-${NODE_EXPORTER_VERSION}.linux-${ARCH}.tar.gz"
TMPDIR=$(mktemp -d)

curl -fsSL "$DOWNLOAD_URL" -o "$TMPDIR/node_exporter.tar.gz"
tar -xzf "$TMPDIR/node_exporter.tar.gz" -C "$TMPDIR"
cp "$TMPDIR/node_exporter-${NODE_EXPORTER_VERSION}.linux-${ARCH}/node_exporter" /usr/local/bin/
chmod +x /usr/local/bin/node_exporter
rm -rf "$TMPDIR"

# 创建 systemd 服务
cat > /etc/systemd/system/node_exporter.service << EOF
[Unit]
Description=Prometheus Node Exporter
After=network.target

[Service]
User=nobody
ExecStart=/usr/local/bin/node_exporter --web.listen-address=:${PORT}
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable node_exporter
systemctl start node_exporter

# 防火墙（仅内网监控系统访问）
if command -v firewall-cmd &>/dev/null; then
    firewall-cmd --add-port="${PORT}/tcp" --zone=internal --permanent
    firewall-cmd --reload
elif command -v ufw &>/dev/null; then
    ufw allow from 10.0.0.0/8 to any port "$PORT"
fi

log "node_exporter 安装完成，端口：$PORT"
exit 0
