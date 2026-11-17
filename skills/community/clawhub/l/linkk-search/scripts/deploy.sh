#!/usr/bin/env bash
# deploy.sh — SearXNG 中国特供一键部署（幂等）
# 用法: bash deploy.sh            默认端口 8888
#       SXP_PORT=8889 bash deploy.sh
set -euo pipefail

PORT="${SXP_PORT:-8888}"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DATA="$HERE/searxng-docker"

echo "[1/4] 环境检查"
OS=$(uname -s 2>/dev/null || echo Unknown)
case "$OS" in
  MINGW*|MSYS*|CYGWIN*)
    echo "检测到 Windows shell 环境。建议改用原生路径：docs/INSTALL-WINDOWS.md（方式 A），或在 WSL 终端里重新运行本脚本。继续尝试……"
    ;;
esac
command -v docker >/dev/null 2>&1 || { echo "!! 未找到 docker："; case "$OS" in Darwin) echo "   macOS 请先装 OrbStack（brew install orbstack）或 colima（brew install colima docker docker-compose && colima start --memory 2）";; MINGW*|MSYS*|CYGWIN*) echo "   Windows 请装 Docker Desktop 并启用 WSL2 后端（见 docs/INSTALL-WINDOWS.md），推荐直接走 PowerShell 原生路径";; *) echo "   Linux/NAS 安装 Docker：curl -fsSL https://get.docker.com | sh；群晖/飞牛用套件中心";; esac; exit 1; }
docker compose version >/dev/null 2>&1 || { echo "!! 未找到 docker compose 插件（老版可试 docker-compose，本包需 compose v2）。安装: sudo apt install docker-compose-plugin 或 NAS 商店更新 Docker 套件"; exit 1; }

echo "[2/4] 准备数据目录与配置"
mkdir -p "$DATA/searxng"
[ -f "$DATA/docker-compose.yml" ] || cp "$HERE/assets/docker-compose.yml" "$DATA/"
if [ ! -f "$DATA/searxng/settings.yml" ]; then
  cp "$HERE/assets/settings.seed.yml" "$DATA/searxng/settings.yml"
  SECRET="$(head -c 24 /dev/urandom | od -An -tx1 | tr -d ' \n')"
  sed -i "s/__REPLACE_ME__/$SECRET/" "$DATA/searxng/settings.yml"
  echo "    settings.yml 已生成（secret_key 已随机化）"
else
  echo "    已有 settings.yml，保持不变（升级配置请手动 diff assets 版本）"
fi

echo "[3/4] 拉取镜像并启动（端口 $PORT）"
cd "$DATA"
SXP_PORT="$PORT" docker compose up -d

echo "[4/4] 等待就绪（最多 60s）"
for i in $(seq 1 30); do
  if curl -s -o /dev/null --max-time 2 "http://127.0.0.1:$PORT/"; then echo "    Web 界面已响应"; break; fi
  sleep 2
done

echo
echo "== 部署完成 =="
echo "本机访问: http://127.0.0.1:$PORT"
echo "内网访问: http://$(hostname -I 2>/dev/null | awk '{print $1}' || echo '<本机IP>'):$PORT"
echo "请继续运行: bash scripts/selftest.sh"
