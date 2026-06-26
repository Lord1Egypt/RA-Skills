#!/usr/bin/env python3
"""油价智能提醒脚本"""
import json, subprocess, re, sys
from datetime import datetime, timedelta

SF = '/workspace/memory/oil_state.json'
try:
    with open(SF) as f: state = json.load(f)
except:
    state = {"last_remind_date": "", "next_adjust_date": "2026-04-07", "trend": None}

today = datetime.now().strftime('%Y-%m-%d')

def curl(url):
    try:
        r = subprocess.run(['curl', '-s', url], capture_output=True, text=True, timeout=12)
        return r.stdout
    except: return ""

html = curl("https://www.ndrc.gov.cn/xwdt/xwfb/")
matches = re.findall(r'href="(/xwdt/xwfb/[^"]+)"[^>]*>([^<]*油价[^<]*)<', html)

news_text = ""
for url, title in matches[:3]:
    content = curl("https://www.ndrc.gov.cn" + url)
    if content and any(k in content for k in ['上调', '下调', '不作调整']):
        news_text = title.strip() + " | " + content[:200]
        break

trend = None
if '上调' in news_text or '上涨' in news_text: trend = 'up'
elif '下调' in news_text or '下降' in news_text or '降低' in news_text: trend = 'down'

d = datetime(2026, 3, 23)
cnt = 0
while cnt < 10:
    d += timedelta(days=1)
    if d.weekday() < 5: cnt += 1
next_date = d.strftime('%Y-%m-%d')
days_left = (d - datetime.now()).days

msg = None
if 1 <= days_left <= 10:
    if trend == 'up':
        msg = f"🌿 【油价提醒】预计{days_left}天后（{next_date}零点）油价将上调，建议近日安排加满油箱！"
    elif trend == 'down':
        msg = f"🌿 【油价提醒】预计{days_left}天后（{next_date}零点）油价将下调，建议调价后再去加油，可节省费用！"
    else:
        msg = f"🌿 【油价提醒】下一轮油价调整窗口约在 {next_date}（约{days_left}天后），届时油价可能有变动，如需加油请留意。"

state['last_check'] = today
state['trend'] = trend
state['next_adjust_date'] = next_date
state['days_left'] = days_left
with open(SF, 'w') as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

print(msg if msg else "NO_REMINDER")
