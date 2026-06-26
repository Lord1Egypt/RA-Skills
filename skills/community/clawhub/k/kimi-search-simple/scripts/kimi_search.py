#!/usr/bin/env python3
"""
Kimi Web Search Tool
Use Kimi API's builtin_function $web_search to perform web search

Usage:
    python3 search.py "your search query"
    python3 search.py "q" --raw
    python3 search.py "Apple latest earnings 2025"

Environment:
    MOONSHOT_API_KEY: Kimi API Key (required)
"""

import argparse
import os
import sys
import json
from typing import Dict, Any

try:
    from openai import OpenAI
except ImportError:
    print("Error: openai package not installed. Run: pip install openai")
    sys.exit(1)


def get_api_key() -> str:
    """Get Moonshot/Kimi API Key from environment or config file"""
    # Try environment variable first
    api_key = os.environ.get("MOONSHOT_API_KEY") or os.environ.get("KIMI_API_KEY")
    
    if not api_key:
        # Try config files
        config_paths = [
            os.path.expanduser("~/.config/moonshot/api_key"),
            os.path.expanduser("~/.openclaw/credentials/moonshot-api-key"),
        ]
        for path in config_paths:
            if os.path.exists(path):
                with open(path, "r") as f:
                    api_key = f.read().strip()
                    if api_key:
                        break
    
    if not api_key:
        print("Error: MOONSHOT_API_KEY not found.")
        print("Please set it as environment variable or create ~/.config/moonshot/api_key")
        print("Get your API key from: https://platform.moonshot.cn/")
        sys.exit(1)
    
    return api_key


DEFAULT_SYSTEM = (
    "You are Kimi, a helpful AI assistant. Use web search to get latest information "
    "and provide accurate, detailed answers."
)
RAW_OUTPUT_SYSTEM = """
你是 Kimi。用户需要基于联网搜索的原始材料展示。
请逐条输出：
  Title: [标题]
  Date：[具体日期，如 2026-04-01]
  URL：[这里填入超链接URL]
  Summary：[搜索结果中的摘要]
禁止仅用一句话概括（例如「以上为…汇总」），禁止省略具体条目。
"""


def search(query: str, model: str = "kimi-k2-turbo-preview", raw_output: bool = False) -> str:
    """
    Perform web search using Kimi's $web_search builtin_function
    
    Args:
        query: Search query string
        model: Model name (default: kimi-k2-turbo-preview for larger context)
        raw_output: If True, after tool round-trip use a strict system prompt so the model lists excerpts instead of a one-liner summary
    
    Returns:
        AI-synthesized search results
    """
    import httpx
    
    # Create HTTP client with timeout
    http_client = httpx.Client(
        base_url="https://api.moonshot.cn/v1",
        timeout=60.0,
        follow_redirects=True,
    )
    
    client = OpenAI(
        base_url="https://api.moonshot.cn/v1",
        api_key=get_api_key(),
        http_client=http_client,
    )
    
    # Declare $web_search as builtin_function
    tools = [
        {
            "type": "builtin_function",
            "function": {
                "name": "$web_search",
            },
        },
    ]
    
    messages = [
        {"role": "system", "content": DEFAULT_SYSTEM},
        {"role": "user", "content": query},
    ]
    
    max_iterations = 3
    iteration = 0
    
    while iteration < max_iterations:
        iteration += 1
        
        # Send request to Kimi API
        completion = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
            temperature=0.3 if raw_output else 0.6,
            max_tokens=8192,
            extra_body={"thinking": {"type": "disabled"}},
        )
        
        choice = completion.choices[0]
        
        if choice.finish_reason != "tool_calls":
            return choice.message.content
        
        messages.append(choice.message)
        
        for tool_call in choice.message.tool_calls:
            tool_call_name = tool_call.function.name
            tool_call_arguments = json.loads(tool_call.function.arguments)
            
            if tool_call_name == "$web_search":
                usage = tool_call_arguments.get("usage", {})
                if usage:
                    print(f"[Search] Content tokens: {usage.get('total_tokens', 'N/A')}", file=sys.stderr)
                
                # Return arguments back to Kimi for internal execution
                tool_result = tool_call_arguments
            else:
                tool_result = {"error": f"Unknown tool: {tool_call_name}"}
            
            # Add tool result to messages
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": tool_call_name,
                "content": json.dumps(tool_result),
            })
        
        if raw_output:
            messages[0] = {"role": "system", "content": RAW_OUTPUT_SYSTEM}
    
    return "Error: Max iterations reached"


def main():
    parser = argparse.ArgumentParser(prog="search.py")
    parser.add_argument("-q", "--query", required=True, help="search query")
    parser.add_argument("-r", "--raw", action="store_true")
    args = parser.parse_args()
    raw_output = args.raw
    print(f"Searching: {args.query}\n", file=sys.stderr)
    print(search(args.query, raw_output=raw_output))


if __name__ == "__main__":
    main()
