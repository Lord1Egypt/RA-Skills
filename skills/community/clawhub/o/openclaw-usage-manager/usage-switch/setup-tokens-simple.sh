#!/bin/bash
# シンプルセットアップ — 1Password不要
# トークンは claude setup-token コマンドで取得できます

TOKENS_FILE="$HOME/.openclaw/workspace/tools/usage-switch/tokens.json"

echo "🔑 C1アカウントのAPIトークンを入力してください（sk-ant-...）："
read -rs C1_TOKEN
echo ""
echo "🔑 C2アカウントのAPIトークンを入力してください（sk-ant-...）："
read -rs C2_TOKEN
echo ""

if [ -z "$C1_TOKEN" ] || [ -z "$C2_TOKEN" ]; then
  echo "❌ トークンが空です。キャンセルしました。"
  exit 1
fi

mkdir -p "$(dirname "$TOKENS_FILE")"
python3 -c "
import json, os
data = {'c1': os.environ['C1_TOKEN'], 'c2': os.environ['C2_TOKEN']}
with open('$TOKENS_FILE', 'w') as f:
    json.dump(data, f, indent=2)
print('✅ tokens.json に保存完了')
" C1_TOKEN="$C1_TOKEN" C2_TOKEN="$C2_TOKEN"

chmod 600 "$TOKENS_FILE"
echo "✅ セットアップ完了"
echo ""
echo "💡 トークンの取得方法: claude setup-token を実行してください"
