#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
直播复盘分析器 - V2 (Secure & Portable)
"""

import os
import sys
import json
import time
import argparse
import requests
from pathlib import Path
import asyncio
import aiohttp

# ==================== 路径配置 (V2 - 动态) ====================
SKILL_DIR = Path(__file__).parent
INPUT_DIR = SKILL_DIR / "input"
OUTPUT_DIR = SKILL_DIR / "output"
TEMPLATE_FILE = SKILL_DIR / "prompt_template.txt"

# ==================== 配置读取 ====================
def get_config_value(key: str, default=None):
    """从 ~/.openclaw/config.json 安全地读取配置值"""
    config_path = Path.home() / '.openclaw' / 'config.json'
    if not config_path.exists():
        return default
    try:
        config = json.loads(config_path.read_text(encoding='utf-8'))
        return config.get(key, default)
    except (json.JSONDecodeError, IOError):
        return default

# ==================== 辅助函数 ====================
def read_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"❌ 读取文件失败 {file_path}: {e}", file=sys.stderr)
        return None

# ==================== 模型调用 ====================
async def model_gpt(message_list, model: str = "gemini-2.5-pro"):
    """调用大模型，返回生成的文本内容"""
    # 从配置中读取 API 信息
    api_url = get_config_value('review_api_url', 'https://api2.aigcbest.top/v1/chat/completions')
    api_key = get_config_value('review_api_key')
    
    if not api_key:
        print("❌ 错误：未在 config.json 中配置 'review_api_key'", file=sys.stderr)
        sys.exit(1)
    
    error_msg = ""
    async with aiohttp.ClientSession() as session:
        for i in range(3):  # 最多重试 3 次
            try:
                async with session.post(
                        api_url,
                        headers={
                            'Authorization': f'Bearer {api_key}',
                            'Content-Type': 'application/json'
                        },
                        data=json.dumps({
                            "model": model,
                            "messages": message_list,
                            "max_tokens": 12000,
                            "temperature": 0
                        }),
                        timeout=999
                ) as response:
                    data = await response.json()
                    if content := data.get('choices', [{}])[0].get('message', {}).get('content'):
                        return content
            except Exception as e:
                error_msg = str(e)
                await asyncio.sleep(i * 2)  # 指数退避
    return error_msg

# ==================== 主程序 ====================
def main():
    parser = argparse.ArgumentParser(description="直播复盘分析器 (V2)")
    parser.add_argument("--client", required=True, help="客户名称")
    parser.add_argument("--session", required=True, help="直播场次名称")
    parser.add_argument("--call-model", action="store_true", help="直接调用模型生成复盘，否则只生成提示词文件")
    args = parser.parse_args()

    client = args.client
    session = args.session

    # 构建输入文件路径
    session_dir = INPUT_DIR / client / session
    data_file = session_dir / "data.txt"
    profile_file = session_dir / "profile.txt"
    script_file = session_dir / "script.txt"

    out_dir = OUTPUT_DIR / client / session

    for f in [data_file, profile_file, script_file]:
        if not f.exists():
            print(f"❌ 文件不存在：{f}", file=sys.stderr)
            sys.exit(1)

    # 读取模板
    if not TEMPLATE_FILE.exists():
        print(f"❌ 模板文件不存在：{TEMPLATE_FILE}", file=sys.stderr)
        sys.exit(1)
    template = read_file(TEMPLATE_FILE)
    if template is None:
        sys.exit(1)

    # 读取输入
    data_content = read_file(data_file)
    profile_content = read_file(profile_file)
    script_content = read_file(script_file)
    if None in (data_content, profile_content, script_content):
        sys.exit(1)

    timestamp=time.strftime("%Y%m%d%H%M%S", time.localtime())
    # 填充提示词
    prompt = template.replace("{直播数据}", data_content) \
                     .replace("{用户画像}", profile_content) \
                     .replace("{直播回放文字稿}", script_content)

    if args.call_model:
        # 准备消息列表
        messages = [{"role": "user", "content": prompt}]
        try:
            # 异步调用模型
            generated_scripts = asyncio.run(model_gpt(messages))
        except Exception as e:
            print(f"模型调用失败：{e}")
            return

        # 保存生成的脚本
        out_dir.mkdir(parents=True, exist_ok=True)
        out_filename = f"{client}-{session}_report_{timestamp}.md"
        output_path = out_dir / out_filename
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(generated_scripts)
        print(f"✅方案已保存至：{output_path}")
    # 输出组装好的提示词
    print(prompt)

if __name__ == "__main__":
    main()
