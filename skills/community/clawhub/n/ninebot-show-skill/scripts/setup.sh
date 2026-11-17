#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd -- "$SCRIPT_DIR/.." && pwd)"
VENV="$SKILL_DIR/.venv"
CONFIG_HOME="${XDG_CONFIG_HOME:-$HOME/.config}"
APP_CONFIG_DIR="$CONFIG_HOME/ninebot-show-skill"
APP_CONFIG="$APP_CONFIG_DIR/config.json"

command -v python3 >/dev/null 2>&1 || {
  echo "错误: 未找到 python3。" >&2
  exit 1
}

python3 -m venv "$VENV"
"$VENV/bin/python" -m pip install --upgrade pip
"$VENV/bin/python" -m pip install -r "$SKILL_DIR/requirements.txt"

mkdir -p "$APP_CONFIG_DIR"
chmod 700 "$APP_CONFIG_DIR" 2>/dev/null || true
if [[ ! -f "$APP_CONFIG" ]]; then
  cp "$SKILL_DIR/templates/config.example.json" "$APP_CONFIG"
  chmod 600 "$APP_CONFIG" 2>/dev/null || true
  echo "已创建配置: $APP_CONFIG"
else
  echo "保留现有配置: $APP_CONFIG"
fi

cat <<EOF2

ninebot-show-skill 依赖安装完成。

请在本机终端完成九号登录（不要把账号密码、验证码、Token 发到聊天中）：
  $VENV/bin/ninecli login
  $VENV/bin/ninecli vehicles --json

然后编辑：
  $APP_CONFIG

把 ninebot.sn 替换为车辆 wnumber。
如需中文地址或地图截图，通过环境变量设置高德 Web 服务 Key：
  AMAP_WEB_KEY=你的高德Web服务Key

完成后测试：
  $SKILL_DIR/scripts/run.sh --check
  $SKILL_DIR/scripts/run.sh
EOF2
