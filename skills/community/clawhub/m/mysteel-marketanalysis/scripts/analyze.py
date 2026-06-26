#!/usr/bin/env python3
"""
钢联大宗商品分析接口调用脚本

功能：调用钢联内部分析接口，获取大宗商品市场的专业分析报告
授权方式: 从 references/api_key.md 文件读取 API 密钥
依赖: requests==2.31.0
"""

import os
import sys
import io
import json
import argparse

# 强制使用UTF-8输出，解决中文乱码问题
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

try:
    import requests
except ImportError:
    print("Error: requests library not installed")
    print("Please run: pip install requests==2.31.0")
    sys.exit(1)


def load_api_key():
    """
    从 references/api_key.md 文件读取 API 密钥
    
    文件格式:
    - 第一行: 注释（以 # 开头）
    - 第二行: API 密钥
    
    返回:
        str: API 密钥
    
    异常:
        Exception: 文件不存在、格式错误或密钥为占位符
    """
    # 获取 api_key.md 文件路径（相对于脚本所在目录）
    script_dir = os.path.dirname(os.path.abspath(__file__))
    api_key_file = os.path.join(script_dir, '..', 'references', 'api_key.md')
    
    # 检查文件是否存在
    if not os.path.exists(api_key_file):
        raise Exception(
            'API key config file not found: references/api_key.md\n'
            'Please configure MYSTEEL_CLAW_APIKEY in the file'
        )
    
    # 读取文件内容
    try:
        with open(api_key_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        raise Exception(f'Failed to read API key file: {str(e)}')
    
    # 过滤空行，获取有效行
    lines = [line.strip() for line in content.split('\n') if line.strip()]
    
    # 验证文件格式（至少2行有效内容）
    if len(lines) < 2:
        raise Exception(
            f'API key file format error, requires at least 2 lines\n'
            f'Current valid lines: {len(lines)}'
        )
    
    # 提取第二行作为API密钥
    api_key = lines[1]
    
    # 检查是否为占位符
    if not api_key or api_key == 'YOUR_API_KEY_HERE':
        raise Exception(
            'API key not configured\n'
            'Please replace YOUR_API_KEY_HERE with actual MYSTEEL_CLAW_APIKEY in references/api_key.md'
        )
    
    return api_key


def call_mysteel_analysis_internal(query):
    """
    调用钢联内部分析接口获取市场分析（内部函数）
    
    参数:
        query (str): 分析查询问题（如"上海建筑钢材市场分析"）
    
    返回:
        str: Markdown格式的分析结果
    
    异常:
        Exception: API调用失败或超时
    """
    try:
        api_key = load_api_key()
    except Exception as e:
        raise e
    
    # 构建请求
    url = 'https://mcp.mysteel.com/mcp/info/chat-robot/rag/answer'
    payload = {'query': query}
    headers = {
        'Content-Type': 'application/json',
        'token': api_key
    }
    
    try:
        response = requests.post(
            url,
            json=payload,
            headers=headers,
            timeout=90  # 90秒超时
        )
        
        # 检查HTTP状态码
        if response.status_code >= 400:
            raise Exception(
                f'HTTP request failed: status code {response.status_code}, '
                f'response: {response.text[:200]}'
            )
        
        # 解析响应
        try:
            result = response.json()
        except json.JSONDecodeError as e:
            raise Exception(f'Failed to parse response: {str(e)}')
        
        # 检查业务状态码
        if not result.get('success', False):
            error_msg = result.get('message', 'Unknown error')
            error_code = result.get('code', 'N/A')
            
            # 特殊处理：Token校验失败（code=400）
            if str(error_code) == '400':
                auth_error = Exception(
                    f'Token validation failed: {error_msg}\n'
                    f'Please check if your API key is correct and update it in references/api_key.md'
                )
                auth_error.is_auth_error = True
                raise auth_error
            
            # 其他错误：返回错误信息，包含错误码和消息
            raise Exception(f'Mysteel API error[{error_code}]: {error_msg}')
        
        # 提取分析结果
        analysis_data = result.get('data', '')
        if not analysis_data:
            raise Exception('Return data is empty, please check if the query is valid')
        
        return analysis_data
        
    except requests.exceptions.Timeout:
        raise Exception('Request timeout (90s), please try again later or simplify the query')
    except requests.exceptions.RequestException as e:
        raise Exception(f'API call failed: {str(e)}')


def call_mysteel_analysis(query):
    """
    调用钢联内部分析接口获取市场分析（带重试机制）
    
    参数:
        query (str): 分析查询问题（如"上海建筑钢材市场分析"）
    
    返回:
        str: Markdown格式的分析结果
    
    异常:
        Exception: API调用失败或超时
    """
    try:
        # 第一次尝试
        return call_mysteel_analysis_internal(query)
    except Exception as error:
        # 如果是Token校验失败，直接抛出，不重试
        if getattr(error, 'is_auth_error', False):
            raise error
        
        # 其他错误（如系统内部异常），重试一次
        sys.stderr.write('First attempt failed, retrying...\n')
        try:
            return call_mysteel_analysis_internal(query)
        except Exception as retry_error:
            # 重试也失败了，抛出错误
            raise retry_error


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(description='Mysteel commodity analysis tool')
    parser.add_argument('--query', required=True, help='Analysis query question')
    args = parser.parse_args()
    
    # 调用分析接口
    try:
        result = call_mysteel_analysis(args.query)
        print(result)
    except Exception as error:
        error_msg = str(error)
        if error_msg.startswith('API key') or error_msg.startswith('Token validation failed'):
            sys.stderr.write(f'Configuration Error: {error_msg}\n')
        else:
            sys.stderr.write(f'Analysis Failed: {error_msg}\n')
        sys.exit(1)


if __name__ == '__main__':
    main()
