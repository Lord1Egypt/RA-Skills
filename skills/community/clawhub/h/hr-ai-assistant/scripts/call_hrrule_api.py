#!/usr/bin/env python3
"""
HRrule AI WebSocket API 调用脚本
用于流式获取 HR 相关内容
支持自动下载附件功能
"""

import sys
import json
import asyncio
import socketio
import os
from urllib.parse import urlparse, urlunparse, urlencode, parse_qsl
from typing import Optional, Callable

# 导入文件下载辅助模块
from download_helper import FileDownloadHelper, generate_download_links_plain, generate_download_links_markdown


# 固定的 WebSocket URL
WS_URL = "wss://ai.hrrule.com"

# 默认模型
DEFAULT_MODEL = "deepseek-ai/DeepSeek-R1"


def get_api_key() -> str:
    """
    获取 API Key

    优先级:
    1. 环境变量 HRRULE_API_KEY
    2. 配置文件 config.json
    3. 提示用户申请

    Returns:
        API Key 字符串,如果未找到则返回空字符串
    """
    # 1. 尝试从环境变量获取
    api_key = os.environ.get('HRRULE_API_KEY')
    if api_key and api_key.strip():
        return api_key.strip()

    # 2. 尝试从配置文件获取
    skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_file = os.path.join(skill_dir, 'config.json')

    if os.path.exists(config_file):
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                api_key = config.get('api_key', '').strip()
                if api_key:
                    return api_key
        except Exception as e:
            print(f"警告: 读取配置文件失败: {e}")

    # 3. 未找到 API Key,返回空字符串
    return ""


def check_api_key(api_key: str) -> bool:
    """
    检查 API Key 是否有效

    Args:
        api_key: API Key 字符串

    Returns:
        True 如果 API Key 不为空且不是占位符
    """
    if not api_key or not api_key.strip():
        return False

    # 检查是否是示例占位符
    placeholders = [
        'your-api-key-here',
        'your-api-key',
        'your-actual-api-key',
        'app-xxx'
    ]

    return not any(api_key.lower().startswith(p.lower()) for p in placeholders)


