#!/usr/bin/env bash
# email-negotiator.sh — 邮件谈判核心脚本
# 依赖：bash, curl, python3, IMAP/SMTP 配置
# 配置文件：~/.openclaw/workspace/config/email.conf

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
CONFIG_FILE="${EMAIL_CONFIG:-$SKILL_DIR/config/email.conf}"
REPORTS_DIR="${REPORTS_DIR:-$SKILL_DIR/reports}"
TEMPLATES_DIR="$SKILL_DIR/references/email-templates"

# ─── 加载配置 ────────────────────────────────────────────────────────────────
load_config() {
  if [[ ! -f "$CONFIG_FILE" ]]; then
    echo "[ERROR] 配置文件不存在: $CONFIG_FILE"
    echo "请创建配置文件，参考格式："
    cat <<'EOF'
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USER=procurement@example.com
SMTP_PASS=your_password
IMAP_HOST=imap.example.com
IMAP_PORT=993
IMAP_USER=procurement@example.com
IMAP_PASS=your_password
SENDER_NAME=采购部
EOF
    exit 1
  fi
  # shellcheck source=/dev/null
  source "$CONFIG_FILE"
}

# ─── 发送邮件（单封）────────────────────────────────────────────────────────
send_email() {
  local to="$1"
  local subject="$2"
  local body="$3"

  python3 - <<PYEOF
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

msg = MIMEMultipart('alternative')
msg['Subject'] = """$subject"""
msg['From'] = f"${SENDER_NAME:-采购部} <${SMTP_USER}>"
msg['To'] = """$to"""

part = MIMEText("""$body""", 'plain', 'utf-8')
msg.attach(part)

with smtplib.SMTP('${SMTP_HOST}', ${SMTP_PORT}) as server:
    server.starttls()
    server.login('${SMTP_USER}', '${SMTP_PASS}')
    server.sendmail('${SMTP_USER}', """$to""", msg.as_string())
    print(f"[OK] 邮件已发送至 $to")
PYEOF
}

# ─── 批量发送询价邮件 ─────────────────────────────────────────────────────────
cmd_send() {
  local template="inquiry"
  local suppliers_file=""
  local product=""
  local quantity=""
  local target_price=""

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --template) template="$2"; shift 2 ;;
      --suppliers) suppliers_file="$2"; shift 2 ;;
      --product) product="$2"; shift 2 ;;
      --quantity) quantity="$2"; shift 2 ;;
      --target-price) target_price="$2"; shift 2 ;;
      *) echo "[WARN] 未知参数: $1"; shift ;;
    esac
  done

  if [[ -z "$suppliers_file" || ! -f "$suppliers_file" ]]; then
    echo "[ERROR] 供应商文件不存在: $suppliers_file"
    exit 1
  fi

  load_config

  local sent=0
  local failed=0

  # 跳过 CSV 表头，逐行处理
  tail -n +2 "$suppliers_file" | while IFS=',' read -r name email product_type history_price priority _rest; do
    # 去除引号和空白
    name=$(echo "$name" | tr -d '"' | xargs)
    email=$(echo "$email" | tr -d '"' | xargs)

    if [[ -z "$email" ]]; then
      echo "[SKIP] 供应商 $name 无邮箱，跳过"
      continue
    fi

    # 读取话术模板
    local template_file="$TEMPLATES_DIR/${template}.txt"
    if [[ ! -f "$template_file" ]]; then
      echo "[ERROR] 话术模板不存在: $template_file"
      exit 1
    fi

    # 替换模板变量
    local body
    body=$(sed \
      -e "s/{{SUPPLIER_NAME}}/$name/g" \
      -e "s/{{PRODUCT}}/${product:-$product_type}/g" \
      -e "s/{{QUANTITY}}/${quantity:-待定}/g" \
      -e "s/{{TARGET_PRICE}}/${target_price:-面议}/g" \
      "$template_file")

    local subject="询价函 — ${product:-$product_type} 采购需求"

    if send_email "$email" "$subject" "$body"; then
      ((sent++)) || true
      echo "[$(date '+%H:%M:%S')] 已发送: $name <$email>"
    else
      ((failed++)) || true
      echo "[ERROR] 发送失败: $name <$email>"
    fi

    # 避免触发邮件服务器频率限制
    sleep 1
  done

  echo ""
  echo "━━━ 发送完成 ━━━"
  echo "成功: $sent 封 | 失败: $failed 封"
}

# ─── 解析收件箱报价 ───────────────────────────────────────────────────────────
cmd_parse() {
  local output_file="$REPORTS_DIR/quotes.csv"

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --inbox) shift ;;
      --output) output_file="$2"; shift 2 ;;
      *) shift ;;
    esac
  done

  load_config
  mkdir -p "$(dirname "$output_file")"

  python3 - <<PYEOF
import imaplib
import email
import re
import csv
import os
from datetime import datetime

# 连接 IMAP
mail = imaplib.IMAP4_SSL('${IMAP_HOST}', ${IMAP_PORT})
mail.login('${IMAP_USER}', '${IMAP_PASS}')
mail.select('INBOX')

