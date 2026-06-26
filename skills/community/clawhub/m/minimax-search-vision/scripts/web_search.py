"""
MiniMax 网络搜索工具

通过 MiniMax Token Plan MCP 提供的 web_search 工具进行网络搜索

注意：此工具依赖于 MiniMax Token Plan MCP 服务。
如果 MCP 调用失败，请检查 mcporter 配置是否正确。
"""

import json
import subprocess
import sys
from pathlib import Path
from typing import Optional

try:
    from .config import get_api_key, masked_key, get_api_host
except ImportError:
    from config import get_api_key, masked_key, get_api_host


def search_via_mcp(query: str) -> dict:
    """
    通过 mcporter 调用 MiniMax MCP 的 web_search 工具
    
    Args:
        query: 搜索查询词
        
    Returns:
        dict: 搜索结果，包含 results 和 related_searches
    """
    # 确保环境变量已加载
    api_key = get_api_key()
    api_host = get_api_host()
    
    # 设置环境变量
    env = {
        **subprocess.os.environ,
        'MINIMAX_API_KEY': api_key,
        'MINIMAX_API_HOST': api_host,
    }
    
    # 通过 mcporter-safe 调用 MiniMax MCP 工具（自动从凭据文件读取 API Key）
    cmd = [
        'mcporter-safe', 'call',
        'MiniMax.web_search',
        '--args', json.dumps({'query': query})
    ]
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60,
            env=env,
            cwd=str(Path.home() / '.mcporter')
        )
        
        if result.returncode != 0:
            error_msg = result.stderr or result.stdout
            # 检查是否是连接错误
            if 'offline' in error_msg.lower() or 'unable to reach' in error_msg.lower():
                raise ConnectionError(
                    f"MiniMax MCP 服务离线或无法连接。\n"
                    f"错误详情: {error_msg}\n"
                    f"请检查：\n"
                    f"1. mcporter 配置是否正确: mcporter config list\n"
                    f"2. MiniMax MCP 是否在线: mcporter list\n"
                    f"3. API Key 是否有效: {masked_key(api_key)}"
                )
            raise RuntimeError(f"MCP 调用失败: {error_msg}")
        
        # 解析输出
        output = result.stdout.strip()
        if output:
            try:
                data = json.loads(output)
                # 统一返回格式：适配 MiniMax API 的 organic 字段
                if 'organic' in data:
                    return {
                        'results': data['organic'],
                        'related_searches': data.get('related_searches', [])
                    }
                return data
            except json.JSONDecodeError:
                return {"raw_output": output}
        
        return {"results": [], "message": "未获取到搜索结果"}
        
    except subprocess.TimeoutExpired:
        raise TimeoutError("搜索请求超时（60秒）")
    except FileNotFoundError:
        raise RuntimeError(
            "未找到 mcporter 命令。\n"
            "请确保已安装 mcporter: npm install -g mcporter"
        )


def web_search(query: str, use_mcp: bool = True) -> dict:
    """
    MiniMax 网络搜索
    
    根据搜索查询词进行网络搜索，返回搜索结果和相关搜索建议。
    
    Args:
        query (str): 搜索查询词
        use_mcp (bool): 是否使用 MCP 调用（默认 True），False 时使用 HTTP API
        
    Returns:
        dict: 搜索结果，格式如下：
        {
            "results": [
                {
                    "title": "结果标题",
                    "url": "https://example.com",
                    "snippet": "结果摘要"
                },
                ...
            ],
            "related_searches": ["相关搜索词1", "相关搜索词2"]
        }
        
    Raises:
        ValueError: 当 query 为空时
        ConnectionError: 当 MCP 服务不可用时
        TimeoutError: 当请求超时时
        RuntimeError: 当发生其他错误时
    """
    if not query or not query.strip():
        raise ValueError("搜索查询词不能为空")
    
    query = query.strip()
    
    print(f"[MiniMax WebSearch] 搜索: {query}")
    print(f"[MiniMax WebSearch] API Key: {masked_key()}")
    
    if use_mcp:
        try:
            result = search_via_mcp(query)
            print(f"[MiniMax WebSearch] 获取到 {len(result.get('results', []))} 条结果")
            return result
        except (ConnectionError, TimeoutError, RuntimeError) as e:
            print(f"[MiniMax WebSearch] MCP 调用失败: {e}")
            print("[MiniMax WebSearch] 尝试使用备用方案...")
            # 这里可以添加备用方案，如使用其他搜索 API
            raise NotImplementedError(
                "MiniMax Token Plan MCP 服务暂时不可用。\n"
                "当前支持的调用方式：\n"
                "1. MiniMax MCP (mcporter call MiniMax.web_search)\n"
                "2. HTTP API (即将支持)\n\n"
                "请检查 mcporter 配置或联系 SysOps 助手。"
            )
    else:
        raise NotImplementedError("HTTP API 调用方式即将支持")


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description="MiniMax 网络搜索工具")
    parser.add_argument('query', nargs='?', help='搜索查询词')
    parser.add_argument('--json', action='store_true', help='输出 JSON 格式')
    
    args = parser.parse_args()
    
    if not args.query:
        parser.print_help()
        sys.exit(1)
    
    try:
        result = web_search(args.query)
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print("\n搜索结果:")
            print("-" * 60)
            for i, item in enumerate(result.get('results', []), 1):
                print(f"{i}. {item.get('title', '无标题')}")
                print(f"   URL: {item.get('url', '无链接')}")
                print(f"   {item.get('snippet', '无摘要')}")
                print()
            
            related = result.get('related_searches', [])
            if related:
                print("相关搜索:", ", ".join(related))
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
