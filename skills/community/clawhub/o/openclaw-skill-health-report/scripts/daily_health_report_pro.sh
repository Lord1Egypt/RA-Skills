#!/bin/bash
# 专业版每日健康报告脚本
# 功能：读取健康记录文件，生成综合评分报告并发送到多通道
# 执行频率：每天 22:00
# 配置：从 config/ 目录的 .env 文件读取

# 获取脚本所在目录（scripts/）
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 获取项目根目录（scripts/ 的上一级）
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

# 获取配置目录
CONFIG_DIR="${PROJECT_ROOT}/config"
LOGS_DIR="${PROJECT_ROOT}/logs"

# 确保日志目录存在 (防错机制：防止因为没建 logs 文件夹导致无法写入)
mkdir -p "${LOGS_DIR}"

# 加载环境变量（从 config/目录的 .env 文件）
if [ -f "${CONFIG_DIR}/.env" ]; then
    set -a
    source "${CONFIG_DIR}/.env"
    set +a
else
    echo "警告：未找到 .env 配置文件，使用默认值"
fi

export TZ=Asia/Shanghai
CURRENT_DATE=$(date +"%Y-%m-%d")
CURRENT_TIME=$(date +"%H:%M:%S")

MEMORY_DIR="${MEMORY_DIR:-/root/.openclaw/workspace/memory}"
TODAY_FILE="${MEMORY_DIR}/${CURRENT_DATE}.md"
LOG_FILE="${LOG_FILE:-${LOGS_DIR}/health_report_pro.log}"

echo "========================================" >> "$LOG_FILE"
echo "执行时间：${CURRENT_DATE} ${CURRENT_TIME}" >> "$LOG_FILE"

if [ ! -f "$TODAY_FILE" ]; then
    echo "错误：文件不存在 - ${TODAY_FILE}" >> "$LOG_FILE"
    exit 1
fi

# 调用专业版 Python 脚本
result=$(python3 "${SCRIPT_DIR}/health_report_pro.py" "$TODAY_FILE" "$CURRENT_DATE" 2>&1)

echo "$result" >> "$LOG_FILE"

# 提取文本报告和 PDF URL
text_report=$(echo "$result" | sed -n '/=== TEXT_REPORT_START ===/,/=== TEXT_REPORT_END ===/p' | sed '1d;$d')
pdf_url=$(echo "$result" | grep "=== PDF_URL ===" -A 1 | tail -1)

if [ -z "$text_report" ] || [ -z "$pdf_url" ]; then
    echo "❌ 报告生成失败" >> "$LOG_FILE"
    exit 1
fi

# 使用 Python 发送三个通道（避免 bash 转义问题）
python3 << PYTHON_SCRIPT
import urllib.request
import json
import sys
import os

text_report = '''${text_report}'''
pdf_url = '${pdf_url}'
current_date = '${CURRENT_DATE}'

# 统一消息内容
message_text = text_report + """

━━━━━━━━━━━━━━━━━━

📄 PDF 完整报告
[点击下载](""" + pdf_url + """)"""

# 配置（从环境变量读取）
DINGTALK_WEBHOOK = os.environ.get('DINGTALK_WEBHOOK', '')
FEISHU_WEBHOOK = os.environ.get('FEISHU_WEBHOOK', '')
TG_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '')
TG_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID', '')

def send_dingtalk():
    if not DINGTALK_WEBHOOK: return '➖'  # 增加非空判断
    try:
        # 修复：钉钉 text 类型使用 {"text": {"content": "..."}} 格式
        data = json.dumps({
            'msgtype': 'text',
            'text': {
                'content': message_text
            }
        }).encode('utf-8')
        req = urllib.request.Request(DINGTALK_WEBHOOK, data=data, headers={'Content-Type': 'application/json'})
        resp = urllib.request.urlopen(req, timeout=10)
        result = json.loads(resp.read().decode('utf-8'))
        return '✅' if result.get('errcode') == 0 else '❌'
    except Exception as e:
        return f'❌:{e}'

def send_feishu():
    if not FEISHU_WEBHOOK: return '➖'  # 增加非空判断
    try:
        data = json.dumps({
            'msg_type': 'text',
            'content': {
                'text': message_text
            }
        }).encode('utf-8')
        req = urllib.request.Request(FEISHU_WEBHOOK, data=data, headers={'Content-Type': 'application/json'})
        resp = urllib.request.urlopen(req, timeout=10)
        result = json.loads(resp.read().decode('utf-8'))
        return '✅' if result.get('code') == 0 else '❌'
    except Exception as e:
        return f'❌:{e}'

def send_telegram():
    if not TG_BOT_TOKEN or not TG_CHAT_ID: return '➖'  # 增加非空判断
    try:
        data = json.dumps({
            'chat_id': TG_CHAT_ID,
            'text': message_text,
            'parse_mode': 'Markdown'
        }).encode('utf-8')
        req = urllib.request.Request(f'https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage', data=data, headers={'Content-Type': 'application/json'})
        resp = urllib.request.urlopen(req, timeout=10)
        result = json.load(resp)
        return '✅' if result.get('ok') else '❌'
    except Exception as e:
        return f'❌:{e}'

# 发送三个通道
ding_result = send_dingtalk()
feishu_result = send_feishu()
tg_result = send_telegram()

print(f"健康报告已发送 [钉钉:{ding_result} 飞书:{feishu_result} Telegram:{tg_result}]")
PYTHON_SCRIPT

echo "========================================" >> "$LOG_FILE"
