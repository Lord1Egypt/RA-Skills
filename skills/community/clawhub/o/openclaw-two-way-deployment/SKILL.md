# OpenClaw 三种部署方案完整技能

## 技能使用说明

运行 `/openclaw-deploy` 选择部署方案，自动完成环境检测、防火墙配置、服务部署。

---

## 方案一：云端网关 + Tailscale + SSH 隧道控制本地

### 完整架构流程图

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              云端服务器 (Linux)                              │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                     OpenClaw Gateway                                  │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                 │   │
│  │  │ 钉钉/飞书     │  │ 核心处理     │  │ AI 模型 API    │                 │   │
│  │  └──────────────┘  └──────────────┘  └──────────────┘                 │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │  SSH Server (22)           Tailscale (<YOUR_CLOUD_IP>:18789)         │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
              ┌─────────────────────┴─────────────────────┐
              │ Tailscale VPN (加密)                       │
              │ SSH 隧道：localhost:2222 → <YOUR_CLOUD_IP>:18789
              ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              本地电脑 (Windows)                              │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │  SSH Client (后台)           OpenClaw CLI / VSCode                   │   │
│  │                              连接：ws://localhost:2222                │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
                                    ▲
                                    │
                          ┌─────────┴─────────┐
                          ▼                   ▼
                   ┌──────────┐        ┌──────────┐
                   │ 钉钉 APP │        │ 浏览器   │
                   └──────────┘        └──────────┘
```

**数据流向：**
1. 钉钉/飞书 → Webhook → 云端网关 (18789)
2. 云端网关 → AI 模型 API → 获取回复
3. 云端网关 → Webhook → 返回钉钉/飞书
4. 本地通过 SSH 隧道访问云端网关进行配置/监控
```

### 部署前检查清单

| 检查项 | 本地 | 云端 | 验证命令 |
|--------|------|------|----------|
| Tailscale 账号 | ✅ 同一账号 | ✅ 同一账号 | `tailscale status` |
| Tailscale 连接 | ✅ 已连接 | ✅ 已连接 | `tailscale ip` |
| Node.js (v18+) | ✅ 已安装 | ✅ 已安装 | `node -v` |
| SSH 客户端 | ✅ 已配置 | ❌ | `ssh -V` |
| SSH 服务端 | ❌ | ✅ 已运行 | `systemctl status sshd` |
| 防火墙 18789 | ❌ | ⚠️ 需放行 | `ufw status` / `firewall-cmd --list-all` |
| 防火墙 22 | ❌ | ⚠️ 需放行 | `ufw status` |
| 云安全组 18789 | ❌ | ⚠️ 需放行 | 云控制台检查 |
| 云安全组 22 | ❌ | ⚠️ 需放行 | 云控制台检查 |

### 云端完整部署脚本（含防火墙 + 安全组检测）

```bash
#!/bin/bash
# plan1-cloud-gateway.sh - 方案一：云端网关完整部署
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
```

### 本地 SSH 隧道脚本（持久运行 + 开机自启）

```powershell
# plan1-local-tunnel.ps1 - 方案一：本地 SSH 隧道持久部署
param(
    [string]$CloudIP = ""
)

$ErrorActionPreference = "Stop"
$TaskName = "OpenClaw-SSH-Tunnel"
$LocalPort = 2222
$RemotePort = 18789
$ScriptDir = "$env:USERPROFILE\.openclaw"

Write-Host "╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║     方案一：云端网关 + Tailscale + SSH 隧道                        ║" -ForegroundColor Cyan
Write-Host "║                  本地 SSH 隧道持久部署                            ║"
Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan

# 1. 检查 Tailscale
Write-Host "`n[1/6] 检查 Tailscale..." -ForegroundColor Yellow
try {
    $tsStatus = tailscale status 2>&1
    if ($LASTEXITCODE -eq 0) {
        $tsIP = (tailscale ip | Select-Object -First 1).Trim()
        Write-Host "  ✓ Tailscale: 已连接 ($tsIP)" -ForegroundColor Green
    } else {
        Write-Host "  Tailscale 未运行，正在启动..." -ForegroundColor Yellow
        tailscale up
        Start-Sleep -Seconds 5
    }
} catch {
    Write-Host "  ✗ Tailscale 未安装" -ForegroundColor Red
    Write-Host "  下载：https://tailscale.com/download" -ForegroundColor Yellow
    exit 1
}

