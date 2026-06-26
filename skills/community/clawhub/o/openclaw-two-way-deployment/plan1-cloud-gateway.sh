#!/bin/bash
# plan1-cloud-gateway.sh - 方案一：云端网关完整部署
# 用法：curl -O https://.../plan1-cloud-gateway.sh && bash plan1-cloud-gateway.sh

set -e

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║     方案一：云端网关 + Tailscale + SSH 隧道                       ║"
echo "║                    云端网关完整部署                              ║"
echo "╚════════════════════════════════════════════════════════════════╝"

# ============== 1. 系统环境检测 ==============
echo -e "\n[1/8] 系统环境检测..."

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

# 检测 SSH 服务
if systemctl is-active --quiet sshd || systemctl is-active --quiet ssh; then
    echo "  ✓ SSH 服务：运行中"
else
    echo "  ⚠ SSH 服务未运行，正在启动..."
    systemctl enable --now sshd 2>/dev/null || systemctl enable --now ssh 2>/dev/null || true
fi

# ============== 2. Tailscale 配置 ==============
echo -e "\n[2/8] 配置 Tailscale..."

if ! command -v tailscale &> /dev/null; then
    echo "  安装 Tailscale..."
    if [ "$OS" = "ubuntu" ] || [ "$OS" = "debian" ]; then
        curl -fsSL https://tailscale.com/install.sh | sh
    elif [ "$OS" = "centos" ] || [ "$OS" = "rhel" ] || [ "$OS" = "rocky" ]; then
        yum install -y yum-utils
        yum-config-manager --add-repo https://pkgs.tailscale.com/stable/centos/9/tailscale.repo
        yum install -y tailscale
    else
        echo "  ✗ 不支持的系统，请手动安装：https://tailscale.com/download"
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
    echo "  请运行以下命令完成认证："
    echo "    tailscale up"
    AUTH_URL=$(tailscale up 2>&1 | grep -o 'https://login.tailscale.com/a/[a-zA-Z0-9]*' || echo "")
    if [ -n "$AUTH_URL" ]; then
        echo "  认证链接：$AUTH_URL"
    fi
    read -p "  完成认证后按回车继续..."
    TAILSCALE_IP=$(tailscale ip | head -1)
    echo "  ✓ Tailscale: 已连接 ($TAILSCALE_IP)"
fi

# ============== 3. 防火墙配置 ==============
echo -e "\n[3/8] 配置防火墙..."

FIREWALL_CONFIGURED=false

# UFW (Ubuntu/Debian)
if command -v ufw &> /dev/null; then
    echo "  检测到 UFW 防火墙..."
    if ufw status | grep -q "Status: active"; then
        echo "  UFW 已启用，配置规则..."
        ufw allow 18789/tcp comment "OpenClaw Gateway" 2>/dev/null || ufw allow 18789/tcp
        ufw allow 22/tcp comment "SSH" 2>/dev/null || ufw allow 22/tcp
        ufw reload 2>/dev/null || true
        echo "  ✓ UFW: 18789/tcp, 22/tcp 已放行"
        FIREWALL_CONFIGURED=true
    else
        echo "  UFW 未启用"
    fi
fi

# Firewalld (CentOS/RHEL)
if [ "$FIREWALL_CONFIGURED" = false ] && command -v firewall-cmd &> /dev/null; then
    echo "  检测到 Firewalld..."
    if systemctl is-active --quiet firewalld; then
        echo "  Firewalld 运行中，配置规则..."
        firewall-cmd --permanent --add-port=18789/tcp 2>/dev/null || true
        firewall-cmd --permanent --add-service=ssh 2>/dev/null || true
        firewall-cmd --reload 2>/dev/null || true
        echo "  ✓ Firewalld: 18789/tcp, ssh 已放行"
        FIREWALL_CONFIGURED=true
    else
        echo "  Firewalld 未运行"
    fi
fi

# iptables (通用)
if [ "$FIREWALL_CONFIGURED" = false ] && command -v iptables &> /dev/null; then
    echo "  检测到 iptables..."
    if ! iptables -L INPUT -n 2>/dev/null | grep -q "dpt:18789"; then
        iptables -I INPUT -p tcp --dport 18789 -j ACCEPT 2>/dev/null || true
        iptables -I INPUT -p tcp --dport 22 -j ACCEPT 2>/dev/null || true
        echo "  ✓ iptables: 18789/tcp, 22/tcp 已添加"
        FIREWALL_CONFIGURED=true
    else
        echo "  端口规则已存在"
    fi
