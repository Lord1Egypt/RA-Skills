#!/usr/bin/env python3
# modules/bitable_sync.py - 飞书多维表格同步
"""
将爬取的热搜数据同步到飞书多维表格
表格：每日热点追踪
Token：从 OpenClaw 加密存储读取
"""
import json, sys, os, time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BITABLE_API = 'https://open.feishu.cn/open-apis/bitable/v1'
APP_TOKEN = 'EcxVb1xh4aIcznshzXrcxYAgnEe'
TABLE_ID = 'tblcLEKcCpw5haoa'
# 找到 scripts/.feishu_token.json（向上4级：modules > hot-radar > skills > workspace）
WORKSPACE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
TOKEN_FILE = os.path.join(WORKSPACE, 'scripts', '.feishu_token.json')


def _load_token():
    try:
        with open(TOKEN_FILE, encoding='utf-8') as f:
            return json.load(f).get('accessToken', '')
    except Exception:
        return None


def _lark_post(endpoint, payload):
    """POST 到飞书 API"""
    import urllib.request, urllib.error
    token = _load_token()
    if not token:
        print('  ⚠️ 未找到飞书 Token，跳过同步')
        return None

    url = f'{BITABLE_API}/{endpoint}'
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, method='POST')
    req.add_header('Authorization', f'Bearer {token}')
    req.add_header('Content-Type', 'application/json')
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except Exception as e:
        print(f'  ⚠️ 飞书 API 失败: {e}')
        return None


def _parse_hot(v):
    """热度值转整数"""
    try:
        if isinstance(v, (int, float)):
            return int(v)
        if isinstance(v, str):
            import re
            v = re.sub(r'[^\d.]', '', v)
            return int(float(v)) if v else 0
        return 0
    except (ValueError, TypeError):
        return 0


def _build_link_obj(title, url):
    """构造超链接字段"""
    text = title[:20] if title else '查看'
    return {'link': url, 'text': text}


def sync_to_bitable(all_items, date_str=None):
    """
    同步数据到飞书多维表格
    all_items: dict，{平台名: [items]}
    date_str: 'YYYY-MM-DD'，默认为今天
    """
    if date_str is None:
        from datetime import date
        date_str = date.today().isoformat()

    # 计算当天毫秒时间戳
    from datetime import datetime, timezone, timedelta
    tz = timezone(timedelta(hours=8))
    dt = datetime.strptime(date_str, '%Y-%m-%d').replace(tzinfo=tz)
    date_ts = int(dt.timestamp() * 1000)

    print(f'\n📤 正在同步到飞书多维表格...')
    print(f'  表格: 每日热点追踪 ({APP_TOKEN})')

    total = 0
    for platform, items in all_items.items():
        if not items:
            continue

        # 构建记录
        records = []
        for item in items:
            title = item.get('title', '')[:200]
            link = item.get('link', '')
            hot = _parse_hot(item.get('hot', 0))
            record = {
                'fields': {
                    '平台': platform,
                    '标题': title,
                    '链接': _build_link_obj(title, link),
                    '热度值': hot,
                    '爬取日期': date_ts,
                }
            }
            records.append(record)

        # 批量写入（每批10条）
        written = 0
        for i in range(0, len(records), 10):
            batch = records[i:i+10]
            result = _lark_post(
                f'apps/{APP_TOKEN}/tables/{TABLE_ID}/records/batch_create',
                {'records': batch}
            )
            if result and result.get('code') == 0:
                written += len(batch)
                total += len(batch)
                print(f'  ✅ {platform}: 写入 {len(batch)} 条')
            else:
                msg = (result or {}).get('msg', '未知错误')
                print(f'  ⚠️ {platform} 批次失败: {msg}')
            time.sleep(0.5)

        if written == 0 and records:
            print(f'  ⚠️ {platform}: 写入失败，跳过')

    print(f'\n🎉 共同步 {total} 条到飞书多维表格')
    return total


if __name__ == '__main__':
    # 测试
    test_data = {
        '知乎热榜': [
            {'title': '测试标题', 'link': 'https://zhihu.com', 'hot': '1000'},
        ]
    }
    sync_to_bitable(test_data)
