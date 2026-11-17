#!/bin/sh
# 邮件通知器示例：用 sendmail（或 msmtp 的 sendmail 兼容接口）发送 stdin 正文。
#
# 依赖：系统 sendmail（或 msmtp）。在 config.yaml 中把 env.RECIPIENT/SENDER
# 换成真实邮箱，并确保 sendmail 已正确配置转发。
set -eu

RECIPIENT="${RECIPIENT:-}"
SENDER="${SENDER:-gold-tracker@localhost}"
SUBJECT="${SUBJECT:-黄金追踪提醒}"

if [ -z "$RECIPIENT" ]; then
  echo "ERROR: RECIPIENT 未配置" >&2
  exit 1
fi

{
  echo "From: $SENDER"
  echo "To: $RECIPIENT"
  echo "Subject: $SUBJECT"
  echo "Content-Type: text/plain; charset=UTF-8"
  echo
  cat
} | /usr/sbin/sendmail -t

echo "SENT"
