# -*- coding: utf-8 -*-
"""
LightReading 每日摘要推送脚本 - 中文版
v3.0 AI 翻译模式：由 AI 翻译后推送中文内容
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import json
import os
import http.client
import urllib.parse
from datetime import datetime

# 企业微信 Webhook
WEBHOOK_URL = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=66260502-9806-45ec-b23e-8db5223a9b27"

# 推送记录文件
PUSHED_FILE = os.path.join(os.path.dirname(__file__), 'pushed_history.json')

def load_pushed_history():
    """加载已推送文章记录"""
    if os.path.exists(PUSHED_FILE):
        try:
            with open(PUSHED_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # 清理 7 天前的记录
                cutoff = datetime.now().timestamp() - 7 * 24 * 3600
                data = {k: v for k, v in data.items() if v > cutoff}
                return data
        except:
            pass
    return {}

def save_pushed_history(history):
    """保存已推送文章记录"""
    try:
        with open(PUSHED_FILE, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print("保存推送历史失败：{}".format(e))

def send_to_wechat(content):
    """发送到企业微信"""
    data = {"msgtype": "text", "text": {"content": content}}
    body = json.dumps(data, ensure_ascii=False).encode('utf-8')
    
    parsed = urllib.parse.urlparse(WEBHOOK_URL)
    conn = http.client.HTTPSConnection(parsed.netloc, timeout=60)
    try:
        conn.request('POST', parsed.path + '?' + parsed.query, body, {'Content-Type': 'application/json; charset=utf-8'})
        response = conn.getresponse()
        response_body = response.read().decode('utf-8')
        
        if response.status != 200:
            raise Exception(f'HTTP {response.status}: {response_body}')
        
        return json.loads(response_body)
    finally:
        conn.close()

def get_today_message():
    """获取今日推送内容（从文件读取 AI 翻译结果）"""
    # 从文件读取今日翻译内容
    cn_file = os.path.join(os.path.dirname(__file__), 'today_cn.txt')
    
    if os.path.exists(cn_file):
        with open(cn_file, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if content:
                print("[INFO] 已从 today_cn.txt 读取今日推送内容")
                return content
    
    # 文件不存在或为空，返回错误信息
    print("[ERROR] 未找到 today_cn.txt 或内容为空")
    print("[INFO] 请先运行 push_wechat.py 抓取英文，然后 AI 翻译并保存到 today_cn.txt")
    
    return """LightReading 每日摘要

【错误】今日推送内容尚未生成

请先执行以下步骤：
1. 运行 push_wechat.py 抓取英文内容
2. AI 翻译英文为中文
3. 将翻译结果保存到 today_cn.txt
4. 再运行本脚本推送

来源：LightReading.com"""

def main():
    print("=" * 60)
    print("LightReading 每日摘要推送（v3.0 中文版）")
    print("=" * 60)
    
    # 获取今日推送内容
    message = get_today_message()
    
    print("\n推送内容预览：")
    print("-" * 60)
    print(message[:500] + "..." if len(message) > 500 else message)
    print("-" * 60)
    
    print("\n正在发送到企业微信...")
    result = send_to_wechat(message)
    print("推送结果：{}".format(result))
    
    if result.get('errcode') == 0:
        print("OK 推送成功")
        # 保存推送记录
        history = load_pushed_history()
        history['last_push_cn'] = datetime.now().timestamp()
        save_pushed_history(history)
        print("已保存推送记录")
    else:
        print("推送失败：{}".format(result))
    
    return result

if __name__ == '__main__':
    main()