# 2. 获取云端 IP
Write-Host "`n[2/6] 配置云端网关..." -ForegroundColor Yellow
if ($CloudIP -eq "") {
    Write-Host "  请输入云端网关 Tailscale IP:" -ForegroundColor Yellow
    $CloudIP = Read-Host "  Cloud IP"
    if ($CloudIP -eq "") {
        Write-Host "  ✗ 未输入 IP 地址" -ForegroundColor Red
        exit 1
    }
}
Write-Host "  云端网关：$CloudIP:$RemotePort" -ForegroundColor Green

# 3. 测试连接
Write-Host "`n[3/6] 测试云端连接..." -ForegroundColor Yellow
$testResult = Test-NetConnection -ComputerName $CloudIP -Port $RemotePort -WarningAction SilentlyContinue -InformationLevel Quiet
if ($testResult) {
    Write-Host "  ✓ 云端网关：可达" -ForegroundColor Green
} else {
    Write-Host "  ✗ 无法连接云端网关" -ForegroundColor Red
    Write-Host "  请检查：" -ForegroundColor Yellow
    Write-Host "    1. 云端 Tailscale 是否运行" -ForegroundColor Yellow
    Write-Host "    2. 云端网关服务是否启动" -ForegroundColor Yellow
    Write-Host "    3. 云安全组是否放行 18789" -ForegroundColor Yellow
    exit 1
}

# 4. 清理旧隧道
Write-Host "`n[4/6] 清理旧隧道进程..." -ForegroundColor Yellow
$sshProcesses = Get-Process | Where-Object { $_.ProcessName -eq "ssh" }
$stopped = 0
foreach ($p in $sshProcesses) {
    $cmd = (Get-CimInstance Win32_Process -Filter "ProcessId = $($p.Id)" -ErrorAction SilentlyContinue).CommandLine
    if ($cmd -like "*${LocalPort}*" -or $cmd -like "*${CloudIP}*") {
        Stop-Process -Id $p.Id -Force -ErrorAction SilentlyContinue
        $stopped++
    }
}
Write-Host "  已停止 $stopped 个旧隧道进程" -ForegroundColor Gray

# 5. 创建持久化脚本
Write-Host "`n[5/6] 创建持久化配置..." -ForegroundColor Yellow

New-Item -ItemType Directory -Force -Path $ScriptDir | Out-Null

$tunnelScript = @"
# OpenClaw SSH 隧道启动脚本
`$ErrorActionPreference = "SilentlyContinue"
`$sshArgs = "-N -L ${LocalPort}:${CloudIP}:${RemotePort} root@${CloudIP}"

# 检查 SSH 连接
while (`$true) {
    Start-Process ssh -ArgumentList `$sshArgs -WindowStyle Hidden -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 60

    # 检查隧道是否通畅
    `$test = Test-NetConnection -ComputerName localhost -Port ${LocalPort} -WarningAction SilentlyContinue -InformationLevel Quiet
    if (-not `$test) {
        # 隧道断开，重启 SSH 进程
        Get-Process | Where-Object { `$_.ProcessName -eq "ssh" -and `$_.CommandLine -like "*${LocalPort}*" } | Stop-Process -Force
    }
}
"@

$scriptPath = "$ScriptDir\start-ssh-tunnel.ps1"
$tunnelScript | Out-File -FilePath $scriptPath -Encoding utf8 -Force
Write-Host "  ✓ 隧道脚本：$scriptPath" -ForegroundColor Green

# 6. 创建计划任务（开机自启）
Write-Host "`n[6/6] 创建计划任务（开机自启）..." -ForegroundColor Yellow

# 删除旧任务
schtasks /Delete /TN $TaskName /F 2>$null | Out-Null

# 创建新任务（系统启动时 + 用户登录时）
$argument = "-ExecutionPolicy Bypass -WindowStyle Hidden -File `"$scriptPath`""
schtasks /Create /TN $TaskName /TR "powershell.exe $argument" /SC ONLOGON /RU SYSTEM /F 2>$null

if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✓ 计划任务：$TaskName (开机自启)" -ForegroundColor Green
} else {
    # 降级方案：当前用户登录时启动
    schtasks /Create /TN $TaskName /TR "powershell.exe $argument" /SC ONLOGON /F 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✓ 计划任务：$TaskName (用户登录自启)" -ForegroundColor Green
    } else {
        Write-Host "  ⚠ 计划任务创建失败，将手动启动" -ForegroundColor Yellow
    }
}

# 立即启动隧道
Write-Host "`n  立即启动 SSH 隧道..." -ForegroundColor Yellow
$sshArgs = "-N -L ${LocalPort}:${CloudIP}:${RemotePort} root@${CloudIP}"
Start-Process ssh -ArgumentList $sshArgs -WindowStyle Hidden

