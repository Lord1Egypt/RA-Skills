#!/usr/bin/env python3
"""
OpenRouter 免费模型查询与调用工具
- 列出所有免费模型
- 调用免费模型对话
"""
import os
import sys
import json
import requests

# ========== 配置 ==========
API_KEY = os.environ.get('OPENROUTER_API_KEY', '')
if not API_KEY:
    try:
        with open('/root/.openclaw/workspace/.env', 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and 'OPENROUTER_API_KEY' in line:
                    API_KEY = line.split('=', 1)[1].strip()
    except:
        pass

API_BASE = "https://openrouter.ai/api/v1"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "https://openclaw.ai",
    "X-Title": "OpenClaw Free Models"
}

# ========== 核心功能 ==========

def list_free_models():
    """获取所有免费模型"""
    resp = requests.get(f"{API_BASE}/models", headers=HEADERS, timeout=15)
    resp.raise_for_status()
    data = resp.json()
    
    free_models = []
    for m in data.get('data', []):
        p = m.get('pricing', {})
        prompt_p = float(p.get('prompt', 1))
        completion_p = float(p.get('completion', 1))
        
        if prompt_p == 0 and completion_p == 0:
            free_models.append({
                'id': m['id'],
                'name': m.get('name', m['id']),
                'context_length': m.get('context_length', 'N/A'),
                'description': m.get('description', '')[:100],
            })
    
    return free_models


def chat_with_free_model(prompt, model='openrouter/free'):
    """调用免费模型"""
    url = f"{API_BASE}/chat/completions"
    data = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 2048,
    }
    
    resp = requests.post(url, headers=HEADERS, json=data, timeout=60)
    if resp.status_code == 403 and 'region' in resp.text.lower():
        return None, f"模型 {model} 在当前地区不可用（403）"
    
    resp.raise_for_status()
    result = resp.json()
    return result['choices'][0]['message']['content'], None


def format_free_models_list(models):
    """格式化免费模型列表"""
    lines = ["🆓 **OpenRouter 免费模型列表**\n"]
    lines.append(f"共 **{len(models)}** 个免费模型\n")
    lines.append("━━━ 推荐模型 ━━━\n")
    
    recommended = ['meta-llama/llama-3.3-70b-instruct:free', 'google/gemma-4-26b-it:free', 
                   'minimax/minimax-m2.5:free', 'google/gemma-3-27b-it:free']
    
    rec_names = {}
    for m in models:
        if m['id'] in recommended:
            rec_names[m['id']] = m['name']
    
    for rid in recommended:
        if rid in rec_names:
            lines.append(f"• **{rec_names[rid]}**\n  `/{rid}`\n")
    
    lines.append("\n━━━ 全部免费模型 ━━━\n")
    for m in models[:20]:
        lines.append(f"• `{m['id']}`\n  {m['name']} | 上下文: {m['context_length']}\n")
    
    if len(models) > 20:
        lines.append(f"\n... 还有 {len(models)-20} 个模型")
    
    lines.append("\n\n💡 使用方式：调用免费模型对话")
    return ''.join(lines)


# ========== 主入口 ==========

if __name__ == "__main__":
    if not API_KEY:
        print("错误: 未找到 OPENROUTER_API_KEY", file=sys.stderr)
        sys.exit(1)
    
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'list'
    arg = sys.argv[2] if len(sys.argv) > 2 else ''
    
    if cmd == 'list':
        models = list_free_models()
        print(format_free_models_list(models))
        
    elif cmd == 'chat':
        if not arg:
            print("用法: python3 openrouter_free.py chat <问题>", file=sys.stderr)
            sys.exit(1)
        result, err = chat_with_free_model(arg)
        if err:
            print(f"错误: {err}", file=sys.stderr)
            sys.exit(1)
        print(result)
        
    elif cmd == 'models-json':
        models = list_free_models()
        print(json.dumps(models, ensure_ascii=False, indent=2))
        
    else:
        print(f"未知命令: {cmd}", file=sys.stderr)
        print("可用命令: list | chat | models-json")
        sys.exit(1)
