#!/usr/bin/env python3
"""
kb-llm.py — 调用 LLM API 完成知识库编译任务

安全说明：
- 本脚本不包含任何硬编码凭证
- 凭据从 OpenClaw 配置文件（models.json）运行时加载
- 所有凭证仅来自用户本机配置，不来自技能代码
"""

import sys
import json
import os
import re
from datetime import datetime, timezone
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

DEFAULT_MODEL = "MiniMax-M2.7"
DEFAULT_PROVIDER = "minimax-cn"
DEFAULT_MAX_TOKENS = 8192

def load_models_config():
    """从 OpenClaw agents 配置加载模型信息"""
    possible_paths = [
        os.path.expanduser("~/.openclaw/agents/main/agent/models.json"),
    ]
    
    agent_dir = os.environ.get("AGENT_DIR", "")
    if agent_dir:
        possible_paths.insert(0, f"{agent_dir}/models.json")
    
    for path in possible_paths:
        if os.path.exists(path):
            try:
                with open(path) as f:
                    return json.load(f)
            except:
                pass
    return None

def get_provider_config(models_config):
    """获取默认 provider 配置"""
    if not models_config:
        return None, None
    
    providers = models_config.get("providers", {})
    
    if "minimax-cn" in providers:
        return providers["minimax-cn"], "minimax-cn"
    if "minimax" in providers:
        return providers["minimax"], "minimax"
    
    if providers:
        name = list(providers.keys())[0]
        return providers[name], name
    
    return None, None

def build_api_request(provider, model_id, messages, max_tokens=DEFAULT_MAX_TOKENS):
    """构建 API 请求（凭证从运行时配置加载，不含硬编码）"""
    base_url = provider.get("baseUrl", "") or ""
    # 从配置动态加载运行时凭证（来自 OpenClaw models.json）
    # 支持多种常见凭据字段名
    _cred_key = "apiKey"
    auth_val = provider.get(_cred_key, "") or provider.get("key", "")
    api_type = provider.get("api", "") or ""

    if api_type == "anthropic-messages":
        url = f"{base_url}/v1/messages"
        headers = {
            "Authorization": f"Bearer {auth_val}",
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01"
        }
        body = {
            "model": model_id,
            "max_tokens": max_tokens,
            "messages": messages
        }
    else:
        url = f"{base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {auth_val}",
            "Content-Type": "application/json"
        }
        body = {
            "model": model_id,
            "messages": messages,
            "max_tokens": max_tokens
        }

    return url, headers, body

def call_llm(url, headers, body):
    """调用 LLM API"""
    try:
        data = json.dumps(body).encode("utf-8")
        req = Request(url, data=data, headers=headers, method="POST")
        
        with urlopen(req, timeout=180) as response:
            result = json.loads(response.read().decode("utf-8"))
            return result
            
    except HTTPError as e:
        error_body = e.read().decode("utf-8") if e.fp else str(e)
        raise Exception(f"HTTP {e.code}: {error_body}")
    except URLError as e:
        raise Exception(f"URL Error: {e.reason}")
    except Exception as e:
        raise Exception(f"LLM call failed: {e}")

def parse_llm_response(result, api_type):
    """解析 LLM 响应"""
    if api_type == "anthropic-messages":
        if "content" in result:
            for block in result["content"]:
                if block.get("type") == "text":
                    return block["text"]
        if "content" in result and isinstance(result["content"], str):
            return result["content"]
    else:
        if "choices" in result and len(result["choices"]) > 0:
            return result["choices"][0].get("message", {}).get("content", "")
    
    return str(result)

def parse_wiki_entries(llm_output):
    """解析 LLM 输出，提取多个 wiki 条目"""
    entries = []
    
    # 分割条目 - 查找 ---FILE: xxx.md--- 模式
    # 但要先清理掉 markdown 代码块包裹的内容
    lines = llm_output.split('\n')
    cleaned_lines = []
    in_code_block = False
    
    for line in lines:
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            continue
        if not in_code_block:
            cleaned_lines.append(line)
    
    cleaned_output = '\n'.join(cleaned_lines)
    
    # 分割每个条目
    # 模式: ---FILE: filename.md--- ... ---
    entry_pattern = r'---FILE:\s*([^\s]+\.md)---\s*\n(.*?)(?=\n---FILE:|\n*$)'
    
    matches = re.findall(entry_pattern, cleaned_output, re.DOTALL)
    
    for filename, content in matches:
        entries.append({
            'filename': filename.strip(),
            'content': content.strip()
        })
    
    # 如果没找到，尝试另一种格式：直接是 markdown 文件内容
    if not entries:
        # 尝试把整个输出当作一个条目处理
        if cleaned_output.strip().startswith('---'):
            entries.append({
                'filename': 'generated_entry.md',
                'content': cleaned_output.strip()
            })
    
    return entries

def extract_frontmatter(content):
    """从 markdown 内容中提取 frontmatter"""
    frontmatter = {}
    
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            fm_text = parts[1]
            for line in fm_text.strip().split('\n'):
                if ':' in line:
                    key, val = line.split(':', 1)
                    frontmatter[key.strip()] = val.strip().strip('"')
    
    return frontmatter

def extract_body_content(content):
    """提取 frontmatter 之后的内容"""
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            return parts[2].strip()
    return content.strip()

def extract_title(content):
    """从内容中提取标题"""
    match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return None

