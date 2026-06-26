# 🔧 OpenClaw 安装服务 - 完整文档

## 概述

这是一个自动化的OpenClaw安装服务技能，包含完整的安装脚本和配置模板。

## 文件清单

```
openclaw-setup-service/
├── SKILL.md                    # 本文档
├── README.md                   # 使用说明
├── _meta.json                  # 元数据
├── scripts/
│   ├── install.sh              # 主安装脚本
│   ├── config.sh               # 配置文件
│   ├── check.sh                # 环境检测
│   └── setup-telegram.sh       # Telegram配置
└── templates/
    └── openclaw.yaml           # 配置模板
```

## 安装脚本内容

### install.sh
```bash
#!/bin/bash
# OpenClaw 自动安装脚本 v1.0
# 支持: Ubuntu 20.04+ / Debian 11+

set -e

echo "🔧 开始安装 OpenClaw..."

# 检测系统
check_system() {
    if [[ -f /etc/debian_version ]]; then
        echo "✓ 检测到 Debian/Ubuntu 系统"
    else
        echo "✗ 仅支持 Debian/Ubuntu 系统"
        exit 1
    fi
}

# 安装依赖
install_deps() {
    apt update
    apt install -y curl git unzip
}

# 安装 Node.js
install_nodejs() {
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
    apt install -y nodejs
    node --version
    npm --version
}

# 安装 pnpm
install_pnpm() {
    npm install -g pnpm
    pnpm --version
}

# 安装 OpenClaw
install_openclaw() {
    pnpm add -g openclaw
}

# 主流程
check_system
install_deps
install_nodejs
install_pnpm
install_openclaw

echo "✅ 安装完成！"
echo "运行: openclaw init"
```

### config.sh
```bash
#!/bin/bash
# OpenClaw 配置脚本

OPENCLAW_DIR="${HOME}/.openclaw"
CONFIG_FILE="${OPENCLAW_DIR}/config.yaml"

# 创建目录
mkdir -p "${OPENCLAW_DIR}"

# 生成配置
cat > "${CONFIG_FILE}" << 'EOF'
version: "1.0"
channels:
  telegram:
    enabled: true
    botToken: "YOUR_BOT_TOKEN"
    adminIds: []
  telegram:
    enabled: false
skills:
  autoUpdate: true
  installPath: "${OPENCLAW_DIR}/skills"
EOF

echo "✓ 配置文件已创建: ${CONFIG_FILE}"
```

### check.sh
```bash
#!/bin/bash
# 环境检测脚本

echo "🔍 检测系统环境..."
echo ""

# 系统信息
echo "系统: $(uname -s) $(uname -r)"
echo "架构: $(uname -m)"
echo ""

# Node.js
if command -v node &> /dev/null; then
    echo "✓ Node.js: $(node --version)"
else
    echo "✗ Node.js: 未安装"
fi

# npm
if command -v npm &> /dev/null; then
    echo "✓ npm: $(npm --version)"
else
    echo "✗ npm: 未安装"
fi

# pnpm
if command -v pnpm &> /dev/null; then
    echo "✓ pnpm: $(pnpm --version)"
else
    echo "✗ pnpm: 未安装"
fi

# OpenClaw
if command -v openclaw &> /dev/null; then
    echo "✓ OpenClaw: $(openclaw --version)"
else
    echo "✗ OpenClaw: 未安装"
fi

# 内存
echo ""
echo "内存: $(free -h | awk '/^Mem:/ {print $2}')"
echo "磁盘: $(df -h / | awk 'NR==2 {print $4}')"
```

### setup-telegram.sh
```bash
#!/bin/bash
# Telegram Bot 配置脚本

read -p "请输入 Bot Token: " TOKEN

cat >> "${HOME}/.openclaw/config.yaml" << EOF
channels:
  telegram:
    enabled: true
    botToken: "${TOKEN}"
    adminIds:
      - YOUR_CHAT_ID
EOF

echo "✓ Telegram 配置完成"
echo "运行: openclaw gateway start"
```

## 配置模板

### openclaw.yaml
```yaml
version: "1.0"

# 频道配置
channels:
  telegram:
    enabled: true
    botToken: "${TELEGRAM_BOT_TOKEN}"
    adminIds: []
    groupAllowFrom: []
    groupPolicy: "allowlist"
  
  # 可以添加更多频道
  # telegram:
  # webhook: {}

# 技能设置
skills:
  autoUpdate: true
  installPath: "${HOME}/.openclaw/skills"
  
# 日志
logging:
  level: info
  file: "${HOME}/.openclaw/logs/jarvis.log"

# 高级
server:
  port: 18789
  host: "0.0.0.0"
```

## 使用步骤

### 1. 下载脚本
```bash
git clone https://github.com/lover876/openclaw-setup-service.git
cd openclaw-setup-service/scripts
chmod +x *.sh
```

### 2. 运行安装
```bash
sudo ./install.sh
```

### 3. 配置
```bash
./config.sh
./setup-telegram.sh
```

### 4. 启动
```bash
openclaw gateway start
```

## 服务价格

| 服务 | 价格 | 内容 |
|------|------|------|
| 基础安装 | ¥199 | 脚本+指导 |
| 标准配置 | ¥399 | 安装+配置Telegram |
| 高级定制 | ¥999 | 安装+配置+技能+培训 |

## 常见问题

Q: 支持哪些系统？
A: Ubuntu 20.04+, Debian 11+

Q: 需要root权限吗？
A: 安装时需要，系统配置不需要

Q: 安装需要多久？
A: 约15-30分钟

## 联系方式

微信: 扫码联系
