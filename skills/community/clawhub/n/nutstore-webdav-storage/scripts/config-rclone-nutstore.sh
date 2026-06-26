#!/usr/bin/env bash
set -euo pipefail

RCLONE_BIN="${RCLONE_BIN:-rclone}"
NUTSTORE_URL="${NUTSTORE_URL:-https://dav.jianguoyun.com/dav/}"
REMOTE_NAME="${REMOTE_NAME:-nutstore}"

if ! command -v "$RCLONE_BIN" >/dev/null 2>&1; then
  echo "[error] rclone 未安装，请先安装 rclone" >&2
  exit 1
fi

cat <<EOF
[info] 即将进入 rclone 配置流程
建议配置：
- remote 名称：${REMOTE_NAME}
- 类型：webdav
- URL：${NUTSTORE_URL}
- vendor：other
- user：坚果云用户名
- pass：坚果云应用密码
EOF

exec "$RCLONE_BIN" config