def print_api_key_help():
    """打印 API Key 申请帮助信息"""
    print("\n" + "="*80)
    print("❌ 未找到有效的 API Key")
    print("="*80)
    print("\n📝 请按照以下步骤免费申请 API Key:\n")
    print("1. 访问: https://ai.hrrule.com/")
    print("2. 注册/登录账号")
    print("3. 在个人中心申请 API Key")
    print("4. 免费,申请后即可使用\n")
    print("📌 配置方式(任选一种):\n")
    print("  方式1: 设置环境变量")
    print("    export HRRULE_API_KEY='your-api-key'\n")
    print("  方式2: 编辑配置文件")
    print("    文件位置: {}/config.json".format(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    print("    内容: {\"api_key\": \"your-api-key\"}\n")
    print("="*80 + "\n")


async def call_hrrule_api(
    api_key: str,
    content: str,
    tag_id: int,
    rt: str,
    ws_url: str = WS_URL,
    model: str = DEFAULT_MODEL,
    on_chunk: Optional[Callable[[str], None]] = None,
    on_complete: Optional[Callable[[], None]] = None,
    on_error: Optional[Callable[[str], None]] = None,
    verbose: bool = False
) -> dict:
    """
    调用 HRrule AI WebSocket API

    Args:
        api_key: API 密钥
        content: 用户问题或需求
        tag_id: 内容类型 ID
        rt: 资源类型
        ws_url: WebSocket 地址(已固定为 wss://ai.hrrule.com)
        model: 模型名称
        on_chunk: 收到内容块时的回调函数
        on_complete: 完成时的回调函数
        on_error: 错误时的回调函数
        verbose: 是否显示详细日志

    Returns:
        dict: {
            'success': bool,  # 是否成功调用 API
            'response': str,  # 响应内容
            'fallback': bool,  # 是否使用了 fallback（通用大模型）
            'error': str  # 错误信息（如果有）
        }
    """
    # 检查 API Key
    if not check_api_key(api_key):
        # 显示友好提示
        print_api_key_help()

        # 返回使用 fallback 的信号
        return {
            'success': False,
            'response': '',
            'fallback': True,
            'error': '未配置 API Key，请访问 https://ai.hrrule.com/ 免费申请'
        }

    # 生成页面会话 ID
    page_session = f"session_{asyncio.get_event_loop().time()}_{id(content)}"

    # 存储完整响应
    full_response = ""
    connected = False
    completed = False

    # 构建 WebSocket URL (在 URL 中添加 ApiKey 查询参数)
    parsed = urlparse(ws_url)
    query_params = parse_qsl(parsed.query)
    query_params.append(('ApiKey', api_key))
    full_ws_url = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path,
        parsed.params,
        urlencode(query_params),
        parsed.fragment
    ))

    if verbose:
        print(f"[WebSocket URL] {full_ws_url}")

    # 创建 Socket.IO 客户端（使用安全的 SSL 验证）
    import ssl
    ssl_context = ssl.create_default_context()
    sio = socketio.AsyncClient(ssl=ssl_context, reconnection=False)

    @sio.on('connect')
    async def on_connect():
        nonlocal connected
        connected = True
        if verbose:
            print(f"[连接成功] Socket ID: {sio.sid}")

        # 发送消息
        message_data = {
            "content": content,
            "page_session": page_session,
            "model": model,
            "tag_id": tag_id,
            "rt": rt,
            "ua": "web",
            "deep": 1,
            "web": 1
        }

        if verbose:
            print(f"[发送消息] Tag ID: {tag_id}, RT: {rt}")
            print(f"[发送消息] Content: {content[:100]}...")

        await sio.emit('open_chat_completion', message_data)

    @sio.on('start')
    async def on_start_event(data):
        if verbose:
            print(f"[开始] history_id: {data.get('history_id')}")

    @sio.on('chunk')
    async def on_chunk_event(data):
        nonlocal full_response

        try:
            # 解析数据
            if isinstance(data, str):
                chunk_data = json.loads(data)
            elif isinstance(data, dict) and 'data' in data:
                chunk_data = json.loads(data['data'])
            else:
                chunk_data = data

            # 提取内容
            content = chunk_data.get('choices', [{}])[0].get('delta', {}).get('content', '')
            thinking = chunk_data.get('choices', [{}])[0].get('delta', {}).get('reasoning_content', '')

            if thinking and verbose:
                print(f"[思考] {thinking[:100]}...")

            if content:
                full_response += content
                if on_chunk:
                    on_chunk(content)
                if verbose:
                    print(f"[内容] {content[:50]}...")

        except Exception as e:
            if verbose:
                print(f"[解析错误] {e}")

    @sio.on('complete')
    async def on_complete_event(data):
        nonlocal completed
        completed = True
        if verbose:
            print(f"[完成] 响应已完成")
        if on_complete:
            on_complete()

    @sio.on('error')
    async def on_error_event(data):
        error_msg = data.get('msg', 'Unknown error') if isinstance(data, dict) else str(data)
        if verbose:
            print(f"[错误] {error_msg}")
        if on_error:
            on_error(error_msg)

    @sio.on('disconnect')
    async def on_disconnect():
        nonlocal connected
        connected = False
        if verbose and not completed:
            print(f"[断开连接]")

    @sio.on('connect_error')
    async def on_connect_error(error):
        nonlocal connected
        connected = False
        error_msg = str(error)
        if verbose:
            print(f"[连接错误] {error_msg}")
        if on_error:
            on_error(error_msg)

    try:
        # 连接服务器
        if verbose:
            print(f"[连接中] {full_ws_url}")

        await sio.connect(full_ws_url, transports=['websocket', 'polling'])

        # 等待完成或超时
        timeout = 120  # 120秒超时
        start_time = asyncio.get_event_loop().time()

        while connected and not completed:
            await asyncio.sleep(0.1)
            elapsed = asyncio.get_event_loop().time() - start_time
            if elapsed > timeout:
                if verbose:
                    print(f"[超时] 等待 {timeout} 秒后超时")
                break

    except Exception as e:
        error_msg = str(e)
        if verbose:
            print(f"[异常] {error_msg}")
        if on_error:
            on_error(error_msg)
    finally:
        # 断开连接
        if connected:
            await sio.disconnect()

    # 返回成功结果
    result = {
        'success': True,
        'response': full_response,
        'fallback': False,
        'error': None,
        'attachments': []
    }

    # 检测并处理附件
    file_ids = FileDownloadHelper(api_key).extract_file_ids(full_response)
    if file_ids:
        print(f"\n[附件] 检测到 {len(file_ids)} 个附件")

        # 使用 Markdown 格式生成下载链接（传入 API Key 以获取真实下载地址）
        result['response'] = generate_download_links_markdown(full_response, api_key)

        # 可选：自动下载附件
        if os.getenv('HRRULE_AUTO_DOWNLOAD', 'false').lower() == 'true':
            downloader = FileDownloadHelper(
                api_key,
                output_dir=os.path.join(os.path.expanduser('~'), '.workbuddy', 'skills', 'hr-ai-assistant', 'downloads')
            )
            downloaded_files = downloader.process_all_rulefiles(full_response)
            result['attachments'] = downloaded_files

    return result


