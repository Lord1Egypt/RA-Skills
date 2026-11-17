#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LipVoice TTS API 客户端
"""
import os
import sys
import json
import time
import argparse
import urllib.request
import urllib.error

# 配置默认编码，解决Windows GBK编码问题
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# API Key 优先级: 参数 > 环境变量 LIPVOICE_API_KEY > 脚本内配置
API_KEY = os.environ.get("LIPVOICE_API_KEY", "")

BASE_URL = "https://openapi.lipvoice.cn/api/third"


def make_request(method, path, data=None, files=None):
    """发送HTTP请求"""
    url = BASE_URL + path
    headers = {'sign': API_KEY}
    
    if not API_KEY:
        return {"code": -1, "msg": "未配置API Key，请设置环境变量 LIPVOICE_API_KEY 或传入 --api-key 参数"}
    
    if files:
        # multipart/form-data
        boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'
        body = b''
        
        # 添加表单字段
        if data:
            for key, value in data.items():
                body += f'--{boundary}\r\n'.encode()
                body += f'Content-Disposition: form-data; name="{key}"\r\n\r\n'.encode()
                body += f'{value}\r\n'.encode()
        
        # 添加文件
        for key, value in files.items():
            if isinstance(value, tuple) and len(value) == 3:
                filename, file_content, content_type = value
                body += f'--{boundary}\r\n'.encode()
                body += f'Content-Disposition: form-data; name="{key}"; filename="{filename}"\r\n'.encode()
                body += f'Content-Type: {content_type}\r\n\r\n'.encode()
                body += file_content + b'\r\n'
            else:
                body += f'--{boundary}\r\n'.encode()
                body += f'Content-Disposition: form-data; name="{key}"\r\n\r\n'.encode()
                body += f'{value}\r\n'.encode()
        
        body += f'--{boundary}--\r\n'.encode()
        headers['Content-Type'] = f'multipart/form-data; boundary={boundary}'
        req = urllib.request.Request(url, data=body, headers=headers, method=method)
    else:
        req_data = json.dumps(data).encode() if data else None
        headers['Content-Type'] = 'application/json'
        req = urllib.request.Request(url, data=req_data, headers=headers, method=method)
    
    try:
        with urllib.request.urlopen(req, timeout=120) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        return json.loads(e.read().decode())
    except Exception as e:
        return {"code": -1, "msg": str(e)}


def upload_model(audio_file, name, describe=""):
    """上传音频创建模型"""
    if not os.path.exists(audio_file):
        return {"code": -1, "msg": f"文件不存在: {audio_file}"}
    
    ext = os.path.splitext(audio_file)[1].lower()
    if ext not in ['.mp3', '.wav', '.m4a']:
        return {"code": -1, "msg": "仅支持mp3/wav/m4a格式"}
    
    with open(audio_file, 'rb') as f:
        file_content = f.read()
    files = {'file': (os.path.basename(audio_file), file_content, f'audio/{ext[1:]}')}
    data = {'name': name, 'describe': describe}
    result = make_request('POST', '/reference/upload', data, files)
    
    if result.get('code') == 0:
        print(f"✅ 模型创建成功!")
        print(f"   名称: {result['data']['name']}")
        print(f"   ID: {result['data']['audioId']}")
    else:
        print(f"❌ 创建失败: {result.get('msg')}")
    
    return result


def list_models():
    """列出所有模型"""
    result = make_request('GET', '/reference/list')
    
    if result.get('code') == 0:
        models = result['data']['list']
        total = result['data']['total']
        print(f"\n共{total}个模型：\n")
        for i, m in enumerate(models, 1):
            desc = f" - {m['describe']}" if m.get('describe') else ""
            print(f"  {i}. {m['name']}{desc}")
            print(f"     ID: {m['audioId']}")
    else:
        print(f"❌ 查询失败: {result.get('msg')}")
    
    return result


def create_tts(text, audio_id, style="1", genre=None, output=None):
    """创建TTS任务并等待完成"""
    data = {
        'audioId': audio_id,
        'content': text,
        'style': style
    }
    if genre is not None:
        data['genre'] = genre
    
    result = make_request('POST', '/tts/create', data)
    
    if result.get('code') != 0:
        print(f"❌ 创建失败: {result.get('msg')}")
        return None
    
    task_id = result['data']['taskId']
    print(f"⏳ TTS任务已创建: {task_id}")
    
    # 等待完成
    for i in range(60):
        time.sleep(1)
        query_result = make_request('GET', f'/tts/result?taskId={task_id}')
        if query_result.get('code') == 0:
            status = query_result['data']['status']
            if status == 2 or status == 3:
                voice_url = query_result['data'].get('voiceUrl')
                if voice_url:
                    # 确定输出文件名
                    if not output:
                        output = f"tts_{task_id[:8]}.wav"
                    # 下载音频
                    try:
                        req = urllib.request.Request(voice_url, headers={'sign': API_KEY})
                        with urllib.request.urlopen(req, timeout=60) as response:
                            with open(output, 'wb') as f:
                                f.write(response.read())
                        print(f"✅ 合成完成！已保存到: {os.path.abspath(output)}")
                        return {"code": 0, "task_id": task_id, "output": os.path.abspath(output), "url": voice_url}
                    except Exception as e:
                        print(f"❌ 下载失败: {e}")
                        return {"code": -1, "msg": str(e)}
            print(f"\r等待中... {i+1}/60", end="", flush=True)
    
    print()
    print("❌ 超时未完成")
    return None


def delete_model(audio_id):
    """删除模型"""
    result = make_request('DELETE', f'/reference/delete?audioId={audio_id}')
    
    if result.get('code') == 0:
        print(f"✅ 模型已删除: {audio_id}")
    else:
        print(f"❌ 删除失败: {result.get('msg')}")
    
    return result


def main():
    parser = argparse.ArgumentParser(description="LipVoice TTS 语音合成工具")
    parser.add_argument('--api-key', help='LipVoice API Key (企业会员)')
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # 上传模型
    p_upload = subparsers.add_parser('upload', help='上传参考音频创建声音克隆模型')
    p_upload.add_argument('--file', required=True, help='参考音频文件路径 (支持mp3/wav/m4a)')
    p_upload.add_argument('--name', required=True, help='模型名称')
    p_upload.add_argument('--describe', default='', help='模型描述')
    
    # 列出模型
    subparsers.add_parser('list', help='列出所有已创建的声音模型')
    
    # 合成语音
    p_tts = subparsers.add_parser('tts', help='文本转语音，自动等待合成并下载')
    p_tts.add_argument('--text', required=True, help='要合成的文本')
    p_tts.add_argument('--audio-id', required=True, help='声音模型ID')
    p_tts.add_argument('--style', default='1', help='合成模式: 1=参考原音频风格, 2=大模型通用风格 (默认: 1)')
    p_tts.add_argument('--genre', type=int, help='语气参数 (可选)')
    p_tts.add_argument('--output', '-o', help='输出音频文件路径 (默认: tts_<taskid>.wav)')
    
    # 删除模型
    p_delete = subparsers.add_parser('delete', help='删除指定声音模型')
    p_delete.add_argument('--audio-id', required=True, help='要删除的模型ID')
    
    args = parser.parse_args()
    
    # 处理API Key
    global API_KEY
    if args.api_key:
        API_KEY = args.api_key
    
    if args.command == 'upload':
        upload_model(args.file, args.name, args.describe)
    elif args.command == 'list':
        list_models()
    elif args.command == 'tts':
        create_tts(args.text, args.audio_id, args.style, args.genre, args.output)
    elif args.command == 'delete':
        delete_model(args.audio_id)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
