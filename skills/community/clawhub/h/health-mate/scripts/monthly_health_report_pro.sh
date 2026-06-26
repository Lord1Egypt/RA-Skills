#!/bin/bash
# Monthly Health-Mate report runner.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
CONFIG_DIR="${PROJECT_ROOT}/config"
LOGS_DIR="${PROJECT_ROOT}/logs"

mkdir -p "${LOGS_DIR}"

# Load environment variables from .env file
if [ -f "${CONFIG_DIR}/.env" ]; then
    set -a
    source "${CONFIG_DIR}/.env"
    set +a
else
    echo "Warning: .env was not found. Default values will be used."
fi

# Setup Cron environment for openclaw CLI
export NVM_DIR="${NVM_DIR:-/root/.nvm}"
export PATH="${CRON_PATH:-/root/.nvm/versions/node/v22.22.0/bin:/root/.local/bin:/root/bin:/home/linuxbrew/.linuxbrew/bin:/home/linuxbrew/.linuxbrew/sbin:/usr/local/bin:/usr/bin:/bin:/root/.npm-global/bin}"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"

export TZ=Asia/Shanghai
CURRENT_DATE=$(date +"%Y-%m-%d")
CURRENT_TIME=$(date +"%H:%M:%S")
LOG_FILE="${LOG_FILE:-${LOGS_DIR}/monthly_health_report_pro.log}"

if [ -z "${MEMORY_DIR:-}" ]; then
    echo "Error: MEMORY_DIR is not set." >> "$LOG_FILE"
    exit 1
fi

TARGET_DATE=$(python3 -c "
from datetime import datetime, timedelta
print((datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d'))
")

echo "========================================" >> "$LOG_FILE"
echo "Run time: ${CURRENT_DATE} ${CURRENT_TIME}" >> "$LOG_FILE"
echo "Monthly anchor date: ${TARGET_DATE}" >> "$LOG_FILE"

result=$(python3 "${SCRIPT_DIR}/monthly_report_pro.py" "$TARGET_DATE" 2>&1)
echo "$result" >> "$LOG_FILE"

delivery_message=$(echo "$result" | sed -n '/=== DELIVERY_MESSAGE_START ===/,/=== DELIVERY_MESSAGE_END ===/p' | sed '1d;$d')

if [ -z "$delivery_message" ]; then
    echo "Error: monthly delivery payload was not produced." >> "$LOG_FILE"
    exit 1
fi

python3 << PYTHON_SCRIPT
import json
import os
import urllib.request

message_text = '''${delivery_message}'''

DINGTALK_WEBHOOK = os.environ.get('DINGTALK_WEBHOOK', '')
FEISHU_WEBHOOK = os.environ.get('FEISHU_WEBHOOK', '')
TG_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '')
TG_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID', '')

def send_dingtalk():
    if not DINGTALK_WEBHOOK:
        return 'skip'
    try:
        data = json.dumps({'msgtype': 'text', 'text': {'content': message_text}}).encode('utf-8')
        req = urllib.request.Request(DINGTALK_WEBHOOK, data=data, headers={'Content-Type': 'application/json'})
        resp = urllib.request.urlopen(req, timeout=10)
        result = json.loads(resp.read().decode('utf-8'))
        return 'ok' if result.get('errcode') == 0 else 'fail'
    except Exception as error:
        return f'fail:{error}'

def send_feishu():
    if not FEISHU_WEBHOOK:
        return 'skip'
    try:
        data = json.dumps({'msg_type': 'text', 'content': {'text': message_text}}).encode('utf-8')
        req = urllib.request.Request(FEISHU_WEBHOOK, data=data, headers={'Content-Type': 'application/json'})
        resp = urllib.request.urlopen(req, timeout=10)
        result = json.loads(resp.read().decode('utf-8'))
        return 'ok' if result.get('code') == 0 else 'fail'
    except Exception as error:
        return f'fail:{error}'

def send_telegram():
    if not TG_BOT_TOKEN or not TG_CHAT_ID:
        return 'skip'
    try:
        def chunk_message(text, limit=3500):
            if len(text) <= limit:
                return [text]
            chunks, current, current_len = [], [], 0
            for paragraph in text.splitlines():
                addition = len(paragraph) + 1
                if current and current_len + addition > limit:
                    chunks.append('\\n'.join(current).strip())
                    current = [paragraph]
                    current_len = addition
                else:
                    current.append(paragraph)
                    current_len += addition
            if current:
                chunks.append('\\n'.join(current).strip())
            return [chunk for chunk in chunks if chunk]

        for index, chunk in enumerate(chunk_message(message_text), start=1):
            data = json.dumps({'chat_id': TG_CHAT_ID, 'text': chunk, 'disable_web_page_preview': True}).encode('utf-8')
            req = urllib.request.Request(f'https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage', data=data, headers={'Content-Type': 'application/json'})
            resp = urllib.request.urlopen(req, timeout=10)
            result = json.load(resp)
            if not result.get('ok'):
                return f"fail:chunk{index}:{result.get('description', 'unknown')}"
        return 'ok'
    except Exception as error:
        return f'fail:{error}'

print(f"Monthly report sent [DingTalk:{send_dingtalk()} Feishu:{send_feishu()} Telegram:{send_telegram()}]")
PYTHON_SCRIPT

echo "========================================" >> "$LOG_FILE"
