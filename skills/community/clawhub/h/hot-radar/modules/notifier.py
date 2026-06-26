#!/usr/bin/env python3
# modules/notifier.py - 飞书推送通知
"""
将日报推送到飞书私聊用户。
使用 urllib 直接发 HTTP 请求（避免 requests 库在 Python 环境中的兼容问题）。
"""
import json, sys, os, urllib.request, urllib.error, ssl

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
WORKSPACE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
TOKEN_FILE = os.path.join(WORKSPACE, 'scripts', '.feishu_token.json')


def _load_token():
    try:
        with open(TOKEN_FILE, encoding='utf-8') as f:
            return json.load(f).get('accessToken', '')
    except Exception:
        return None


def _post(url, payload, token):
    """POST 到飞书 API"""
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, method='POST')
    req.add_header('Authorization', f'Bearer {token}')
    req.add_header('Content-Type', 'application/json')
    ctx = ssl.create_default_context()
    try:
        with urllib.request.urlopen(req, timeout=15, context=ctx) as r:
            return json.loads(r.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        return {'code': e.code, 'msg': e.read().decode('utf-8', errors='replace')}
    except Exception as e:
        return {'code': -1, 'msg': str(e)}


def _get(url, token):
    """GET 飞书 API"""
    req = urllib.request.Request(url)
    req.add_header('Authorization', f'Bearer {token}')
    ctx = ssl.create_default_context()
    try:
        with urllib.request.urlopen(req, timeout=15, context=ctx) as r:
            return json.loads(r.read().decode('utf-8'))
    except Exception as e:
        return {'code': -1, 'msg': str(e)}


def send_message(text, token=None):
    """发送纯文本消息到私聊用户"""
    token = token or _load_token()
    if not token:
        print('  ⚠️ 未找到飞书 Token，跳过消息推送')
        return False

    USER_OPEN_ID = 'ou_55de636cdcc8e2facd8a54121c94cdbc'

    payload = {
        'receive_id': USER_OPEN_ID,
        'msg_type': 'text',
        'content': json.dumps({'text': text}),
    }

    result = _post(
        'https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id',
        payload, token
    )
    if result.get('code') == 0:
        print('  ✅ 飞书消息发送成功')
        return True
    else:
        print(f'  ⚠️ 飞书消息失败: {result.get("msg", "")[:100]}')
        return False


def send_report(report_md, date, token=None):
    """
    发送热点日报简报到飞书私聊。

    先尝试发送富文本 post 消息，如果格式错误则降级为 text 消息。
    """
    token = token or _load_token()
    if not token:
        print('  ⚠️ 未找到飞书 Token，跳过推送')
        return False

    USER_OPEN_ID = 'ou_55de636cdcc8e2facd8a54121c94cdbc'

    # ---- 尝试发送富文本 post 消息 ----
    lines = [l.strip() for l in report_md.split('\n') if l.strip()]

    # 提取标题
    title = f'📡 热点日报 {date}'

    # 提取排行榜前5
    top_items = []
    for i, line in enumerate(lines):
        if '🔥 热点排行榜' in line:
            # 找到排行榜后面的条目
            for j in range(i + 1, min(i + 10, len(lines))):
                l = lines[j]
                if l.startswith('|') and not l.startswith('|--'):
                    parts = [p.strip() for p in l.split('|') if p.strip() and not p.strip().startswith('排名')]
                    if len(parts) >= 2:
                        rank = parts[0]
                        topic = parts[1][:25]
                        top_items.append(f'  {rank}. {topic}')
            break

    # 构建飞书 post 消息体（每行是一个 paragraph）
    paragraphs = [
        [{'tag': 'text', 'text': title}],
        [{'tag': 'text', 'text': '共追踪 30 条热点，覆盖 7 个平台'}],
        [{'tag': 'at', 'text': '@熊叔'}],
        [{'tag': 'text', 'text': '━━━━━━━━━━━━━━━'}],
    ]
    for item in top_items[:5]:
        paragraphs.append([{'tag': 'text', 'text': item}])
    paragraphs.append([{'tag': 'text', 'text': '━━━━━━━━━━━━━━━'}])
    paragraphs.append([{'tag': 'a', 'text': '📊 查看飞书多维表格', 'href': 'https://a5jl1ri0mq.feishu.cn/base/EcxVb1xh4aIcznshzXrcxYAgnEe'}])
    paragraphs.append([{'tag': 'a', 'text': '📄 查看完整日报', 'href': 'https://a5jl1ri0mq.feishu.cn/docx/EcxVb1xh4aIcznshzXrcxYAgnEe'}])

    payload = {
        'receive_id': USER_OPEN_ID,
        'msg_type': 'post',
        'content': json.dumps({
            'zh_cn': {
                'title': title,
                'content': paragraphs
            }
        }, ensure_ascii=False),
    }

    result = _post(
        'https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id',
        payload, token
    )

    if result.get('code') == 0:
        print('  ✅ 飞书日报卡片发送成功')
        return True

    # 降级：发送 text 消息
    summary_lines = [
        title,
        '━━━━━━━━━━━━━━━',
        '🔥 热点排行榜',
        *top_items[:5],
        '━━━━━━━━━━━━━━━',
        '📊 飞书多维表格: https://a5jl1ri0mq.feishu.cn/base/EcxVb1xh4aIcznshzXrcxYAgnEe',
        '📄 完整日报: skills/hot-radar/reports/',
    ]
    return send_message('\n'.join(summary_lines), token)


if __name__ == '__main__':
    test = '# 📡 热点日报 2026-05-23\n\n## 🔥 热点排行榜\n| 1 | 神舟二十三号发射 |\n| 2 | U17男足亚军 |\n'
    send_report(test, '2026-05-23')
