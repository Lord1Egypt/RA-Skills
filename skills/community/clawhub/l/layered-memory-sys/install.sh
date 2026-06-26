#!/bin/bash
# install.sh - layered-memory-sys 一键安装脚本
# 用法: bash install.sh [--docker|--native]

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}========================================${NC}"
echo -e "${CYAN}  layered-memory-sys 一键安装${NC}"
echo -e "${CYAN}========================================${NC}"

# 检查 Docker
check_docker() {
  if command -v docker &> /dev/null; then
    return 0
  fi
  return 1
}

# Docker 模式安装
install_docker() {
  echo -e "\n${GREEN}🐳 Docker 模式安装...${NC}"
  
  if ! check_docker; then
    echo -e "${RED}❌ 未检测到 Docker，请先安装 Docker${NC}"
    echo "  curl -fsSL https://get.docker.com | sh"
    exit 1
  fi
  
  # 创建 memory 目录
  mkdir -p memory/backups
  
  # 创建默认配置
  if [ ! -f memory/config.json ]; then
    cat > memory/config.json << 'EOF'
{
  "api": { "port": 3456 },
  "memoryDir": "/app/memory",
  "dream": {
    "schedule": "0 3 * * *",
    "autoArchive": true,
    "autoConsolidate": true,
    "autoForget": true,
    "autoMerge": true
  }
}
EOF
    echo "  ✅ 已创建默认配置"
  fi
  
  echo -e "\n🚀 启动服务..."
  docker compose up -d
  
  echo -e "\n${GREEN}✅ 安装完成!${NC}"
  echo -e "   📊 面板:     http://localhost/memory"
  echo -e "   🔌 API:     http://localhost:3456"
  echo -e "   📦 备份:     ./backups/"
  echo -e "\n${CYAN}查看日志:  docker compose logs -f${NC}"
}

# 原生模式安装
install_native() {
  echo -e "\n${GREEN}📦 原生模式安装...${NC}"
  
  # 检查 Node.js
  if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ 请先安装 Node.js (v18+)${NC}"
    exit 1
  fi
  
  echo "  ✅ Node.js $(node -v)"
  
  # 安装依赖
  echo "  安装依赖..."
  npm install --production
  
  # 创建 memory 目录
  mkdir -p memory/backups
  
  # 创建默认配置
  if [ ! -f memory/config.json ]; then
    cat > memory/config.json << 'EOF'
{
  "api": { "port": 3456 },
  "memoryDir": "./memory",
  "dream": {
    "schedule": "0 3 * * *",
    "autoArchive": true,
    "autoConsolidate": true,
    "autoForget": true,
    "autoMerge": true
  }
}
EOF
    echo "  ✅ 已创建默认配置"
  fi
  
  # 安装 systemd 服务
  if command -v systemctl &> /dev/null; then
    SCRIPTS_DIR="$(cd "$(dirname "$0")" && pwd)"
    cat > /tmp/layered-memory.service << EOF
[Unit]
Description=layered-memory-sys API Service
After=network.target

[Service]
Type=simple
WorkingDirectory=${SCRIPTS_DIR}
ExecStart=$(which node) ${SCRIPTS_DIR}/scripts/start-api.mjs
Restart=always
RestartSec=5
Environment=NODE_ENV=production

[Install]
WantedBy=multi-user.target
EOF
    
    if [ "$EUID" -eq 0 ]; then
      cp /tmp/layered-memory.service /etc/systemd/system/
      systemctl daemon-reload
      systemctl enable layered-memory
      systemctl start layered-memory
      echo -e "  ✅ systemd 服务已安装并启动"
    else
      echo -e "  ⚠️ 非 root 用户，跳过 systemd 安装"
      echo "    手动: sudo cp /tmp/layered-memory.service /etc/systemd/system/"
    fi
  fi
  
  # 启动服务
  echo -e "\n🚀 启动服务..."
  nohup node scripts/start-api.mjs > /tmp/layered-memory.log 2>&1 &
  echo "  ✅ 服务已启动 (PID: $!)"
  
  echo -e "\n${GREEN}✅ 安装完成!${NC}"
  echo -e "   🔌 API:     http://localhost:3456"
  echo -e "   📦 备份:     ./memory/backups/"
  echo -e "   📊 面板:     需要配置 Nginx 反向代理"
  echo -e "\n${CYAN}启动:  node scripts/start-api.mjs${NC}"
  echo -e "${CYAN}备份:  node scripts/backup.mjs${NC}"
}

# 主流程
echo ""
echo "选择安装方式:"
echo "  1) Docker （推荐，含 Nginx + 面板）"
echo "  2) 原生（直接跑 Node.js）"
echo ""
read -p "请输入 [1/2] (默认 1): " choice

case "${choice:-1}" in
  1|docker|Docker)
    install_docker
    ;;
  2|native|Native)
    install_native
    ;;
  *)
    echo -e "${RED}无效选择${NC}"
    exit 1
    ;;
esac
