#!/usr/bin/env python3
"""
Kimi Web Search - 使用 Moonshot API 的 $web_search 内置工具进行联网搜索

Usage:
    kimi-search.py "搜索关键词"
    kimi-search.py "今天的新闻"
"""

import sys
import os
import json
from openai import OpenAI

def search(query: str, api_key: str = None) -> dict:
    """
    使用 Kimi 内置的 $web_search 工具进行联网搜索
    
    Args:
        query: 搜索关键词
        api_key: Moonshot API Key，如果不提供则从环境变量获取
    
    Returns:
        包含搜索结果的 dict
    """
    if not api_key:
        api_key = os.environ.get("MOONSHOT_API_KEY")
        if not api_key:
            raise ValueError("需要提供 MOONSHOT_API_KEY 或设置环境变量")
    
    client = OpenAI(
        api_key=api_key,
        base_url="https://api.moonshot.cn/v1",
    )
    
    messages = [
        {"role": "system", "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手。"},
        {"role": "user", "content": query}
    ]
    
    # 声明内置搜索工具
    tools = [
        {
            "type": "builtin_function",
            "function": {
                "name": "$web_search",
            }
        }
    ]
    
    finish_reason = None
    
    while finish_reason is None or finish_reason == "tool_calls":
        completion = client.chat.completions.create(
            model="kimi-k2-turbo-preview",
            messages=messages,
            temperature=0.6,
            tools=tools,
        )
        
        choice = completion.choices[0]
        finish_reason = choice.finish_reason
        
        if finish_reason == "tool_calls":
            # 模型要求执行工具调用
            messages.append(choice.message)
            
            for tool_call in choice.message.tool_calls:
                tool_call_name = tool_call.function.name
                tool_call_arguments = json.loads(tool_call.function.arguments)
                
                if tool_call_name == "$web_search":
                    # 对于内置工具，原样返回参数即可
                    tool_result = tool_call_arguments
                else:
                    tool_result = {"error": f"Unknown tool: {tool_call_name}"}
                
                # 将工具执行结果返回给模型
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": tool_call_name,
                    "content": json.dumps(tool_result),
                })
    
    # 返回最终结果
    return {
        "query": query,
        "answer": choice.message.content,
        "usage": {
            "prompt_tokens": completion.usage.prompt_tokens if completion.usage else 0,
            "completion_tokens": completion.usage.completion_tokens if completion.usage else 0,
            "total_tokens": completion.usage.total_tokens if completion.usage else 0,
        }
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: kimi-search.py <query>", file=sys.stderr)
        sys.exit(1)
    
    query = sys.argv[1]
    
    try:
        result = search(query)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
