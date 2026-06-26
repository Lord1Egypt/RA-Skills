#!/bin/bash
# ══════════════════════════════════════════════════
# 法眼（LawEye）一键部署脚本
# 目标: Ubuntu 20.04+ / Debian 11+
# 用法: chmod +x deploy.sh && sudo ./deploy.sh
# ══════════════════════════════════════════════════

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'
STEP=0

pass() { echo -e "${GREEN}[✓]${NC} $1"; }
warn() { echo -e "${YELLOW}[!]${NC} $1"; }
fail() { echo -e "${RED}[✗]${NC} $1"; exit 1; }
step() { STEP=$((STEP+1)); echo -e "\n${GREEN}[${STEP}/8]${NC} $1"; }

# ───────────── 参数确认 ─────────────
if [ -z "$1" ]; then
    echo "用法: ./deploy.sh <域名>"
    echo "示例: ./deploy.sh ai-gaoqian.xyz"
    exit 1
fi
DOMAIN=$1
PROJECT_DIR="/opt/laweye"

echo "═══════════════════════════════════"
echo "  法眼 LawEye v2.1 部署"
echo "  域名: ${DOMAIN}"
echo "═══════════════════════════════════"

# ── 1: 系统更新 ──
step "系统更新 + 基础依赖"
apt-get update -qq && apt-get upgrade -y -qq
apt-get install -y -qq python3 python3-pip nginx certbot python3-certbot-nginx
pass "系统依赖就绪"

# ── 2: Python 依赖 ──
step "安装 Python 依赖"
pip3 install pycryptodome -q
pass "pycryptodome 已安装"

# ── 3: 部署代码 ──
step "部署服务代码"
mkdir -p ${PROJECT_DIR}
cp laweye_server.py ${PROJECT_DIR}/
cp contract_reviewer.py ${PROJECT_DIR}/
cp alipay_private_key.pem ${PROJECT_DIR}/
cp alipay_public_key.pem ${PROJECT_DIR}/
chmod 600 ${PROJECT_DIR}/alipay_private_key.pem
pass "代码已部署到 ${PROJECT_DIR}"

# ── 4: systemd 服务 ──
step "注册 systemd 服务"
cp laweye.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable laweye
systemctl start laweye
sleep 2
if systemctl is-active --quiet laweye; then
    pass "laweye 服务已启动"
else
    fail "laweye 启动失败，检查: journalctl -u laweye -n 20"
fi

# ── 5: 健康检查 ──
step "本地健康检查"
sleep 1
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8888/ || echo "000")
if [ "$HTTP_CODE" = "402" ]; then
    pass "服务正常 (HTTP 402 Payment Required)"
else
    warn "服务返回 ${HTTP_CODE}，预期 402，请检查"
fi

# ── 6: Nginx 反代 ──
step "配置 Nginx 反代"
sed "s/YOUR_DOMAIN/${DOMAIN}/g" nginx.conf > /etc/nginx/sites-available/laweye
ln -sf /etc/nginx/sites-available/laweye /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
nginx -t && systemctl reload nginx
pass "Nginx 配置已生效"

# ── 7: SSL 证书 ──
step "申请 SSL 证书"
certbot --nginx -d ${DOMAIN} --non-interactive --agree-tos --email admin@${DOMAIN} --redirect 2>&1 | tail -3
pass "SSL 证书已配置"

# ── 8: 最终验证 ──
step "最终验证"
sleep 2
HTTPS_CODE=$(curl -s -o /dev/null -w "%{http_code}" https://${DOMAIN}/ || echo "000")
if [ "$HTTPS_CODE" = "402" ]; then
    pass "公网验证通过！https://${DOMAIN}/ → 402"
else
    warn "公网返回 ${HTTPS_CODE}，请手动检查 https://${DOMAIN}/"
fi

echo ""
echo "═══════════════════════════════════"
echo "  部署完成"
echo "  服务地址: https://${DOMAIN}"
echo "  本地端口: 127.0.0.1:8888"
echo "  管理命令: systemctl {start|stop|restart} laweye"
echo "  查看日志: journalctl -u laweye -f"
echo "═══════════════════════════════════"