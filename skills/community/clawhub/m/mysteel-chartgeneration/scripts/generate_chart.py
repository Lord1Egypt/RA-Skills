#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI图表生成API调用脚本

功能：
- 调用AI图表生成API生成ECharts配置
- 自动生成唯一requestId
- 将结果保存为JSON文件
- 自动从task描述生成图表标题
- 仅支持同步模式（asyncEnable固定为false）

授权方式: ApiKey（从api_key.md文件读取）
"""

import os
import sys
import json
import uuid
import argparse
import requests
from pathlib import Path


def load_api_key():
    """
    从项目的references目录下读取api_key.md文件
    
    Returns:
        str: API密钥
    
    Raises:
        Exception: 文件不存在或格式错误
    """
    script_dir = Path(__file__).parent.parent
    api_key_file = script_dir / 'references' / 'api_key.md'
    
    if not api_key_file.exists():
        raise Exception(
            f"api_key.md 文件不存在。请先在项目的references目录下创建该文件并填入API密钥。\n"
            f"文件路径：{api_key_file}\n"
            f"文件格式：api_key: 你的密钥"
        )
    
    content = api_key_file.read_text(encoding='utf-8').strip()
    
    if not content:
        raise Exception(f"api_key.md 文件为空，请填入API密钥。文件路径：{api_key_file}")
    
    if content.startswith('api_key:'):
        api_key = content.split(':', 1)[1].strip()
    else:
        api_key = content
    
    if not api_key:
        raise Exception(f"未能从api_key.md文件中解析出有效的API密钥。文件路径：{api_key_file}")
    
    return api_key


def generate_request_id():
    """
    生成唯一的请求标识符
    
    Returns:
        str: 唯一的requestId
    """
    unique_id = str(uuid.uuid4()).replace('-', '')
    return f"req-{unique_id[:16]}"


def generate_title_from_task(task):
    """
    从任务描述中生成图表标题
    
    Args:
        task (str): 任务描述
    
    Returns:
        str: 生成的图表标题
    """
    task_clean = task.strip()
    
    prefixes_to_remove = [
        '生成一个', '生成', '画一个', '画个', '创建一个', '创建',
        '帮我生成', '帮我画', '请生成', '请画', '展示',
        '显示', '呈现', '可视化'
    ]
    
    for prefix in prefixes_to_remove:
        if task_clean.startswith(prefix):
            task_clean = task_clean[len(prefix):].strip()
            break
    
    # 移除数据部分
    if '，数据为：' in task_clean:
        task_clean = task_clean.split('，数据为：')[0].strip()
    elif ',数据为：' in task_clean:
        task_clean = task_clean.split(',数据为：')[0].strip()
    elif '数据为：' in task_clean:
        task_clean = task_clean.split('数据为：')[0].strip()
    
    # 移除图表类型后缀
    suffixes_to_remove = [
        '图表', '图', '走势图', '趋势图', '折线图', '柱状图',
        '饼图', '对比图', '结构图', '关系图'
    ]
    
    for suffix in suffixes_to_remove:
        if task_clean.endswith(suffix):
            task_clean = task_clean[:-len(suffix)].strip()
            break
    
    if not task_clean or len(task_clean) < 2:
        return 'AI生成图表'
    
    return task_clean


def generate_chart(task, mode='FREEDOM', data=None, type_param=None,
                   data_example=None, data_description=None, option=None,
                   robust_mode=False, session_id=None, output_dir='./output'):
    """
    调用AI图表生成API（同步模式）
    
    Args:
        task (str): 任务描述
        mode (str): 生成模式
        data (str): JSON字符串形式的数据
        type_param (str): 图表类型
        data_example (str): JSON字符串形式的数据示例
        data_description (str): 数据描述
        option (str): JSON字符串形式的图表配置
        robust_mode (bool): 是否开启健壮模式
        session_id (str): 会话标识符
        output_dir (str): 输出目录
    
    Returns:
        dict: API响应结果
    
    Raises:
        Exception: API调用失败或解析错误
    """
    api_key = load_api_key()
    request_id = generate_request_id()
    
    payload = {
        'requestId': request_id,
        'task': task,
        'mode': mode,
        'asyncEnable': False
    }
    
    if data is not None:
        payload['data'] = json.loads(data)
    if type_param is not None:
        payload['type'] = type_param
    if data_example is not None:
        payload['dataExample'] = json.loads(data_example)
    if data_description is not None:
        payload['dataDescription'] = data_description
    if option is not None:
        payload['option'] = json.loads(option)
    if robust_mode:
        payload['robustMode'] = True
    if session_id is not None:
        payload['sessionId'] = session_id
    
    url = 'https://mcp.mysteel.com/mcp/info/genie-tool/v1/tool/ai-chart'
    
    print(f"[INFO] 调用AI图表生成API...")
    print(f"[INFO] requestId: {request_id}")
    print(f"[INFO] mode: {mode}")
    
    headers = {
        'Content-Type': 'application/json',
        'token': api_key
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        
        if response.status_code >= 400:
            raise Exception(f"HTTP请求失败: 状态码 {response.status_code}, 响应内容: {response.text}")
        
        result = response.json()
        code = result.get('code')
        
        if str(code) != '200':
            error_msg = result.get('message', '未知错误')
            raise Exception(f"API错误: {error_msg}")
        
        print(f"[INFO] API调用成功")
        
        data_result = result.get('data', {})
        option_data = data_result.get('option')
        option_url = data_result.get('optionUrl')
        preview_url = data_result.get('previewUrl')
        
        print(f"[INFO] optionUrl: {option_url}")
        print(f"[INFO] previewUrl: {preview_url}")
        
        # 创建输出目录
        output_path = Path(output_dir).resolve()
        output_path.mkdir(parents=True, exist_ok=True)
        
        # 保存option文件
        option_file = output_path / f"{request_id}_option.json"
        option_file.write_text(json.dumps(option_data, indent=2, ensure_ascii=False), encoding='utf-8')
        
        # 生成标题并保存meta文件
        chart_title = generate_title_from_task(task)
        meta_file = output_path / f"{request_id}_meta.json"
        meta_info = {
            'requestId': request_id,
            'task': task,
            'title': chart_title
        }
        meta_file.write_text(json.dumps(meta_info, indent=2, ensure_ascii=False), encoding='utf-8')
        
        print(f"[INFO] 图表配置已保存到: {option_file}")
        print(f"[INFO] 图表标题: {chart_title}")
        
        return result
        
    except requests.exceptions.RequestException as e:
        raise Exception(f"API调用失败: {str(e)}")
    except json.JSONDecodeError as e:
        raise Exception(f"解析响应失败: {str(e)}")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='AI图表生成API调用脚本')
    parser.add_argument('--task', required=True, help='任务描述')
    parser.add_argument('--mode', default='FREEDOM', help='生成模式')
    parser.add_argument('--session-id', help='会话标识符')
    parser.add_argument('--output-dir', default='./output', help='输出目录')
    parser.add_argument('--data', help='JSON字符串形式的数据')
    parser.add_argument('--type', dest='type_param', help='图表类型')
    parser.add_argument('--data-example', help='JSON字符串形式的数据示例')
    parser.add_argument('--data-description', help='数据描述')
    parser.add_argument('--option', help='JSON字符串形式的图表配置')
    parser.add_argument('--robust-mode', action='store_true', help='是否开启健壮模式')
    
    args = parser.parse_args()
    
    try:
        result = generate_chart(
            task=args.task,
            mode=args.mode,
            data=args.data,
            type_param=args.type_param,
            data_example=args.data_example,
            data_description=args.data_description,
            option=args.option,
            robust_mode=args.robust_mode,
            session_id=getattr(args, 'session_id', None),
            output_dir=args.output_dir
        )
        print('[SUCCESS] 图表生成成功')
        request_id = result['data'].get('requestId', '')
        if request_id:
            print(f"图表配置文件: {args.output_dir}/{request_id}_option.json")
    except Exception as e:
        print(f"[ERROR] {e}")
        if 'api_key.md' in str(e):
            print('[提示] 请创建 api_key.md 文件，内容格式：api_key: 你的密钥')
        sys.exit(1)


if __name__ == '__main__':
    main()
