#!/usr/bin/env python3
"""
Dream Agent - LLM API 调用模块
使用 Python 代替 curl，更可靠的 JSON 处理
集成 Cost Tracker 自动记录 Token 消耗
"""
import urllib.request
import urllib.error
import ssl
import json
import sys
import os
from datetime import datetime

API_KEY = "sk-cp-pD1WY6KcHeUNXDeKmG4ZnzDch-sXsZKmAsNn7rXZDoAbGwc7u6XJn55Z6GbgW3qngTC-i5geM4PzDwkaSj8sQUSk2TPPj-lrLc-Yamjn-S2j4mfOT8RGKUY"
API_URL = "https://api.minimaxi.com/v1/text/chatcompletion_v2"

# Cost Tracker 配置
COST_TRACKER_SCRIPT = os.path.expanduser("~/.openclaw/workspace/skills/huo15-cost-tracker/scripts/track.sh")

def analyze_log(log_content):
    """调用 LLM 分析日志，提取记忆"""
    
    prompt = f"""你是一个记忆管理专家。请分析以下日志，提取值得长期记忆的内容。

日志内容：
{log_content}

请识别以下类型的记忆：
1. user - 用户偏好、沟通风格、习惯
2. feedback - 纠正（之前做错了什么）、确认（某方法有效）
3. project - 项目进展、决策、上下文
4. reference - 外部系统信息、资源位置

请以 JSON 格式输出，格式如下：
{{
  "memories": [
    {{
      "type": "user|feedback|project|reference",
      "name": "简短的文件名（英文）",
      "summary": "一句话总结",
      "content": "详细的记忆内容"
    }}
  ],
  "prune": [
    {{
      "name": "要删除的记忆文件名",
      "reason": "删除原因"
    }}
  ]
}}

请只输出 JSON，不要有其他内容。"""

    data = {
        "model": "MiniMax-M2.1",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3,
        "max_tokens": 2000
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

    try:
        start_time = datetime.now()
        with urllib.request.urlopen(req, context=ctx, timeout=60) as resp:
            result = json.loads(resp.read().decode('utf-8'))
            end_time = datetime.now()
            duration_ms = int((end_time - start_time).total_seconds() * 1000)
            
            # 提取 Token 使用量
            input_tokens = 0
            output_tokens = 0
            if 'usage' in result:
                input_tokens = result['usage'].get('prompt_tokens', 0)
                output_tokens = result['usage'].get('completion_tokens', 0)
            elif 'data' in result:
                input_tokens = result['data'].get('tokens', 0) // 2  # 估算
                output_tokens = result['data'].get('tokens', 0) // 2
            
            # 记录到 Cost Tracker
            try:
                os.system(f"{COST_TRACKER_SCRIPT} record "
                          f"--input-tokens {input_tokens} "
                          f"--output-tokens {output_tokens} "
                          f"--model MiniMax-M2.1 "
                          f"--duration {duration_ms} > /dev/null 2>&1")
            except:
                pass  # Cost Tracker 记录失败不影响主流程
            
            if 'choices' in result and result['choices']:
                content = result['choices'][0]['message']['content']
                # 提取 JSON
                start = content.find('{')
                end = content.rfind('}') + 1
                if start >= 0 and end > start:
                    json_str = content[start:end]
                    return json.loads(json_str)
                else:
                    return {"memories": [], "prune": []}
            
            return {"memories": [], "prune": []}
            
    except Exception as e:
        print(f"API Error: {e}", file=sys.stderr)
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: dream-api.py <log_content>")
        sys.exit(1)
    
    log_content = sys.argv[1]
    result = analyze_log(log_content)
    
    if result:
        print(json.dumps(result, ensure_ascii=False))
    else:
        print("{}", file=sys.stderr)
        sys.exit(1)
