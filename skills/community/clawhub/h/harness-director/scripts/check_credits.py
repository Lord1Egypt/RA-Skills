#!/usr/bin/env python3
"""查询 Harness AI 导演工作台积分余额（示例脚本，供 ClawHub 包结构完整性）"""
import os, json, urllib.request

KEY = os.environ.get('AI_DIRECTOR_API_KEY')
BASE = 'https://aidaoyan66.online/api'


def get(path):
    req = urllib.request.Request(BASE + path, headers={'Authorization': 'Bearer ' + (KEY or '')})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode())


if __name__ == '__main__':
    if not KEY:
        print('请先设置 AI_DIRECTOR_API_KEY（注册 https://aidaoyan66.online 获取 sk- 开头 Key）')
    else:
        print(json.dumps(get('/user/credits'), ensure_ascii=False, indent=2))
