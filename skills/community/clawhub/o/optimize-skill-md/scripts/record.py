#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
optimize-skill-md/scripts/record.py

SKILL.md 优化记录上报脚本
用途：每次使用 optimize-skill-md 技能时调用一次记录接口

记录接口：https://redfox.hk/story/api/skill/record/save
网络实现：使用 requests 库，开启 SSL 证书验证
鉴权方式：优先使用内置 API Key，不可用时从环境变量 REDFOX_API_KEY 读取
固定参数：SKILL.md优化

用法：
  python record.py
"""

import sys
import os

try:
    import requests
except ImportError:
    print("❌ 缺少依赖：requests")
    print("请执行：pip install requests")
    sys.exit(1)

RECORD_URL = 'https://redfox.hk/story/api/skill/record/save'
SKILL_NAME = 'SKILL.md优化-GitHub'
BUILTIN_API_KEY = 'ak_b45b6a6881f4400fb321428947eb6661'


def _get_api_keys() -> list:
    """返回可用 API Key 列表：内置 Key + 环境变量 Key（去重）。"""
    keys = []
    if BUILTIN_API_KEY:
        keys.append(BUILTIN_API_KEY)
    env_key = os.getenv('REDFOX_API_KEY', '').strip()
    if env_key and env_key not in keys:
        keys.append(env_key)
    if not keys:
        print('❌ 未配置 REDFOX_API_KEY 环境变量')
        print('请前往 https://www.redfox.hk/login 注册获取个人 API Token')
        print('然后通过以下方式配置：')
        print('  export REDFOX_API_KEY="ak_xxxx..."')
        sys.exit(1)
    return keys


def save_record():
    """调用记录接口，上报一次技能使用记录。逐个尝试可用 Key。"""
    payload = {'skillName': SKILL_NAME}
    for api_key in _get_api_keys():
        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'X-API-Key': api_key,
        }
        try:
            resp = requests.post(
                RECORD_URL,
                json=payload,
                headers=headers,
                verify=True,
                timeout=10
            )
            if resp.status_code == 200:
                data = resp.json()
                code = data.get('code')
                if code in (200, 2000):
                    print('✅ 记录上报成功')
                    return
                elif code in (3106, 3107):
                    continue  # Key 失效，尝试下一个
                else:
                    print(f'⚠️ 接口返回异常：{data}')
                    return
            else:
                print(f'⚠️ HTTP {resp.status_code}：{resp.text}')
                return
        except requests.exceptions.RequestException as e:
            print(f'⚠️ 记录上报失败（不影响主流程）：{e}')
            return
    print('⚠️ 所有 API Key 均已失效，请前往 https://www.redfox.hk/login 获取个人 Key')
    print('  配置：export REDFOX_API_KEY="ak_xxxx..."')


if __name__ == '__main__':
    save_record()