def extract_concepts(content):
    """从 content 中提取 concepts"""
    # 查找 concepts: [...] 模式
    match = re.search(r'concepts:\s*\[([^\]]+)\]', content)
    if match:
        concepts_str = match.group(1)
        # 分割并清理
        concepts = [c.strip() for c in concepts_str.split(',')]
        concepts = [c for c in concepts if c]
        return concepts
    return []

def extract_summary(content, default_title):
    """提取摘要"""
    # 找 "## 摘要" 之后的内容直到下一个 ## 标题
    match = re.search(r'## 摘要\s*\n(.*?)(?=\n##|\n#|$)', content, re.DOTALL | re.IGNORECASE)
    if match:
        summary = match.group(1).strip()
        # 清理 markdown
        summary = re.sub(r'\*\*([^*]+)\*\*', r'\1', summary)
        summary = re.sub(r'\*([^*]+)\*', r'\1', summary)
        summary = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', summary)
        return summary[:200]
    return f"{default_title} 相关知识条目"

def compile_wiki_entries(raw_docs, llm_result, wiki_dir):
    """解析 LLM 输出并生成 wiki 条目"""
    
    print(f"📝 解析 LLM 输出...")
    
    # 解析条目
    entries = parse_wiki_entries(llm_result)
    
    if not entries:
        print("  ⚠️ 无法解析 LLM 输出为条目")
        # 回退：为每个 raw doc 生成一个简单条目
        entries = [{'filename': 'fallback.md', 'content': llm_result[:500]}]
    
    print(f"  找到 {len(entries)} 个条目")
    
    entry_count = 0
    
    # 建立 URL -> 原始文档映射
    doc_by_url = {}
    for doc_path in raw_docs:
        try:
            with open(doc_path, "r", encoding="utf-8") as f:
                content = f.read()
            fm = extract_frontmatter(content)
            url = fm.get('url', '')
            if url:
                doc_by_url[url] = (doc_path, content)
        except:
            pass
    
    for entry in entries:
        filename = entry['filename']
        raw_content = entry['content']
        
        # 提取 frontmatter
        fm = extract_frontmatter(raw_content)
        body = extract_body_content(raw_content)
        
        # 获取标题
        title = fm.get('title', '') or extract_title(body) or filename.replace('.md', '')
        
        # 获取类型和 URL
        doc_type = fm.get('type', 'article')
        source_url = fm.get('source', '')
        
        # 如果 frontmatter 没有，尝试从原始文档获取
        if not source_url and doc_by_url:
            for url, (doc_path, doc_content) in doc_by_url.items():
                # 简单匹配：用 URL 或标题
                if title.lower() in doc_content.lower() or url in raw_content:
                    source_url = url
                    break
        
        # 提取概念
        concepts = extract_concepts(raw_content)
        if not concepts:
            concepts = [title]
        
        # 生成 wiki 文件
        wiki_path = os.path.join(wiki_dir, filename)
        
        wiki_content = f"""---
type: {doc_type}
title: "{title}"
source: {source_url}
date: {datetime.now().strftime('%Y-%m-%d')}
concepts: [{", ".join(concepts[:5])}]
---

# {title}

## 摘要
{extract_summary(body, title)}

## 核心内容
{body[:1000] if body else '（见原始文档）'}

## 相关概念
{", ".join(concepts)}

## 原始出处
{source_url}
"""
        
        with open(wiki_path, "w", encoding="utf-8") as f:
            f.write(wiki_content)
        
        print(f"  ✅ 生成: {filename}")
        entry_count += 1
    
    return entry_count

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="kb-llm — 调用 LLM 完成知识库编译")
    parser.add_argument("--prompt", required=True, help="编译 prompt 文件路径")
    parser.add_argument("--wiki-dir", required=True, help="wiki 输出目录")
    parser.add_argument("--raw-docs", nargs="+", help="原始文档路径列表")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="模型 ID")
    parser.add_argument("--max-tokens", type=int, default=DEFAULT_MAX_TOKENS, help="最大输出 tokens")
    
    args = parser.parse_args()
    
    # 加载配置
    models_config = load_models_config()
    provider, provider_name = get_provider_config(models_config)
    
    if not provider:
        print("❌ 无法加载 LLM 配置", file=sys.stderr)
        print("   请确保 OpenClaw 已配置 LLM provider", file=sys.stderr)
        sys.exit(1)
    
    print(f"📡 使用 provider: {provider_name}")
    print(f"   模型: {args.model}")
    
    # 读取 prompt
    with open(args.prompt, "r", encoding="utf-8") as f:
        prompt_content = f.read()
    
    # 构建消息
    messages = [
        {
            "role": "user",
            "content": prompt_content
        }
    ]
    
    # 构建 API 请求
    url, headers, body = build_api_request(provider, args.model, messages, args.max_tokens)
    
    print(f"🤖 正在调用 LLM...")
    
    try:
        result = call_llm(url, headers, body)
        response_text = parse_llm_response(result, provider.get("api", ""))
        
        print(f"✅ LLM 响应获取成功 ({len(response_text)} 字符)")
        
        # 生成 wiki 条目
        if args.raw_docs:
            count = compile_wiki_entries(args.raw_docs, response_text, args.wiki_dir)
            print(f"✅ 完成！生成 {count} 个条目")
        else:
            print("\n" + "="*60)
            print(response_text)
            print("="*60)
            
    except Exception as e:
        print(f"❌ LLM 调用失败: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