def print_streaming(text: str, output_dir: str = None, use_markdown: bool = True, api_key: str = None):
    """打印流式内容，并检测和替换 <rulefile> 标签

    Args:
        text: 流式输出文本
        output_dir: 下载文件保存目录
        use_markdown: 是否使用 Markdown 格式（默认 True，更适合 WorkBuddy）
        api_key: API Key（用于获取真实下载地址）
    """
    if output_dir and text and '<rulefile>' in text:
        # 检测是否包含 <rulefile> 标签，只在检测到时才处理
        if use_markdown:
            # 使用 Markdown 格式（WorkBuddy 支持 Markdown 链接）
            text = generate_download_links_markdown(text, api_key)
        else:
            # 使用纯文本格式
            text = generate_download_links_plain(text, output_dir)
    print(text, end='', flush=True)


def main():
    """命令行主函数"""
    import argparse

    # 设置标准输出编码为 UTF-8
    import sys
    if sys.platform == 'win32':
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer)

    parser = argparse.ArgumentParser(description='HRrule AI WebSocket API 客户端')
    parser.add_argument('--api-key', help='API 密钥 (可选,不填则使用配置或环境变量)')
    parser.add_argument('--content', required=True, help='用户问题或需求')
    parser.add_argument('--tag-id', type=int, required=True, help='内容类型 ID')
    parser.add_argument('--rt', required=True, help='资源类型')
    parser.add_argument('--ws-url', default=WS_URL, help='WebSocket 地址')
    parser.add_argument('--model', default=DEFAULT_MODEL, help='模型名称')
    parser.add_argument('--verbose', action='store_true', help='显示详细日志')
    parser.add_argument('--auto-download', action='store_true', help='自动下载附件')

    args = parser.parse_args()

    # 获取 API Key (优先使用命令行参数)
    api_key = args.api_key if args.api_key else get_api_key()

    # 隐藏命令行中的 API Key（防止通过 ps 命令泄露）
    if args.api_key:
        try:
            # 清除命令行参数中的敏感信息
            sys.argv = [arg for arg in sys.argv if not arg.startswith('--api-key')]
            sys.argv.append('--api-key')
            sys.argv.append('***HIDDEN***')
        except:
            pass  # 如果清除失败，也不影响正常执行

    # 设置自动下载标志
    if args.auto_download:
        os.environ['HRRULE_AUTO_DOWNLOAD'] = 'true'

    # 设置下载目录
    output_dir = os.path.join(os.path.expanduser('~'), '.workbuddy', 'skills', 'hr-ai-assistant', 'downloads')

    try:
        response = asyncio.run(call_hrrule_api(
            api_key=api_key,
            content=args.content,
            tag_id=args.tag_id,
            rt=args.rt,
            ws_url=args.ws_url,
            model=args.model,
            on_chunk=lambda text: print_streaming(text, output_dir, use_markdown=True, api_key=api_key),
            verbose=args.verbose
        ))

        # 打印完整响应（确保包含 Markdown 格式的下载链接）
        print("\n" + "="*80)
        if response.get('success'):
            final_response = response.get('response', '')
            # 如果响应中包含 <rulefile> 标签，确保转换为 Markdown 格式
            if '<rulefile>' in final_response:
                final_response = generate_download_links_markdown(final_response, api_key)

            print(f"完整响应 ({len(final_response)} 字符):")
            print("="*80)
            print(final_response)

            # 如果有附件，显示附件信息
            if response.get('attachments'):
                print("\n" + "="*80)
                print(f"已下载附件 ({len(response.get('attachments', []))} 个):")
                print("="*80)
                for idx, filepath in enumerate(response.get('attachments', []), 1):
                    print(f"{idx}. {filepath}")

    except ValueError as e:
        print(f"\n错误: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\n异常: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
