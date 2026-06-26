#!/bin/bash
# plan2-cloud-remote-gateway.sh - 方案二：云端远程网关完整部署（Remote 模式 + Token 认证）
# 用法：curl -O https://.../plan2-cloud-remote-gateway.sh && bash plan2-cloud-remote-gateway.sh

set -e

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║     方案二：云端网关 + Tailscale + 本地节点                       ║"
echo "║                  云端远程网关部署 (Remote 模式)                   ║"
echo "╚════════════════════════════════════════════════════════════════╝"

# ============== 1. 系统环境检测 ==============
echo -e "\n[1/7] 系统环境检测..."

if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$ID
    echo "  系统：$OS ($PRETTY_NAME)"
else
    echo "  ✗ 无法识别系统"
    exit 1
fi

if [ "$EUID" -ne 0 ]; then
    echo "  ✗ 请使用 root 权限运行"
    exit 1
fi
echo "  ✓ 权限检查通过 (root)"

# ============== 2. Tailscale 配置 ==============
echo -e "\n[2/7] 配置 Tailscale..."

if ! command -v tailscale &> /dev/null; then
    echo "  安装 Tailscale..."
    if [ "$OS" = "ubuntu" ] || [ "$OS" = "debian" ]; then
        curl -fsSL https://tailscale.com/install.sh | sh
    else
        echo "  ✗ 不支持的系统，请手动安装"
        exit 1
    fi
fi

systemctl enable --now tailscaled 2>/dev/null || tailscaled &
sleep 3

if tailscale status 2>&1 | grep -q "connected"; then
    TAILSCALE_IP=$(tailscale ip | head -1)
    echo "  ✓ Tailscale: 已连接 ($TAILSCALE_IP)"
else
    echo "  ⚠ Tailscale 未连接"
    echo "  运行：tailscale up"
    read -p "  完成后按回车..."
    TAILSCALE_IP=$(tailscale ip | head -1)
fi

# ============== 3. 防火墙配置 ==============
echo -e "\n[3/7] 配置防火墙..."

if command -v ufw &> /dev/null && ufw status | grep -q "Status: active"; then
    ufw allow 18789/tcp comment "OpenClaw Gateway"
    echo "  ✓ UFW: 18789/tcp 已放行"
elif command -v firewall-cmd &> /dev/null && systemctl is-active --quiet firewalld; then
    firewall-cmd --permanent --add-port=18789/tcp
    firewall-cmd --reload
    echo "  ✓ Firewalld: 18789/tcp 已放行"
fi

echo "  ⚠ 云服务器安全组需手动放行 18789 (Tailscale IP: $TAILSCALE_IP)"

# ============== 4. Node.js 配置 ==============
echo -e "\n[4/7] 配置 Node.js..."

if ! command -v node &> /dev/null; then
    echo "  安装 Node.js 22..."
    if [ "$OS" = "ubuntu" ] || [ "$OS" = "debian" ]; then
        curl -fsSL https://deb.nodesource.com/setup_22.x | bash -
        apt-get install -y nodejs
    else
        echo "  ✗ 不支持的系统"
        exit 1
    fi
fi
echo "  ✓ Node.js: $(node -v)"

npm config set registry https://registry.npmmirror.com 2>/dev/null || true

# ============== 5. OpenClaw 安装 ==============
echo -e "\n[5/7] 安装 OpenClaw..."

npm install -g openclaw
echo "  ✓ OpenClaw: 已安装"

# ============== 6. 生成 Token ==============
echo -e "\n[6/7] 生成认证 Token..."

TOKEN=$(openssl rand -hex 20)
echo "  ✓ Token: $TOKEN"
echo "  ⚠ 请保存此 Token，本地节点配置需要"

# 保存 Token 到文件
echo "$TOKEN" > ~/.openclaw/token.txt 2>/dev/null || true

# ============== 7. 配置网关 + systemd ==============
echo -e "\n[7/7] 配置网关 (Remote 模式)..."

mkdir -p ~/.openclaw

cat > ~/.openclaw/openclaw.json << EOF
{
  "gateway": {
    "port": 18789,
    "mode": "remote",
    "bind": "lan",
    "auth": {
      "mode": "token",
      "token": "$TOKEN"
    }
  },
  "security": {
    "dangerouslyAllowInsecurePrivateWs": true
  }
}
EOF

echo "  ✓ 配置文件：~/.openclaw/openclaw.json"

echo -e "\n  创建 systemd 服务..."
cat > /etc/systemd/system/openclaw-gateway.service << 'EOF'
[Unit]
Description=OpenClaw Gateway (Remote Mode)
After=network.target tailscaled.service
Wants=tailscaled.service

[Service]
Type=simple
User=root
WorkingDirectory=/root/.openclaw
ExecStart=/usr/bin/node /usr/lib/node_modules/openclaw/dist/index.js gateway --port 18789 --bind lan --allow-unconfigured
Restart=on-failure
RestartSec=10
StartLimitBurst=3
StartLimitIntervalSec=300

Environment=NODE_ENV=production
Environment=OPENCLAW_ALLOW_INSECURE_PRIVATE_WS=1

LimitNOFILE=65535
Nice=-5

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable openclaw-gateway
systemctl start openclaw-gateway

sleep 5

# ============== 验证 ==============
echo -e "\n╔════════════════════════════════════════════════════════════════╗"
if systemctl is-active --quiet openclaw-gateway; then
    echo "║                     ✓ 部署成功                                 ║"
    echo "╚════════════════════════════════════════════════════════════════╝"

    echo -e "\n【服务信息】"
    echo "  服务状态：$(systemctl is-active openclaw-gateway)"
    echo "  运行模式：remote"
    echo "  认证方式：token"

    echo -e "\n【网络信息】"
    echo "  Tailscale IP: $TAILSCALE_IP"
    echo "  网关地址：ws://${TAILSCALE_IP}:18789"
    echo "  Token: $TOKEN"

    echo -e "\n【端口监听】"
    ss -tlnp | grep 18789 || true

    echo -e "\n【本地节点配置示例 (PowerShell)】"
    cat << POWERSHELL
`$config = @{
  gateway = @{
    mode = "remote"
    auth = @{ token = "$TOKEN" }
    remote = @{ url = "ws://${TAILSCALE_IP}:18789" }
  }
} | ConvertTo-Json | Out-File ~/.openclaw/openclaw.json -Encoding utf8
POWERSHELL

    echo -e "\n【下一步操作】"
    echo "  1. 在本地运行 plan2-local-node.ps1"
    echo "  2. 检查连接：openclaw status"
    echo "  3. 查看日志：journalctl -u openclaw-gateway -f"
else
    echo "║                     ✗ 部署失败                                 ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
    journalctl -u openclaw-gateway --no-pager -n 20
    exit 1
fi
