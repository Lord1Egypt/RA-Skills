#!/usr/bin/env bash
set -euo pipefail

API_URL="https://agent.mathmind.cn/minimalist/api/imgEditNB2"
DEFAULT_RATIO="auto"
DEFAULT_SIZE="1K"
TIMEOUT=600  # 10分钟超时，nano-banana2生成时间较长

prompt=""
ratio="$DEFAULT_RATIO"
size="$DEFAULT_SIZE"
urls=()
use_local_key="false"

require_cmd() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "Error: missing required command '$1'"
    exit 1
  fi
}

require_cmd "curl"
require_cmd "python3"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --prompt)
      prompt="${2:-}"
      shift 2
      ;;
    --url)
      urls+=("${2:-}")
      shift 2
      ;;
    --ratio)
      ratio="${2:-}"
      shift 2
      ;;
    --size)
      size="${2:-}"
      shift 2
      ;;
    --use-local-key)
      use_local_key="true"
      shift
      ;;
    *)
      echo "Unknown argument: $1"
      exit 1
      ;;
  esac
done

if [[ -z "$prompt" ]]; then
  echo "Error: --prompt is required"
  exit 1
fi

if [[ -z "${X_API_KEY:-}" && "$use_local_key" == "true" && -f "$HOME/.config/nano-banana2/.env" ]]; then
  require_cmd "grep"
  require_cmd "tail"
  require_cmd "cut"
  require_cmd "tr"
  # Safely read key-value from .env without executing file content.
  X_API_KEY=$(grep -E '^X_API_KEY=' "$HOME/.config/nano-banana2/.env" | tail -n 1 | cut -d'=' -f2- | tr -d '\r')
fi

if [[ -z "${X_API_KEY:-}" ]]; then
  echo "Error: missing X_API_KEY"
  echo "Hint: export X_API_KEY first, or use --use-local-key to read ~/.config/nano-banana2/.env"
  exit 1
fi

case "$ratio" in
  auto|1:1|16:9|9:16|4:3|3:4|3:2|2:3|5:4|4:5|21:9) ;;
  *) ratio="$DEFAULT_RATIO" ;;
esac

case "$size" in
  1K|2K|4K) ;;
  *) size="$DEFAULT_SIZE" ;;
esac

urls_json="[]"
if [[ ${#urls[@]} -gt 0 ]]; then
  urls_json=$(printf '%s\n' "${urls[@]}" | python3 -c "import json,sys; print(json.dumps([line.strip() for line in sys.stdin if line.strip()]))")
fi

payload=$(python3 -c "import json,sys; print(json.dumps({'urls': json.loads(sys.argv[1]), 'prompt': sys.argv[2], 'aspectRatio': sys.argv[3], 'imageSize': sys.argv[4]}, ensure_ascii=False))" "$urls_json" "$prompt" "$ratio" "$size")

# 带超时调用，只执行一次
response=$(curl -s -m "$TIMEOUT" --location "$API_URL" \
  --header 'Content-Type: application/json' \
  --header "x-api-key: $X_API_KEY" \
  --data "$payload" 2>&1)

# 检查是否超时或错误
if [[ "$response" == "" ]]; then
  echo "ERROR:请求超时（${TIMEOUT}秒）"
  exit 1
fi

echo "$response" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    if data.get('code') == 0:
        d = data.get('data', {})
        if isinstance(d, dict) and d.get('image_url'):
            print('IMAGE_URL:' + d['image_url'])
        elif isinstance(d, dict) and isinstance(d.get('array'), list) and d['array'] and isinstance(d['array'][0], dict) and d['array'][0].get('url'):
            print('IMAGE_URL:' + d['array'][0]['url'])
        else:
            print('SUCCESS:' + json.dumps(data, ensure_ascii=False))
    else:
        print('ERROR:' + data.get('errorMessage', 'Unknown error'))
except:
    print('ERROR:解析失败 - ' + sys.stdin.read()[:200])
"