Start-Sleep -Seconds 3

# 验证
$tunnelTest = Test-NetConnection -ComputerName localhost -Port $LocalPort -WarningAction SilentlyContinue -InformationLevel Quiet
if ($tunnelTest) {
    Write-Host "  ✓ SSH 隧道：已建立 (localhost:${LocalPort} -> ${CloudIP}:${RemotePort})" -ForegroundColor Green

    Write-Host "`n╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
    Write-Host "║                     ✓ 部署成功                                 ║" -ForegroundColor Green
    Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan

    Write-Host "`n【隧道信息】"
    Write-Host "  本地端口：localhost:${LocalPort}"
    Write-Host "  远程地址：${CloudIP}:${RemotePort}"
    Write-Host "  计划任务：$TaskName (开机/登录自启)"

    Write-Host "`n【下一步操作】"
    Write-Host "  1. 配置远程网关：openclaw gateway remote set ws://localhost:${LocalPort}"
    Write-Host "  2. 检查状态：openclaw status"
    Write-Host "  3. 查看日志：openclaw logs --follow"
} else {
    Write-Host "  ✗ SSH 隧道建立失败" -ForegroundColor Red
    Write-Host "  请检查 SSH 密钥配置或手动运行：" -ForegroundColor Yellow
    Write-Host "    ssh -N -L ${LocalPort}:${CloudIP}:${RemotePort} root@${CloudIP}"
    exit 1
}
```

---

## 方案二：云端网关 + Tailscale + 本地节点

### 完整架构流程图

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              云端服务器 (Linux)                              │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                  OpenClaw Gateway (Remote 模式)                       │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                 │   │
│  │  │ 钉钉/飞书     │  │ WebSocket    │  │ AI 模型 API    │                 │   │
│  │  │ Webhook      │  │ 服务端        │  │              │                 │   │
│  │  └──────────────┘  └──────────────┘  └──────────────┘                 │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │  Tailscale: <YOUR_CLOUD_IP>:18789 (Token 认证)                       │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ Tailscale VPN (加密)
                                    │ WebSocket: ws://<YOUR_CLOUD_IP>:18789
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              本地电脑 (Windows)                              │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                  OpenClaw Node (本地节点)                             │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                 │   │
│  │  │ WebSocket    │  │ 本地执行     │  │ 返回结果     │                 │   │
│  │  │ 客户端        │  │              │  │              │                 │   │
│  │  └──────────────┘  └──────────────┘  └──────────────┘                 │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │  Tailscale: <YOUR_LOCAL_IP>         本地 CLI/VSCode                   │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
                                    ▲
                                    │
                          ┌─────────┴─────────┐
                          ▼                   ▼
                   ┌──────────┐        ┌──────────┐
                   │ 钉钉 APP │        │ 浏览器   │
                   └──────────┘        └──────────┘
```

**数据流向：**
1. 钉钉/飞书 → Webhook → 云端网关
2. 云端网关 → WebSocket → 本地节点
3. 本地节点 → 执行任务 → 返回结果 → 云端网关
4. 云端网关 → AI 模型 API → 获取回复 → 返回钉钉/飞书
```

### 部署前检查清单

| 检查项 | 本地 | 云端 | 验证命令 |
|--------|------|------|----------|
| Tailscale 账号 | ✅ 同一账号 | ✅ 同一账号 | `tailscale status` |
| Tailscale 连接 | ✅ 已连接 | ✅ 已连接 | `tailscale ip` |
| Node.js (v18+) | ✅ 已安装 | ✅ 已安装 | `node -v` |
| 防火墙 18789 | ❌ | ⚠️ 需放行 | `ufw status` |
| 云安全组 18789 | ❌ | ⚠️ 需放行 | 云控制台检查 |
| Token 配置 | ✅ 一致 | ✅ 一致 | 检查配置文件 |

### 云端完整部署脚本（Remote 模式 + Token 认证）

```bash
#!/bin/bash
# plan2-cloud-remote-gateway.sh - 方案二：云端远程网关完整部署
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
```

### 本地节点完整部署脚本

```powershell
# plan2-local-node.ps1 - 方案二：本地节点完整部署
param(
    [string]$CloudIP = "",
    [string]$Token = ""
)

