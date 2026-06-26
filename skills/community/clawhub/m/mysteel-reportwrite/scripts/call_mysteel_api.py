#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
钢联研报API调用脚本（Python版本）

功能：
- 从references/api_key.md文件读取API密钥
- 调用钢联研报梗概生成接口（响应式）
- 处理响应式回答，提取梗概内容
- 返回JSON格式的结果
"""

import os
import sys
import io
import json
import time
import argparse
import requests

# 强制使用UTF-8输出，解决中文乱码问题
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


def read_api_key():
    """
    从references/api_key.md文件读取API密钥
    
    文件格式：
    第一行：注释说明
    第二行：api_key值（无多余空行）
    
    Returns:
        str: API密钥，如果文件不存在或密钥无效则返回空字符串
    """
    # 获取脚本所在目录的父目录（Skill根目录）
    script_dir = os.path.dirname(os.path.abspath(__file__))
    skill_root = os.path.dirname(script_dir)
    
    # API密钥文件路径
    api_key_file = os.path.join(skill_root, 'references', 'api_key.md')
    
    # 检查文件是否存在
    if not os.path.exists(api_key_file):
        return ''
    
    try:
        with open(api_key_file, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
        
        # 文件至少需要2行（注释行+密钥行）
        if len(lines) < 2:
            return ''
        
        # 第二行为api_key
        api_key = lines[1]
        
        # 检查是否为占位符
        if api_key == 'YOUR_API_KEY_HERE' or not api_key:
            return ''
        
        return api_key
    except Exception as e:
        print(f"读取API密钥文件失败: {e}", file=sys.stderr)
        return ''


def is_token_invalid_error(data):
    """
    检查数据是否为Token校验失败错误
    
    Args:
        data: 解析后的JSON数据
    
    Returns:
        bool: 是否为Token校验失败
    """
    if not data or not isinstance(data, dict):
        return False
    
    # 检查code和message
    code = str(data.get('code', ''))
    message = data.get('message', '')
    
    return code == '400' and 'Token校验失败' in message


def is_retryable_error(data):
    """
    检查数据是否为可重试错误（5XX或非2XX）
    
    Args:
        data: 解析后的JSON数据
    
    Returns:
        bool: 是否为可重试错误
    """
    if not data or not isinstance(data, dict):
        return False
    
    code = str(data.get('code', ''))
    
    # 5XX错误或非2XX错误（排除400 Token错误）
    if code.startswith('5'):
        return True
    
    if code.startswith('4') and code != '400':
        return True
    
    return False


def call_mysteel_api(query, api_key):
    """
    调用钢联研报API生成研报梗概
    
    Args:
        query: 研报撰写目标
        api_key: API密钥
    
    Returns:
        dict: 包含研报梗概的字典
    """
    # 1. 构建请求
    url = 'https://mcp.mysteel.com/mcp/info/chat-robot/rag/answer'
    headers = {
        'Content-Type': 'application/json',
        'token': api_key
    }
    payload = {
        'query': query
    }
    
    try:
        # 2. 发送请求（超时2分钟）
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=120
        )
        
        # 检查HTTP状态码
        if response.status_code >= 400:
            error_text = response.text
            return {
                'success': False,
                'error': f'HTTP请求失败: 状态码 {response.status_code}, 响应内容: {error_text}',
                'retryable': True
            }
        
        # 3. 处理响应式回答（JSON格式）
        json_data = response.json()
        
        # Token校验失败
        if is_token_invalid_error(json_data):
            return {
                'success': False,
                'error': 'Token校验失败，请更换apikey',
                'error_code': 'token_invalid',
                'api_response': json_data
            }
        
        # 其他错误
        if not json_data.get('success'):
            code = str(json_data.get('code', ''))
            is_retryable = is_retryable_error(json_data)
            
            return {
                'success': False,
                'error': json_data.get('message', 'API返回错误'),
                'error_code': code,
                'retryable': is_retryable,
                'api_response': json_data
            }
        
        # 成功响应，提取梗概内容
        # 根据返回格式，梗概在data字段中
        outline = json_data.get('data', '')
        
        # 如果是嵌套结构，尝试提取
        if isinstance(outline, dict):
            outline = json.dumps(outline, ensure_ascii=False, indent=2)
        
        return {
            'success': True,
            'outline': str(outline),
            'api_response': json_data
        }
        
    except requests.exceptions.Timeout:
        return {
            'success': False,
            'error': '请求超时，研报梗概生成时间过长（超过2分钟）',
            'retryable': True
        }
    except requests.exceptions.RequestException as e:
        return {
            'success': False,
            'error': f'网络请求失败: {str(e)}',
            'retryable': True
        }
    except Exception as e:
        return {
            'success': False,
            'error': f'未知错误: {str(e)}',
            'retryable': False
        }


def main():
    """主函数"""
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='调用钢联研报API生成研报梗概')
    parser.add_argument('--query', required=True, help='研报撰写目标')
    args = parser.parse_args()
    
    query = args.query
    
    # 读取API密钥
    api_key = read_api_key()
    
    if not api_key:
        result = {
            'success': False,
            'error': '缺少API密钥，请检查references/api_key.md文件是否存在，或api_key是否为占位符'
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(1)
    
    # 调用API
    result = call_mysteel_api(query, api_key)
    
    # 检查是否需要重试
    if not result.get('success') and result.get('retryable') and result.get('error_code') != 'token_invalid':
        print(f"[Retry] 首次调用失败，正在重试... 错误: {result.get('error')}", file=sys.stderr)
        
        # 等待1秒后重试
        time.sleep(1)
        
        # 重试一次
        result = call_mysteel_api(query, api_key)
        
        if not result.get('success') and result.get('retryable'):
            print(f"[Retry] 重试仍然失败: {result.get('error')}", file=sys.stderr)
    
    # Token校验失败提示
    if not result.get('success') and result.get('error_code') == 'token_invalid':
        print("[Token Error] Token校验失败，请更换apikey", file=sys.stderr)
    
    # 输出结果（JSON格式）
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    # 根据结果设置退出码
    sys.exit(0 if result.get('success') else 1)


if __name__ == '__main__':
    main()
