#!/usr/bin/env python3
"""
发送飞书复盘通知
通过 OpenClaw sessions_send 发送消息
"""

import json
import sys
from pathlib import Path
from datetime import datetime

WORKSPACE = Path('/root/.openclaw/workspace')

def get_latest_report():
    """获取最新的复盘报告"""
    today = datetime.now().strftime('%Y-%m-%d')
    report_file = WORKSPACE / f'每日复盘_{today}.md'
    
    if report_file.exists():
        with open(report_file, 'r', encoding='utf-8') as f:
            return f.read()
    return None

def extract_summary(report_content):
    """从报告中提取摘要"""
    if not report_content:
        return None
    
    lines = report_content.split('\n')
    summary = []
    
    # 提取关键信息
    for line in lines:
        if '上证指数' in line:
            summary.append(line.strip())
        elif '深证成指' in line:
            summary.append(line.strip())
        elif '创业板指' in line:
            summary.append(line.strip())
        elif '持仓盈亏' in line:
            summary.append(line.strip())
        elif '祥龙电业' in line and '现价' in line:
            summary.append(line.strip())
    
    return '\n'.join(summary[:6])

def create_feishu_message(summary):
    """创建飞书消息卡片"""
    if not summary:
        return None
    
    message = {
        "msg_type": "text",
        "content": {
            "text": f"📊 每日股市复盘\n\n{summary}\n\n详细报告：/root/.openclaw/workspace/每日复盘_*.md"
        }
    }
    
    return json.dumps(message, ensure_ascii=False)

def main():
    """主函数"""
    print("📱 发送飞书复盘通知...\n")
    
    # 获取最新报告
    report = get_latest_report()
    if not report:
        print("❌ 未找到今日复盘报告")
        return 1
    
    # 提取摘要
    summary = extract_summary(report)
    
    # 创建消息
    message = create_feishu_message(summary)
    if not message:
        print("❌ 创建消息失败")
        return 1
    
    print(f"📝 消息内容：\n{summary}\n")
    
    # 输出消息 JSON，由调用方发送
    print(f"\n✅ 消息 JSON：\n{message}")
    
    # 保存到待发送文件
    pending_file = WORKSPACE / 'feishu_pending_message.json'
    with open(pending_file, 'w', encoding='utf-8') as f:
        f.write(message)
    
    print(f"\n💾 已保存到：{pending_file}")
    print(f"⏳ 等待 OpenClaw 发送...")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