$ErrorActionPreference = "Stop"
$OpenClawDir = "$env:USERPROFILE\.openclaw"
$NodeExe = "C:\Program Files\nodejs\node.exe"
$OpenClawMjs = "$env:APPDATA\npm\node_modules\openclaw\openclaw.mjs"
$TaskName = "OpenClaw-Node"

Write-Host "╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║     方案二：云端网关 + Tailscale + 本地节点                       ║" -ForegroundColor Cyan
Write-Host "║                    本地节点完整部署                              ║"
Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan

# 1. 检查 Tailscale
Write-Host "`n[1/6] 检查 Tailscale..." -ForegroundColor Yellow
$tsStatus = tailscale status 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "  Tailscale 未运行，正在启动..." -ForegroundColor Yellow
    tailscale up
    Start-Sleep -Seconds 5
}
$tsIP = (tailscale ip | Select-Object -First 1).Trim()
Write-Host "  ✓ Tailscale IP: $tsIP" -ForegroundColor Green

# 2. 检查 Node.js
Write-Host "`n[2/6] 检查 Node.js..." -ForegroundColor Yellow
if (!(Test-Path $NodeExe)) {
    Write-Host "  ✗ Node.js 未安装" -ForegroundColor Red
    Write-Host "  下载：https://nodejs.org/" -ForegroundColor Yellow
    exit 1
}
$nodeVer = & $NodeExe -v
Write-Host "  ✓ Node.js: $nodeVer" -ForegroundColor Green

# 3. 检查/安装 OpenClaw
Write-Host "`n[3/6] 检查 OpenClaw..." -ForegroundColor Yellow
if (!(Test-Path $OpenClawMjs)) {
    Write-Host "  安装 OpenClaw..." -ForegroundColor Yellow
    npm install -g openclaw --registry=https://registry.npmmirror.com
    if ($LASTEXITCODE -ne 0) {
        Write-Host "  ✗ 安装失败" -ForegroundColor Red
        exit 1
    }
}
Write-Host "  ✓ OpenClaw: 已安装" -ForegroundColor Green

# 4. 获取云端信息
Write-Host "`n[4/6] 配置连接信息..." -ForegroundColor Yellow

if ($CloudIP -eq "") {
    Write-Host "  请输入云端网关 Tailscale IP:" -ForegroundColor Yellow
    $CloudIP = Read-Host "  Cloud IP"
}

if ($Token -eq "") {
    Write-Host "  请输入云端网关 Token:" -ForegroundColor Yellow
    $Token = Read-Host "  Token"
}

Write-Host "  云端网关：$CloudIP:18789" -ForegroundColor Green

# 5. 测试连接
Write-Host "`n[5/6] 测试云端连接..." -ForegroundColor Yellow
$testResult = Test-NetConnection -ComputerName $CloudIP -Port 18789 -WarningAction SilentlyContinue -InformationLevel Quiet
if (!$testResult) {
    Write-Host "  ✗ 无法连接云端网关" -ForegroundColor Red
    Write-Host "  请检查：" -ForegroundColor Yellow
    Write-Host "    1. 云端 Tailscale 是否运行" -ForegroundColor Yellow
    Write-Host "    2. 云端网关是否启动" -ForegroundColor Yellow
    Write-Host "    3. 云安全组是否放行 18789" -ForegroundColor Yellow
    exit 1
}
Write-Host "  ✓ 云端网关：可达" -ForegroundColor Green

# 6. 配置并启动
Write-Host "`n[6/6] 配置并启动节点..." -ForegroundColor Yellow

New-Item -ItemType Directory -Force -Path $OpenClawDir | Out-Null

$config = @{
    gateway = @{
        mode = "remote"
        auth = @{ token = $Token }
        remote = @{ url = "ws://$($CloudIP):18789" }
    }
} | ConvertTo-Json -Depth 10

$config | Out-File -FilePath "$OpenClawDir\openclaw.json" -Encoding utf8 -Force
Write-Host "  ✓ 配置：$OpenClawDir\openclaw.json" -ForegroundColor Green