# 搜索最近30天的邮件
_, msg_ids = mail.search(None, 'SINCE', (datetime.now().strftime('%d-%b-%Y')))

results = []
for msg_id in msg_ids[0].split():
    _, msg_data = mail.fetch(msg_id, '(RFC822)')
    msg = email.message_from_bytes(msg_data[0][1])

    sender = msg.get('From', '')
    subject = msg.get('Subject', '')
    date = msg.get('Date', '')

    # 提取邮件正文
    body = ''
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == 'text/plain':
                body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                break
    else:
        body = msg.get_payload(decode=True).decode('utf-8', errors='ignore')

    # 简单价格提取（匹配 ¥/元/RMB + 数字）
    price_patterns = [
        r'[¥￥]\s*(\d+(?:[,，]\d{3})*(?:\.\d+)?)',
        r'(\d+(?:[,，]\d{3})*(?:\.\d+)?)\s*元',
        r'单价[：:]\s*(\d+(?:\.\d+)?)',
        r'报价[：:]\s*(\d+(?:\.\d+)?)',
    ]
    prices = []
    for pattern in price_patterns:
        matches = re.findall(pattern, body)
        prices.extend([m.replace(',', '').replace('，', '') for m in matches])

    results.append({
        'sender': sender,
        'subject': subject,
        'date': date,
        'extracted_prices': '|'.join(prices[:3]),  # 最多取3个价格
        'body_preview': body[:200].replace('\n', ' '),
    })

mail.logout()

# 写入 CSV
output_path = """$output_file"""
with open(output_path, 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.DictWriter(f, fieldnames=['sender', 'subject', 'date', 'extracted_prices', 'body_preview'])
    writer.writeheader()
    writer.writerows(results)

print(f"[OK] 解析完成，共 {len(results)} 封邮件 → {output_path}")
PYEOF
}

# ─── 发起多轮议价 ─────────────────────────────────────────────────────────────
cmd_negotiate() {
  local round=2
  local strategy="pressure"
  local quotes_file="$REPORTS_DIR/quotes.csv"

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --round) round="$2"; shift 2 ;;
      --strategy) strategy="$2"; shift 2 ;;
      --quotes) quotes_file="$2"; shift 2 ;;
      *) shift ;;
    esac
  done

  if [[ ! -f "$quotes_file" ]]; then
    echo "[ERROR] 报价文件不存在: $quotes_file，请先运行 parse"
    exit 1
  fi

  load_config

  local template_file="$TEMPLATES_DIR/negotiate-round${round}-${strategy}.txt"
  if [[ ! -f "$template_file" ]]; then
    # 降级到通用压价模板
    template_file="$TEMPLATES_DIR/negotiate-pressure.txt"
  fi

  if [[ ! -f "$template_file" ]]; then
    echo "[ERROR] 谈判话术模板不存在: $template_file"
    exit 1
  fi

  echo "[INFO] 第 $round 轮谈判，策略: $strategy"
  echo "[INFO] 话术模板: $template_file"
  echo ""

  local sent=0
  tail -n +2 "$quotes_file" | while IFS=',' read -r sender subject date prices preview _rest; do
    # 从 sender 提取邮箱
    local email
    email=$(echo "$sender" | grep -oE '[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}' | head -1)

    if [[ -z "$email" ]]; then
      continue
    fi

    local body
    body=$(sed \
      -e "s/{{ROUND}}/$round/g" \
      -e "s/{{STRATEGY}}/$strategy/g" \
      -e "s/{{QUOTED_PRICE}}/$prices/g" \
      "$template_file")

    local reply_subject="Re: $subject"

    if send_email "$email" "$reply_subject" "$body"; then
      ((sent++)) || true
      echo "[$(date '+%H:%M:%S')] 第${round}轮已发送: $email"
    fi

    sleep 1
  done

  echo ""
  echo "━━━ 第 $round 轮谈判邮件发送完成，共 $sent 封 ━━━"
}

# ─── 主入口 ───────────────────────────────────────────────────────────────────
main() {
  local cmd="${1:-help}"
  shift || true

  case "$cmd" in
    send)      cmd_send "$@" ;;
    parse)     cmd_parse "$@" ;;
    negotiate) cmd_negotiate "$@" ;;
    help|--help|-h)
      echo "用法: email-negotiator.sh <命令> [参数]"
      echo ""
      echo "命令:"
      echo "  send       批量发送询价邮件"
      echo "  parse      解析收件箱报价"
      echo "  negotiate  发起多轮议价"
      echo ""
      echo "示例:"
      echo "  send --template inquiry --suppliers ./suppliers.csv --product 笔记本 --quantity 100"
      echo "  parse --inbox --output ./reports/quotes.csv"
      echo "  negotiate --round 2 --strategy pressure"
      ;;
    *)
      echo "[ERROR] 未知命令: $cmd"
      exit 1
      ;;
  esac
}

main "$@"
