#!/usr/bin/env python3
"""
MiniMax API Wrapper - 自动集成 Cost Tracker
任何调用 MiniMax API 的地方都可以用这个 wrapper
"""
import urllib.request
import urllib.error
import ssl
import json
import os
import time
from datetime import datetime

# ============ 配置区 ============
API_KEY = "sk-cp-pD1WY6KcHeUNXDeKmG4ZnzDch-sXsZKmAsNn7rXZDoAbGwc7u6XJn55Z6GbgW3qngTC-i5geM4PzDwkaSj8sQUSk2TPPj-lrLc-Yamjn-S2j4mfOT8RGKUY"
API_URL = "https://api.minimaxi.com/v1/text/chatcompletion_v2"

# Cost Tracker 配置
COST_TRACKER_SCRIPT = os.path.expanduser("~/.openclaw/workspace/skills/huo15-cost-tracker/scripts/track.sh")
# ============

def call_minimax(messages, model="MiniMax-M2.1", temperature=0.7, max_tokens=2000):
    """
    调用 MiniMax API，自动记录成本
    
    Args:
        messages: [{"role": "user", "content": "..."}]
        model: 模型名称
        temperature: 温度参数
        max_tokens: 最大 token 数
    
    Returns:
        API 响应结果
    """
    data = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens
    }
    
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    req = urllib.request.Request(
        API_URL,
        data=json.dumps(data).encode('utf-8'),
        headers={
            'Authorization': f'Bearer {API_KEY}',
            'Content-Type': 'application/json'
        }
    )
    
    start_time = datetime.now()
    
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=120) as resp:
            result = json.loads(resp.read().decode('utf-8'))
            end_time = datetime.now()
            duration_ms = int((end_time - start_time).total_seconds() * 1000)
            
            # 提取 Token 使用量
            input_tokens = 0
            output_tokens = 0
            if 'usage' in result:
                input_tokens = result['usage'].get('prompt_tokens', 0)
                output_tokens = result['usage'].get('completion_tokens', 0)
            
            # 记录到 Cost Tracker
            _record_cost(input_tokens, output_tokens, model, duration_ms)
            
            return result
            
    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code} - {e.reason}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"API Error: {e}", file=sys.stderr)
        return None

def _record_cost(input_tokens, output_tokens, model, duration_ms):
    """内部函数：记录成本"""
    try:
        os.system(f'{COST_TRACKER_SCRIPT} record '
                  f'--input-tokens {input_tokens} '
                  f'--output-tokens {output_tokens} '
                  f'--model "{model}" '
                  f'--duration {duration_ms} > /dev/null 2>&1')
    except:
        pass

def chat(prompt, system_prompt=None):
    """
    简单的对话接口
    
    Args:
        prompt: 用户输入
        system_prompt: 系统提示（可选）
    
    Returns:
        AI 回复文本
    """
    messages = []
    
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    
    messages.append({"role": "user", "content": prompt})
    
    result = call_minimax(messages)
    
    if result and 'choices' in result and result['choices']:
        return result['choices'][0]['message']['content']
    
    return None

# ============ 示例用法 ============
if __name__ == "__main__":
    print("🔮 MiniMax API Wrapper (with Cost Tracker)")
    print("=" * 40)
    
    # 示例调用
    response = chat("你好，请介绍一下自己")
    
    if response:
        print(f"AI: {response}")
        
        # 查看成本
        print("")
        print("💰 成本统计:")
        os.system(f"{COST_TRACKER_SCRIPT} report")