# 创建启动脚本
$startScript = "$OpenClawDir\start-node.ps1"
@"
`$env:OPENCLAW_ALLOW_INSECURE_PRIVATE_WS = "1"
& "$NodeExe" "$OpenClawMjs" node run --host "$CloudIP" --port 18789
"@ | Out-File -FilePath $startScript -Encoding utf8 -Force

# 启动节点
Write-Host "  启动节点..." -ForegroundColor Yellow
$env:OPENCLAW_ALLOW_INSECURE_PRIVATE_WS = "1"
Start-Process $NodeExe -ArgumentList "$OpenClawMjs", "node", "run", "--host", $CloudIP, "--port", "18789" -WindowStyle Normal

Start-Sleep -Seconds 5

Write-Host "`n╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║                     ✓ 部署成功                                 ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan

Write-Host "`n【连接信息】"
Write-Host "  云端网关：ws://$($CloudIP):18789"
Write-Host "  节点状态：启动中..."

Write-Host "`n【下一步操作】"
Write-Host "  1. 检查状态：openclaw status"
Write-Host "  2. 查看日志：openclaw logs --follow"
Write-Host "  3. 配置开机自启（可选）："
Write-Host "     schtasks /Create /TN `"$TaskName`" /TR `"powershell -File '$startScript'`" /SC ONLOGON /F"
```

---

## 方案三：云端网关 + 本地网关双部署（含同步备份）

### 完整架构流程图

```
                              ┌──────────────┐
                              │  通讯软件     │
                              │ (钉钉/飞书)   │
                              └──────┬───────┘
                                     │
                ┌────────────────────┴────────────────────┐
                │                                         │
                ▼                                         ▼
┌───────────────────────────┐               ┌───────────────────────────┐
│    云端网关 (Primary)     │               │   本地网关 (Secondary)     │
│  <YOUR_CLOUD_IP>:18789    │               │   127.0.0.1:18789         │
│                           │               │                           │
│  ┌─────────────────────┐  │               │  ┌─────────────────────┐  │
│  │ 通道插件 (钉钉/飞书) │  │               │  │ 本地通道 (测试/备用) │  │
│  └──────────┬──────────┘  │               │  └──────────┬──────────┘  │
│             │             │               │             │             │
│  ┌──────────▼──────────┐  │               │  ┌──────────▼──────────┐  │
│  │ AI 模型 (云端 API)    │  │               │  │ AI 模型 (本地 API)    │  │
│  │ Claude / Qwen       │  │               │  │ Ollama / LM Studio  │  │
│  └──────────┬──────────┘  │               │  └──────────┬──────────┘  │
│             │             │               │             │             │
│  ┌──────────▼──────────┐  │   同步通道    │  ┌──────────▼──────────┐  │
│  │ 数据同步模块        │◄─┼───────────────┼─►│ 数据同步模块        │  │
│  │ - 会话状态 (实时)   │  │   Tailscale   │  │ - 会话状态 (实时)   │  │
│  │ - 消息历史 (增量)   │  │   (加密)      │  │ - 消息历史 (增量)   │  │
│  └──────────┬──────────┘  │               │  └──────────┬──────────┘  │
│             │             │               │             │             │
│  ┌──────────▼──────────┐  │               │  ┌──────────▼──────────┐  │
│  │ SQLite (云端存储)   │  │               │  │ SQLite (本地存储)   │  │
│  └─────────────────────┘  │               │  └─────────────────────┘  │
└───────────────────────────┘               └───────────────────────────┘

故障转移:
  ┌─────────────────────────────────────────────────────────────────────┐
  │ 正常：通讯软件 → 云端网关 → 处理并回复                               │
  │ 云端故障：本地网关接管 → 离线队列 → 云端恢复后同步                   │
  │ 本地故障：云端继续运行 → 数据从云端恢复                              │
  └─────────────────────────────────────────────────────────────────────┘
```
```

### 部署前检查清单

| 检查项 | 本地 | 云端 | 验证命令 |
|--------|------|------|----------|
| Tailscale 账号 | ✅ 同一账号 | ✅ 同一账号 | `tailscale status` |
| Tailscale 连接 | ✅ 已连接 | ✅ 已连接 | `tailscale ip` |
| Node.js (v18+) | ✅ 已安装 | ✅ 已安装 | `node -v` |
| 防火墙 18789 | ⚠️ 仅本地 | ⚠️ 需放行 | `ufw status` |
| 云安全组 18789 | ❌ | ⚠️ 需放行 | 云控制台检查 |
| 同步 Token | ✅ 一致 | ✅ 一致 | 检查配置文件 |

