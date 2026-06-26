#!/bin/bash
# plan3-cloud-gateway.sh - 方案三：云端网关完整部署（含同步备份）
# 用法：curl -O https://.../plan3-cloud-gateway.sh && bash plan3-cloud-gateway.sh

set -e

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║     方案三：云端网关 + 本地网关双部署                              ║"
echo "║                  云端网关完整部署（含同步备份）                  ║"
echo "╚════════════════════════════════════════════════════════════════╝"

# 系统检测
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$ID
else
    echo "✗ 无法识别系统"
    exit 1
fi

if [ "$EUID" -ne 0 ]; then
    echo "✗ 请使用 root 权限运行"
    exit 1
fi

# 1. Tailscale
echo -e "\n[1/7] 配置 Tailscale..."
if ! command -v tailscale &> /dev/null; then
    curl -fsSL https://tailscale.com/install.sh | sh
fi
systemctl enable --now tailscaled 2>/dev/null || tailscaled &
sleep 3
TAILSCALE_IP=$(tailscale ip | head -1)
echo "  ✓ Tailscale: $TAILSCALE_IP"

# 2. 防火墙
echo -e "\n[2/7] 配置防火墙..."
if command -v ufw &> /dev/null && ufw status | grep -q "active"; then
    ufw allow 18789/tcp comment "OpenClaw Gateway"
    ufw allow 18790/tcp comment "OpenClaw Sync"
    echo "  ✓ UFW: 18789, 18790 已放行"
elif command -v firewall-cmd &> /dev/null && systemctl is-active --quiet firewalld; then
    firewall-cmd --permanent --add-port=18789/tcp
    firewall-cmd --permanent --add-port=18790/tcp
    firewall-cmd --reload
    echo "  ✓ Firewalld: 18789, 18790 已放行"
fi
echo "  ⚠ 云服务器安全组需手动放行 18789, 18790"

# 3. Node.js
echo -e "\n[3/7] 配置 Node.js..."
if ! command -v node &> /dev/null; then
    if [ "$OS" = "ubuntu" ] || [ "$OS" = "debian" ]; then
        curl -fsSL https://deb.nodesource.com/setup_22.x | bash -
        apt-get install -y nodejs
    fi
fi
echo "  ✓ Node.js: $(node -v)"

# 4. OpenClaw
echo -e "\n[4/7] 安装 OpenClaw..."
npm install -g openclaw --registry=https://registry.npmmirror.com
echo "  ✓ OpenClaw: 已安装"

# 5. 配置
echo -e "\n[5/7] 配置网关（含同步）..."
mkdir -p ~/.openclaw

# 生成同步 Token
SYNC_TOKEN=$(openssl rand -hex 20)

cat > ~/.openclaw/openclaw.json << EOF
{
  "gateway": {
    "port": 18789,
    "mode": "local",
    "bind": "lan"
  },
  "sync": {
    "enabled": true,
    "port": 18790,
    "token": "$SYNC_TOKEN",
    "direction": "bidirectional",
    "interval": 300
  }
}
EOF

echo "  ✓ 配置文件：~/.openclaw/openclaw.json"
echo "  同步 Token: $SYNC_TOKEN"

# 6. systemd 服务
echo -e "\n[6/7] 创建 systemd 服务..."

cat > /etc/systemd/system/openclaw-gateway.service << 'EOF'
[Unit]
Description=OpenClaw Gateway (with Sync)
After=network.target tailscaled.service
Wants=tailscaled.service

[Service]
Type=simple
User=root
WorkingDirectory=/root/.openclaw
ExecStart=/usr/bin/node /usr/lib/node_modules/openclaw/dist/index.js gateway --port 18789 --bind lan
Restart=always
Environment=NODE_ENV=production

LimitNOFILE=65535
Nice=-5

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable openclaw-gateway
systemctl start openclaw-gateway

sleep 5

# 7. 验证
echo -e "\n[7/7] 验证服务..."

echo -e "\n╔════════════════════════════════════════════════════════════════╗"
if systemctl is-active --quiet openclaw-gateway; then
    echo "║                     ✓ 部署成功                                 ║"
    echo "╚════════════════════════════════════════════════════════════════╝"

    echo -e "\n【服务信息】"
    echo "  服务状态：$(systemctl is-active openclaw-gateway)"
    echo "  开机自启：$(systemctl is-enabled openclaw-gateway)"

    echo -e "\n【网络信息】"
    echo "  Tailscale IP: $TAILSCALE_IP"
    echo "  网关地址：ws://${TAILSCALE_IP}:18789"
    echo "  同步端口：${TAILSCALE_IP}:18790"

    echo -e "\n【端口监听】"
    ss -tlnp | grep -E "18789|18790" || true

    echo -e "\n【下一步操作】"
    echo "  1. 在本地运行 plan3-local-gateway.ps1"
    echo "  2. 配置双向同步：openclaw sync config"
    echo "  3. 查看同步状态：openclaw sync status"
else
    echo "║                     ✗ 部署失败                                 ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
    journalctl -u openclaw-gateway --no-pager -n 20
    exit 1
fi
