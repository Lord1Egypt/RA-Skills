#!/bin/bash
# diagnostic.sh - OpenClaw 快速诊断脚本
# 用法：curl -O https://.../diagnostic.sh && bash diagnostic.sh

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║              OpenClaw 诊断报告                                  ║"
echo "╚════════════════════════════════════════════════════════════════╝"

echo -e "\n【1. 系统信息】"
uname -a
grep PRETTY_NAME /etc/os-release 2>/dev/null || true

echo -e "\n【2. Tailscale 状态】"
tailscale status 2>&1 | head -10 || echo "Tailscale 未安装/未运行"
echo "  IP 地址：$(tailscale ip 2>/dev/null | head -1 || echo 'N/A')"

echo -e "\n【3. Node.js 版本】"
node -v 2>/dev/null || echo "Node.js 未安装"
npm -v 2>/dev/null || true

echo -e "\n【4. OpenClaw 状态】"
openclaw status 2>&1 | head -20 || echo "OpenClaw 未安装/无法运行"

echo -e "\n【5. 端口监听】"
echo "  OpenClaw 端口 (18789, 18790):"
ss -tlnp 2>/dev/null | grep -E "18789|18790" || netstat -tlnp 2>/dev/null | grep -E "18789|18790" || echo "  无 OpenClaw 端口监听"

echo -e "\n【6. 防火墙状态】"
if command -v ufw &> /dev/null; then
    echo "  UFW:"
    ufw status 2>&1 | head -10
fi
if command -v firewall-cmd &> /dev/null; then
    echo "  Firewalld:"
    firewall-cmd --list-all 2>&1 | head -10
fi
if command -v iptables &> /dev/null; then
    echo "  iptables OpenClaw 规则:"
    iptables -L INPUT -n 2>/dev/null | grep -E "18789|18790" || echo "  无相关规则"
fi

echo -e "\n【7. 网关服务】"
systemctl status openclaw-gateway --no-pager -l 2>&1 | head -15 || echo "服务未安装"

echo -e "\n【8. 最近日志 (最后 10 条)】"
journalctl -u openclaw-gateway --no-pager -n 10 2>&1 || echo "无日志"

echo -e "\n【9. 连接测试】"
echo "  本地 18789 端口:"
Test-NetConnection -ComputerName localhost -Port 18789 -WarningAction SilentlyContinue -InformationLevel Quiet 2>/dev/null && echo "  ✓ 可达" || echo "  ✗ 不可达"

echo -e "\n╔════════════════════════════════════════════════════════════════╗"
echo "║                      诊断完成                                      ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "如需进一步帮助，请将以上输出发送给技术支持"