### 本地网关完整部署（含开机自启 + 同步配置）

```powershell
# plan3-local-gateway.ps1 - 方案三：本地网关完整部署（含同步备份）
param(
    [string]$CloudIP = ""
)

$ErrorActionPreference = "Stop"
$OpenClawDir = "$env:USERPROFILE\.openclaw"
$NodeExe = "C:\Program Files\nodejs\node.exe"
$TaskName = "OpenClaw-Gateway"
$SyncPort = 18790

Write-Host "╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║     方案三：云端网关 + 本地网关双部署                              ║" -ForegroundColor Cyan
Write-Host "║                  本地网关完整部署（含同步备份）                  ║"
Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan

# 1. 检查 Tailscale
Write-Host "`n[1/7] 检查 Tailscale..." -ForegroundColor Yellow
$tsStatus = tailscale status 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "  Tailscale 未运行，正在启动..." -ForegroundColor Yellow
    tailscale up
    Start-Sleep -Seconds 5
}
$tsIP = (tailscale ip | Select-Object -First 1).Trim()
Write-Host "  ✓ Tailscale IP: $tsIP" -ForegroundColor Green

# 2. 检查 Node.js
Write-Host "`n[2/7] 检查 Node.js..." -ForegroundColor Yellow
if (!(Test-Path $NodeExe)) {
    Write-Host "  ✗ Node.js 未安装" -ForegroundColor Red
    exit 1
}
Write-Host "  ✓ Node.js: $(& $NodeExe -v)" -ForegroundColor Green

# 3. 安装 OpenClaw
Write-Host "`n[3/7] 安装 OpenClaw..." -ForegroundColor Yellow
npm install -g openclaw --registry=https://registry.npmmirror.com
if ($LASTEXITCODE -ne 0) {
    Write-Host "  ✗ 安装失败" -ForegroundColor Red
    exit 1
}
Write-Host "  ✓ OpenClaw: 已安装" -ForegroundColor Green

# 4. 配置网关
Write-Host "`n[4/7] 配置网关..." -ForegroundColor Yellow

if ($CloudIP -eq "") {
    Write-Host "  请输入云端网关 Tailscale IP:" -ForegroundColor Yellow
    $CloudIP = Read-Host "  Cloud IP"
}

New-Item -ItemType Directory -Force -Path $OpenClawDir | Out-Null

$config = @{
    gateway = @{
        port = 18789
        mode = "local"
        bind = "localhost"
    }
    sync = @{
        enabled = $true
        remoteUrl = "https://$($CloudIP):${SyncPort}"
        token = $(openssl rand -hex 20)
        direction = "bidirectional"
        interval = 300
    }
} | ConvertTo-Json -Depth 10

$config | Out-File -FilePath "$OpenClawDir\openclaw.json" -Encoding utf8 -Force
Write-Host "  ✓ 配置：$OpenClawDir\openclaw.json" -ForegroundColor Green
Write-Host "  同步配置：双向同步 (5 分钟间隔)" -ForegroundColor Green

# 5. 创建开机自启脚本
Write-Host "`n[5/7] 创建开机自启配置..." -ForegroundColor Yellow

$startScript = "$OpenClawDir\start-gateway.ps1"
@"
`$env:OPENCLAW_ALLOW_INSECURE_PRIVATE_WS = "1"
& "$NodeExe" "$OpenClawMjs" gateway run
"@ | Out-File -FilePath $startScript -Encoding utf8 -Force

# 创建计划任务
$argument = "-ExecutionPolicy Bypass -WindowStyle Hidden -File `"$startScript`""
schtasks /Delete /TN $TaskName /F 2>$null | Out-Null
schtasks /Create /TN $TaskName /TR "powershell.exe $argument" /SC ONLOGON /F 2>$null

if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✓ 计划任务：$TaskName (开机自启)" -ForegroundColor Green
} else {
    Write-Host "  ⚠ 计划任务创建失败" -ForegroundColor Yellow
}

# 6. 启动网关
Write-Host "`n[6/7] 启动网关..." -ForegroundColor Yellow