fi

if [ "$FIREWALL_CONFIGURED" = false ]; then
    echo "  ℹ 未检测到防火墙工具"
fi

echo "  ⚠ 重要：如使用云服务器 (阿里云/腾讯云/AWS 等)，请确保云控制台安全组已放行："
echo "     - 18789/tcp (Tailscale IP: $TAILSCALE_IP)"
echo "     - 22/tcp (SSH)"

# ============== 4. Node.js 配置 ==============
echo -e "\n[4/8] 配置 Node.js 环境..."

if command -v node &> /dev/null; then
    NODE_VER=$(node -v)
    echo "  ✓ Node.js 已安装：$NODE_VER"
else
    echo "  安装 Node.js 22..."
    if [ "$OS" = "ubuntu" ] || [ "$OS" = "debian" ]; then
        curl -fsSL https://deb.nodesource.com/setup_22.x | bash -
        apt-get install -y nodejs
    elif [ "$OS" = "centos" ] || [ "$OS" = "rhel" ] || [ "$OS" = "rocky" ]; then
        curl -fsSL https://rpm.nodesource.com/setup_22.x | bash -
        yum install -y nodejs
    else
        echo "  ✗ 不支持的系统，请手动安装 Node.js"
        exit 1
    fi
    echo "  ✓ Node.js 安装完成：$(node -v)"
fi

npm config set registry https://registry.npmmirror.com 2>/dev/null || true

# ============== 5. OpenClaw 安装 ==============
echo -e "\n[5/8] 安装 OpenClaw..."

if command -v openclaw &> /dev/null; then
    echo "  ✓ OpenClaw 已安装"
    openclaw --version
else
    echo "  安装 OpenClaw..."
    npm install -g openclaw
    echo "  ✓ OpenClaw 安装完成"
fi

# ============== 6. 网关配置 ==============
echo -e "\n[6/8] 配置 OpenClaw 网关..."

mkdir -p ~/.openclaw

cat > ~/.openclaw/openclaw.json << 'EOF'
{
  "gateway": {
    "port": 18789,
    "mode": "local",
    "bind": "lan"
  }
}
EOF

echo "  ✓ 配置文件：~/.openclaw/openclaw.json"

# ============== 7. systemd 服务配置 ==============
echo -e "\n[7/8] 创建 systemd 服务..."

cat > /etc/systemd/system/openclaw-gateway.service << 'EOF'
[Unit]
Description=OpenClaw Gateway Service
After=network.target tailscaled.service
Wants=tailscaled.service

[Service]
Type=simple
User=root
WorkingDirectory=/root/.openclaw
ExecStart=/usr/bin/node /usr/lib/node_modules/openclaw/dist/index.js gateway --port 18789 --bind lan
Restart=always
RestartSec=5
StartLimitBurst=3
StartLimitIntervalSec=300

Environment=NODE_ENV=production

# 资源限制
LimitNOFILE=65535
Nice=-5
OOMScoreAdjust=-500

[Install]
WantedBy=multi-user.target
EOF

echo "  ✓ systemd 服务配置完成"

# ============== 8. 启动服务 ==============
echo -e "\n[8/8] 启动服务..."

systemctl daemon-reload
systemctl enable openclaw-gateway
systemctl start openclaw-gateway

echo "  等待服务启动..."
sleep 5

# ============== 验证 ==============
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
    echo "  控制面板：http://${TAILSCALE_IP}:18789/"

    echo -e "\n【端口监听】"
    ss -tlnp | grep 18789 || netstat -tlnp | grep 18789 || true

    echo -e "\n【下一步操作】"
    echo "  1. 在本地电脑运行 SSH 隧道脚本 (start-tunnel.ps1)"
    echo "  2. 或在本地配置远程网关：openclaw gateway remote set ws://${TAILSCALE_IP}:18789"
    echo "  3. 查看日志：journalctl -u openclaw-gateway -f"

    echo -e "\n【本地 SSH 隧道脚本】"
    echo "  在本地 PowerShell 运行："
    echo "  ssh -N -f -L 2222:${TAILSCALE_IP}:18789 root@${TAILSCALE_IP}"
else
    echo "║                     ✗ 部署失败                                 ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
    echo -e "\n【错误日志】"
    journalctl -u openclaw-gateway --no-pager -n 20
    exit 1
fi
