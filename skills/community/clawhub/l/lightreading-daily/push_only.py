# -*- coding: utf-8 -*-
"""
科技新闻推送脚本 - 仅推送已翻译内容
"""

import json
import http.client
import urllib.parse
import os
from datetime import datetime

WEBHOOK_URL = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=66260502-9806-45ec-b23e-8db5223a9b27"
PUSHED_FILE = os.path.join(os.path.dirname(__file__), 'pushed_history.json')

def load_pushed_history():
    """加载已推送文章记录"""
    if os.path.exists(PUSHED_FILE):
        try:
            with open(PUSHED_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
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
            raise Exception('HTTP {}: {}'.format(response.status, response_body))
        
        return json.loads(response_body)
    finally:
        conn.close()

def main():
    print("=" * 60)
    print("科技新闻推送（仅推送模式）")
    print("=" * 60)
    
    output_file_cn = os.path.join(os.path.dirname(__file__), 'combined_cn.txt')
    
    if not os.path.exists(output_file_cn):
        print("\n[ERROR] 中文翻译文件不存在：{}".format(output_file_cn))
        return None
    
    # 读取中文翻译
    print("\n[INFO] 读取中文翻译文件：{}".format(output_file_cn))
    with open(output_file_cn, 'r', encoding='utf-8') as f:
        message = f.read()
    
    # 检查占位符
    if '[AI 翻译]' in message or '[待翻译]' in message or '(根据完整英文内容翻译要点' in message:
        print("\n[WARNING] 中文翻译包含占位符，跳过推送")
        return None
    
    print("[INFO] 中文翻译已完成，准备推送")
    
    # 推送
    print("\n正在发送到企业微信...")
    result = send_to_wechat(message)
    print("推送结果：{}".format(result))
    
    if result.get('errcode') == 0:
        print("OK 推送成功")
        # 保存推送记录（简化处理）
        history = load_pushed_history()
        history['daily_push_{}'.format(datetime.now().strftime('%Y%m%d'))] = datetime.now().timestamp()
        save_pushed_history(history)
        print("已保存推送记录")
    else:
        print("推送失败：{}".format(result))
    
    return result

if __name__ == '__main__':
    main()
