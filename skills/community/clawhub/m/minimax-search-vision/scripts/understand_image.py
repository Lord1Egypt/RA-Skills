"""
MiniMax 图片理解工具

通过 MiniMax Token Plan MCP 提供的 understand_image 工具进行图片理解

注意：此工具依赖于 MiniMax Token Plan MCP 服务。
支持格式：JPEG, PNG, GIF, WebP (最大 20MB)
"""

import json
import subprocess
import sys
from pathlib import Path
from typing import Union

try:
    from .config import get_api_key, masked_key, get_api_host
except ImportError:
    from config import get_api_key, masked_key, get_api_host


def validate_image_url(image_url: str) -> bool:
    """
    验证图片 URL 格式
    
    Args:
        image_url: 图片 URL 或本地路径
        
    Returns:
        bool: 是否有效
    """
    if not image_url:
        return False
    
    # 本地文件
    if Path(image_url).is_file():
        # 检查文件大小（最大 20MB）
        size_mb = Path(image_url).stat().st_size / (1024 * 1024)
        if size_mb > 20:
            raise ValueError(f"图片文件过大: {size_mb:.1f}MB（最大 20MB）")
        return True
    
    # HTTP/HTTPS URL
    if image_url.startswith(('http://', 'https://')):
        return True
    
    return False


def understand_via_mcp(prompt: str, image_url: str) -> dict:
    """
    通过 mcporter 调用 MiniMax MCP 的 understand_image 工具
    
    Args:
        prompt: 对图片的提问或分析要求
        image_url: 图片来源（HTTP/HTTPS URL 或本地文件路径）
        
    Returns:
        dict: 图片理解结果
    """
    # 验证图片
    if not validate_image_url(image_url):
        raise ValueError(
            f"无效的图片地址: {image_url}\n"
            f"支持的格式：\n"
            f"  - HTTP/HTTPS URL: https://example.com/image.jpg\n"
            f"  - 本地文件: /path/to/image.jpg（最大 20MB）"
        )
    
    # 确保环境变量已加载
    api_key = get_api_key()
    api_host = get_api_host()
    
    # 设置环境变量
    env = {
        **subprocess.os.environ,
        'MINIMAX_API_KEY': api_key,
        'MINIMAX_API_HOST': api_host,
    }
    
    # 构建请求参数
    args = {
        'prompt': prompt,
        'image_url': image_url
    }
    
    # 通过 mcporter-safe 调用 MiniMax MCP 工具（自动从凭据文件读取 API Key）
    cmd = [
        'mcporter-safe', 'call',
        'MiniMax.understand_image',
        '--args', json.dumps(args)
    ]
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120,  # 图片理解可能需要更长时间
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
                return json.loads(output)
            except json.JSONDecodeError:
                return {"raw_output": output}
        
        return {"result": "未获取到分析结果"}
        
    except subprocess.TimeoutExpired:
        raise TimeoutError("图片理解请求超时（120秒），图片可能太大")
    except FileNotFoundError:
        raise RuntimeError(
            "未找到 mcporter 命令。\n"
            "请确保已安装 mcporter: npm install -g mcporter"
        )


def understand_image(
    prompt: str,
    image_url: str,
    use_mcp: bool = True
) -> dict:
    """
    MiniMax 图片理解
    
    对图片进行理解和分析，支持多种图片输入方式。
    
    Args:
        prompt (str): 对图片的提问或分析要求
        image_url (str): 图片来源，支持：
            - HTTP/HTTPS URL: https://example.com/image.jpg
            - 本地文件路径: /path/to/image.jpg
        use_mcp (bool): 是否使用 MCP 调用（默认 True）
        
    Returns:
        dict: 图片分析结果
        
    Raises:
        ValueError: 当参数无效时
        ConnectionError: 当 MCP 服务不可用时
        TimeoutError: 当请求超时时
        RuntimeError: 当发生其他错误时
    """
    if not prompt or not prompt.strip():
        raise ValueError("图片分析提示词不能为空")
    
    if not image_url or not image_url.strip():
        raise ValueError("图片地址不能为空")
    
    prompt = prompt.strip()
    image_url = image_url.strip()
    
    print(f"[MiniMax ImageUnderstand] 分析图片: {image_url}")
    print(f"[MiniMax ImageUnderstand] 提示词: {prompt}")
    print(f"[MiniMax ImageUnderstand] API Key: {masked_key()}")
    
    # 验证图片
    try:
        validate_image_url(image_url)
    except ValueError as e:
        raise
    
    if use_mcp:
        try:
            result = understand_via_mcp(prompt, image_url)
            print(f"[MiniMax ImageUnderstand] 分析完成")
            return result
        except (ConnectionError, TimeoutError, RuntimeError) as e:
            print(f"[MiniMax ImageUnderstand] MCP 调用失败: {e}")
            print("[MiniMax ImageUnderstand] 尝试使用备用方案...")
            raise NotImplementedError(
                "MiniMax Token Plan MCP 服务暂时不可用。\n"
                "当前支持的调用方式：\n"
                "1. MiniMax MCP (mcporter call MiniMax.understand_image)\n"
                "2. HTTP API (即将支持)\n\n"
                "请检查 mcporter 配置或联系 SysOps 助手。"
            )
    else:
        raise NotImplementedError("HTTP API 调用方式即将支持")


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description="MiniMax 图片理解工具")
    parser.add_argument('prompt', nargs='?', help='对图片的提问或分析要求')
    parser.add_argument('image_url', nargs='?', help='图片地址 (URL 或本地路径)')
    parser.add_argument('--json', action='store_true', help='输出 JSON 格式')
    
    args = parser.parse_args()
    
    if not args.prompt or not args.image_url:
        parser.print_help()
        print("\n示例:")
        print("  python understand_image.py '这是什么' 'https://example.com/image.jpg'")
        print("  python understand_image.py '描述这张图' '/path/to/image.png'")
        sys.exit(1)
    
    try:
        result = understand_image(args.prompt, args.image_url)
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print("\n图片分析结果:")
            print("-" * 60)
            print(result.get('result', result.get('raw_output', '无结果')))
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
