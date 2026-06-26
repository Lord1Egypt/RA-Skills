#!/bin/bash
# ═══════════════════════════════════════════════════════════════════
# OpenClaw Connect Node - 一键卸载脚本
# ═══════════════════════════════════════════════════════════════════

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

# Default values
SERVICE_NAME="openclaw-node"
INSTALL_DIR="/opt/openclaw-node"

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --install-dir)  INSTALL_DIR="$2";  shift 2 ;;
    --service-name) SERVICE_NAME="$2"; shift 2 ;;
    --purge)        PURGE=1;           shift ;;
    --help|-h)
      echo "Usage: $0 [OPTIONS]"
      echo ""
      echo "Options:"
      echo "  --install-dir DIR    安装目录 (默认: /opt/openclaw-node)"
      echo "  --service-name NAME  服务名 (默认: openclaw-node)"
      echo "  --purge              同时删除安装目录和数据"
      echo "  --help               显示帮助"
      exit 0
      ;;
    *) shift ;;
  esac
done

echo ""
echo -e "${YELLOW}╔═══════════════════════════════════════════════╗${NC}"
echo -e "${YELLOW}║   OpenClaw Connect Node - 卸载               ║${NC}"
echo -e "${YELLOW}╚═══════════════════════════════════════════════╝${NC}"
echo ""

# Check root
if [[ $EUID -ne 0 ]]; then
  echo -e "${RED}[ERROR] 请使用 root 用户运行${NC}"
  exit 1
fi

# Stop and disable service
echo -e "${CYAN}[1/4] 停止服务...${NC}"
if systemctl is-active --quiet "$SERVICE_NAME" 2>/dev/null; then
  systemctl stop "$SERVICE_NAME"
  echo -e "${GREEN}  ✓ 服务已停止${NC}"
else
  echo "  服务未运行，跳过"
fi

echo -e "${CYAN}[2/4] 禁用服务...${NC}"
if systemctl is-enabled --quiet "$SERVICE_NAME" 2>/dev/null; then
  systemctl disable "$SERVICE_NAME"
  echo -e "${GREEN}  ✓ 服务已禁用${NC}"
else
  echo "  服务未启用，跳过"
fi

echo -e "${CYAN}[3/4] 删除 systemd 配置...${NC}"
if [[ -f "/etc/systemd/system/${SERVICE_NAME}.service" ]]; then
  rm -f "/etc/systemd/system/${SERVICE_NAME}.service"
  systemctl daemon-reload
  echo -e "${GREEN}  ✓ systemd 配置已删除${NC}"
else
  echo "  配置文件不存在，跳过"
fi

echo -e "${CYAN}[4/4] 删除管理命令...${NC}"
if [[ -f "/usr/local/bin/${SERVICE_NAME}" ]]; then
  rm -f "/usr/local/bin/${SERVICE_NAME}"
  echo -e "${GREEN}  ✓ 管理命令已删除${NC}"
else
  echo "  管理命令不存在，跳过"
fi

echo ""

# Purge data if requested
if [[ "$PURGE" == "1" ]]; then
  echo -e "${YELLOW}正在删除安装目录: ${INSTALL_DIR}${NC}"
  if [[ -d "$INSTALL_DIR" ]]; then
    rm -rf "$INSTALL_DIR"
    echo -e "${GREEN}  ✓ 安装目录已删除${NC}"
  else
    echo "  目录不存在，跳过"
  fi
else
  echo -e "${YELLOW}注意: 安装目录 ${INSTALL_DIR} 未删除${NC}"
  echo "  如需删除，请手动执行: rm -rf ${INSTALL_DIR}"
  echo "  或重新运行: $0 --purge"
fi

echo ""
echo -e "${GREEN}═══════════════════════════════════════════════════${NC}"
echo -e "${GREEN}  ✅ OpenClaw Connect Node 已卸载${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════${NC}"
echo ""
