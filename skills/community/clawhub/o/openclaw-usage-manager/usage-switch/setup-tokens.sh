#!/bin/bash
# C1/C2 トークンセットアップ（一度だけ実行）
echo "🔑 1Passwordからトークンを取得中..."

C1_TOKEN=$(op item get your-c1-item-id --reveal --format=json 2>/dev/null | python3 -c "import json,sys; d=json.load(sys.stdin); f=next((x for x in d.get('fields',[]) if str(x.get('value','')).startswith('sk-ant')),None); print(f['value'] if f else '')")
C2_TOKEN=$(op item get your-c2-item-id --reveal --format=json 2>/dev/null | python3 -c "import json,sys; d=json.load(sys.stdin); f=next((x for x in d.get('fields',[]) if str(x.get('value','')).startswith('sk-ant')),None); print(f['value'] if f else '')")

if [ -z "$C1_TOKEN" ] || [ -z "$C2_TOKEN" ]; then
  echo "❌ トークン取得失敗。1Passwordにログイン済みか確認してください"
  exit 1
fi

# 環境変数経由でPythonに渡す（シェル変数の直接展開によるインジェクション防止）
C1_TOKEN="$C1_TOKEN" C2_TOKEN="$C2_TOKEN" python3 -c "
import json, os
data = {'c1': os.environ['C1_TOKEN'], 'c2': os.environ['C2_TOKEN']}
path = os.path.join(os.environ['HOME'], '.openclaw/workspace/tools/usage-switch/tokens.json')
with open(path, 'w') as f:
    json.dump(data, f, indent=2)
print('✅ tokens.json に保存完了')
"
chmod 600 "$HOME/.openclaw/workspace/tools/usage-switch/tokens.json"
echo "✅ セットアップ完了"