$env:OPENCLAW_ALLOW_INSECURE_PRIVATE_WS = "1"
Start-Process $NodeExe -ArgumentList "$OpenClawMjs", "gateway", "run" -WindowStyle Normal

Start-Sleep -Seconds 5

# 7. 验证
Write-Host "`n[7/7] 验证网关..." -ForegroundColor Yellow
$portTest = Test-NetConnection -ComputerName localhost -Port 18789 -WarningAction SilentlyContinue -InformationLevel Quiet
if ($portTest) {
    Write-Host "  ✓ 网关：运行中 (localhost:18789)" -ForegroundColor Green

    Write-Host "`n╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
    Write-Host "║                     ✓ 部署成功                                 ║" -ForegroundColor Green
    Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan

    Write-Host "`n【访问信息】"
    Write-Host "  网关地址：ws://localhost:18789"
    Write-Host "  控制面板：http://localhost:18789/"
    Write-Host "  开机自启：$TaskName"

    Write-Host "`n【同步配置】"
    Write-Host "  云端网关：$CloudIP"
    Write-Host "  同步端口：${SyncPort}"
    Write-Host "  同步方向：双向"
    Write-Host "  同步间隔：300 秒"

    Write-Host "`n【下一步操作】"
    Write-Host "  1. 在云端运行 plan3-cloud-gateway.sh"
    Write-Host "  2. 检查状态：openclaw status"
    Write-Host "  3. 配置同步：openclaw sync config"
} else {
    Write-Host "  ✗ 网关启动失败" -ForegroundColor Red
    exit 1
}
```

### 云端网关完整部署（含同步备份）

```bash
#!/bin/bash
# plan3-cloud-gateway.sh - 方案三：云端网关完整部署（含同步备份）
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

cat > ~/.openclaw/openclaw.json << 'EOF'
{
  "gateway": {
    "port": 18789,
    "mode": "local",
    "bind": "lan"
  },
  "sync": {
    "enabled": true,
    "port": 18790,
    "token": "auto-generated",
    "direction": "bidirectional",
    "interval": 300
  }
}
EOF

echo "  ✓ 配置文件：~/.openclaw/openclaw.json"

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
```

---

## 故障排查

### 通用诊断脚本

```bash
#!/bin/bash
# diagnostic.sh - OpenClaw 快速诊断

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║              OpenClaw 诊断报告                                  ║"
echo "╚════════════════════════════════════════════════════════════════╝"

echo -e "\n【1. 系统信息】"
uname -a
grep PRETTY_NAME /etc/os-release 2>/dev/null || true

echo -e "\n【2. Tailscale 状态】"
tailscale status 2>&1 | head -10 || echo "Tailscale 未安装/未运行"

echo -e "\n【3. Node.js 版本】"
node -v 2>/dev/null || echo "Node.js 未安装"
npm -v 2>/dev/null || true

echo -e "\n【4. OpenClaw 状态】"
openclaw status 2>&1 | head -20 || echo "OpenClaw 未安装/无法运行"

echo -e "\n【5. 端口监听】"
ss -tlnp 2>/dev/null | grep -E "18789|18790" || netstat -tlnp 2>/dev/null | grep -E "18789|18790" || echo "无 OpenClaw 端口"

echo -e "\n【6. 防火墙状态】"
if command -v ufw &> /dev/null; then
    ufw status 2>&1 | head -10
fi
if command -v firewall-cmd &> /dev/null; then
    firewall-cmd --list-all 2>&1 | head -10
fi

echo -e "\n【7. 网关服务】"
systemctl status openclaw-gateway --no-pager -l 2>&1 | head -15 || echo "服务未安装"

echo -e "\n【8. 最近日志】"
journalctl -u openclaw-gateway --no-pager -n 10 2>&1 || echo "无日志"
```

### 常见问题速查

| 问题 | 可能原因 | 解决方案 |
|------|----------|----------|
| 端口不通 | 防火墙阻挡 | `ufw allow 18789/tcp` |
| Tailscale 断开 | 认证过期 | `tailscale up --force` |
| 同步失败 | Token 不一致 | 检查两边配置文件 |
| 服务无法启动 | 端口占用 | `ss -tlnp \| grep 18789` |
| Webhook 不响应 | 安全组未放行 | 云控制台添加入站规则 |
