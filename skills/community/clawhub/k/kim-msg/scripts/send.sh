#!/usr/bin/env bash
# Kim 消息发送包装脚本
# 智能密钥加载：环境变量优先，自动 fallback 到密钥文件
# 用法：./send.sh -u <用户名> -m <消息内容>

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 常见密钥文件路径（按优先级排序）
CREDENTIAL_FILES=(
  "$HOME/.openclaw/.secrets"
  "$HOME/.kim_credentials"
  "./kim_credentials"
)

# 从密钥文件加载密钥
load_credentials() {
  for cred_file in "${CREDENTIAL_FILES[@]}"; do
    if [[ -f "$cred_file" ]]; then
      local app_key=$(grep "^KIM_APPKEY=" "$cred_file" 2>/dev/null | cut -d= -f2 | tr -d '[:space:]')
      local secret_key=$(grep "^KIM_SECRET=" "$cred_file" 2>/dev/null | cut -d= -f2 | tr -d '[:space:]')
      
      if [[ -n "$app_key" && -n "$secret_key" ]]; then
        echo "$app_key:$secret_key"
        return 0
      fi
    fi
  done
  return 1
}

# 检查环境变量
has_env_credentials() {
  [[ -n "$KIM_APP_KEY" && -n "$KIM_SECRET_KEY" ]]
}

# 主逻辑
if has_env_credentials; then
  # 环境变量已设置，直接使用
  exec "$SCRIPT_DIR/message.js" "$@"
else
  # 环境变量未设置，尝试从文件加载
  credentials=$(load_credentials) || {
    echo "❌ 错误：缺少 Kim 密钥配置"
    echo ""
    echo "请用以下任一方式配置："
    echo "  1. 设置环境变量："
    echo "     export KIM_APP_KEY=your_app_key"
    echo "     export KIM_SECRET_KEY=your_secret_key"
    echo ""
    echo "  2. 创建密钥文件（推荐）："
    echo "     KIM_APPKEY=your_app_key"
    echo "     KIM_SECRET=your_secret_key"
    echo ""
    echo "     支持的文件位置："
    echo "     - ~/.openclaw/.secrets"
    echo "     - ~/.kim_credentials"
    echo "     - ./kim_credentials"
    exit 1
  }
  
  # 导出密钥并执行
  export KIM_APP_KEY=$(echo "$credentials" | cut -d: -f1)
  export KIM_SECRET_KEY=$(echo "$credentials" | cut -d: -f2)
  exec "$SCRIPT_DIR/message.js" "$@"
fi
