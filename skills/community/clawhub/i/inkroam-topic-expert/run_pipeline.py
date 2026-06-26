#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
选题专家一键运行脚本
抓取 tophub.today → AI相关度筛选 + 打分 → 写入飞书选题库 → 输出推送文本
"""

import json
import re
import sys
import httpx
from pathlib import Path
from datetime import datetime

# ========== 配置（从环境变量读取，不硬编码） ==========
import os

def _env(key, default=None):
    val = os.environ.get(key, default)
    if val is None:
        raise EnvironmentError(f"缺少环境变量: {key}，请在 config.json 或 .env 中配置")
    return val

FEISHU_APP_ID = _env("FEISHU_APP_ID")
FEISHU_APP_SECRET = _env("FEISHU_APP_SECRET")
FEISHU_API = _env("FEISHU_API", "https://open.feishu.cn/open-apis")
APP_TOKEN = _env("FEISHU_APP_TOKEN")
TABLE_ID = _env("FEISHU_TABLE_ID")

# AI / 自媒体 / 效率 相关关键词
CORE_KEYWORDS = [
    'AI', 'ai', 'Ai', '人工智能', 'ChatGPT', 'GPT', 'Claude', 'OpenAI',
    '大模型', 'LLM', 'Gemini', 'Sora', 'AGI', 'Copilot', 'Cursor',
    'Manus', 'DeepSeek', 'deepseek', '通义', '文心', 'Kimi',
]
BROAD_KEYWORDS = [
    '效率', '自媒体', '副业', '写作', '变现', '创业', '工具', '编程',
    '程序员', '开发者', '互联网', '科技', '产品', '运营', '赚钱',
    '职场', '裁员', '降薪', '加班', '内卷', '35岁', '转型',
    '公众号', '小红书', '短视频', '直播', '带货', '流量',
    '专业', '大学', '教育', '就业',
]

# 优先平台（权重更高）
PRIORITY_PLATFORMS = {'知乎', '微信', '36氪', '虎嗅网', '少数派', '量子位', '机器之心', 'Readhub'}

# 标签映射
TAG_KEYWORDS = {
    'AI': ['AI', 'ai', '人工智能', 'GPT', 'ChatGPT', 'Claude', 'OpenAI', '大模型', 'LLM', 'DeepSeek', 'Manus', 'Cursor'],
    '副业': ['副业', '赚钱', '变现', '收入', '月入'],
    '自媒体': ['自媒体', '公众号', '小红书', '短视频', '直播', '带货', '流量'],
    '写作': ['写作', '文章', '文案', '笔记'],
    '工具': ['工具', '软件', '插件', 'app', 'App', 'APP', 'Cursor', 'Copilot'],
    '变现': ['变现', '商业化', '盈利', '融资', '投资'],
    '运营': ['运营', '增长', '推广', '营销'],
    '技巧': ['技巧', '方法', '攻略', '教程', '实操'],
}


def get_feishu_token():
    """获取飞书 token"""
    resp = httpx.post(
        f"{FEISHU_API}/auth/v3/tenant_access_token/internal",
        json={"app_id": FEISHU_APP_ID, "app_secret": FEISHU_APP_SECRET},
        timeout=10
    )
    data = resp.json()
    if data.get("code") != 0:
        raise Exception(f"Token 失败: {data}")
    return data["tenant_access_token"]


def fetch_tophub():
    """从 tophub.today 抓取热点"""
    import requests
    from bs4 import BeautifulSoup

    WANTED = {
        '微博', '知乎', '微信', '百度', '36氪', '少数派',
        '虎嗅网', 'IT之家', '掘金', '机器之心', '量子位',
        'Readhub', '哔哩哔哩', '抖音', '快手', 'GitHub',
    }

    resp = requests.get('https://tophub.today/', headers={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    }, timeout=15)
    resp.encoding = 'utf-8'
    soup = BeautifulSoup(resp.text, 'html.parser')

    topics = []
    for card in soup.select('.cc-cd'):
        lb = card.select_one('.cc-cd-lb')
        platform = lb.get_text(strip=True).split('‧')[0].strip() if lb else ''

        if not any(w in platform for w in WANTED):
            continue

        for i, item in enumerate(card.select('.cc-cd-cb-ll')):
            t_tag = item.select_one('.t')
            e_tag = item.select_one('.e')
            title = t_tag.get_text(strip=True) if t_tag else ''
            if not title:
                continue
            hot_text = e_tag.get_text(strip=True) if e_tag else ''
            topics.append({
                'title': title,
                'platform': platform,
                'hot': parse_hot(hot_text),
                'hot_text': hot_text,
                'rank': i + 1,
            })

    return topics


def parse_hot(text):
    """解析热度值（万为单位）"""
    if not text:
        return 0
    text = text.replace(',', '').replace(' ', '')
    try:
        if '亿' in text:
            m = re.search(r'([\d.]+)\s*亿', text)
            return int(float(m.group(1)) * 10000) if m else 0
        elif '万' in text:
            m = re.search(r'([\d.]+)\s*万', text)
            return int(float(m.group(1))) if m else 0
        else:
            m = re.search(r'(\d+)', text)
            if m:
                val = int(m.group(1))
                return val // 10000 if val > 10000 else 0
            return 0
    except:
        return 0


def score_topic(topic):
    """对单个选题打分（满分100）"""
    title = topic['title']
    platform = topic['platform']
    hot = topic['hot']

    # 1. 热度分（30分）
    if hot >= 500:
        hot_score = 30
    elif hot >= 200:
        hot_score = 25
    elif hot >= 50:
        hot_score = 20
    elif hot >= 10:
        hot_score = 15
    else:
        hot_score = 8

    # 2. 相关度（25分）
    rel_score = 0
    for kw in CORE_KEYWORDS:
        if kw in title:
            rel_score = 25
            break
    if rel_score == 0:
        matched = sum(1 for kw in BROAD_KEYWORDS if kw in title)
        rel_score = min(matched * 8, 25)

    # 3. 时效性（20分）- 排名越靠前越新鲜，热度越高说明当前正在爆发
    rank = topic.get('rank', 50)
    if rank <= 3:
        time_score = 20   # TOP3 = 刚刚爆发
    elif rank <= 10:
        time_score = 18
    elif rank <= 20:
        time_score = 15
    elif rank <= 35:
        time_score = 12
    else:
        time_score = 8    # 排名靠后 = 可能已过峰值

    # 4. 可写性（15分）
    write_score = 8
    if 10 <= len(title) <= 40:
        write_score += 4
    if any(c in title for c in '？?'):
        write_score += 2
    if any(c.isdigit() for c in title):
        write_score += 1
    write_score = min(write_score, 15)

    # 5. 差异化（10分）- 优先平台加分
    diff_score = 5
    if platform in PRIORITY_PLATFORMS:
        diff_score += 3
    if topic['rank'] <= 5:
        diff_score += 2
    diff_score = min(diff_score, 10)

    total = hot_score + rel_score + time_score + write_score + diff_score
    return {
        'total': total,
        'hot': hot_score,
        'relevance': rel_score,
        'timeliness': time_score,
        'writability': write_score,
        'differentiation': diff_score,
    }


def assign_tags(title):
    """自动分配标签"""
    tags = []
    for tag, keywords in TAG_KEYWORDS.items():
        if any(kw in title for kw in keywords):
            tags.append(tag)
    return tags if tags else ['其他']


def assign_priority(score):
    """根据分数分配优先级"""
    if score >= 80:
        return '高'
    elif score >= 65:
        return '中'
    else:
        return '低'


def generate_rough_elements(topic):
    """生成初步三要素（粗粒度）"""
    title = topic['title']
    platform = topic['platform']

    # 简单的规则化三要素
    target = "关注AI/科技/效率的自媒体人和职场人"
    pain = f"看到「{title[:20]}...」想了解但没时间深挖"
    solution = f"基于{platform}热点数据，拆解核心信息+给出可执行建议"

    return target, pain, solution


def write_to_feishu(token, topics_with_scores):
    """批量写入飞书多维表格"""
    url = f"{FEISHU_API}/bitable/v1/apps/{APP_TOKEN}/tables/{TABLE_ID}/records/batch_create"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    records = []
    now_ms = int(datetime.now().timestamp() * 1000)  # 飞书日期字段用毫秒时间戳
    for item in topics_with_scores:
        topic = item['topic']
        scores = item['scores']
        target, pain, solution = generate_rough_elements(topic)
        tags = assign_tags(topic['title'])
        priority = assign_priority(scores['total'])

        fields = {
            "文本": topic['title'],
            "平台来源": topic['platform'],
            "热度值": topic['hot'],
            "采集时间": now_ms,
            "状态": "待处理",
            "目标人群": target,
            "痛点": pain,
            "解决方案": solution,
            "标签": tags,
            "优先级": priority,
            "备注": f"评分:{scores['total']} (热度{scores['hot']}+相关{scores['relevance']}+时效{scores['timeliness']}+可写{scores['writability']}+差异{scores['differentiation']}) | {topic.get('hot_text','')} | 排名#{topic['rank']}",
        }
        records.append({"fields": fields})

    # 飞书批量接口最多500条，分批
    success = 0
    for i in range(0, len(records), 100):
        batch = records[i:i+100]
        resp = httpx.post(url, headers=headers, json={"records": batch}, timeout=30)
        data = resp.json()
        if data.get("code") == 0:
            success += len(batch)
        else:
            print(f"  ✗ 批量写入失败: {data.get('msg', data)}")
            # 逐条重试
            for rec in batch:
                single_url = f"{FEISHU_API}/bitable/v1/apps/{APP_TOKEN}/tables/{TABLE_ID}/records"
                r = httpx.post(single_url, headers=headers, json=rec, timeout=15)
                if r.json().get("code") == 0:
                    success += 1

    return success


def format_telegram_message(ranked_topics):
    """格式化 Telegram 推送消息"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [f"📊 **选题推荐** | {now}\n"]

    s_topics = [t for t in ranked_topics if t['scores']['total'] >= 80]
    a_topics = [t for t in ranked_topics if 65 <= t['scores']['total'] < 80]

    if s_topics:
        lines.append("🔥 **S级（强烈推荐）**")
        for i, item in enumerate(s_topics[:5], 1):
            t = item['topic']
            s = item['scores']
            tags = ' '.join(f'#{tag}' for tag in assign_tags(t['title']))
            lines.append(f"{i}. **{t['title']}**")
            lines.append(f"   📈 {t['platform']} {t['hot']}万 | 评分{s['total']} | {tags}")
        lines.append("")

    if a_topics:
        lines.append("✅ **A级（推荐）**")
        start = len(s_topics) + 1
        for i, item in enumerate(a_topics[:5], start):
            t = item['topic']
            s = item['scores']
            lines.append(f"{i}. {t['title']}")
            lines.append(f"   📈 {t['platform']} {t['hot']}万 | 评分{s['total']}")
        lines.append("")

    lines.append(f"共筛选 {len(ranked_topics)} 个选题，已写入飞书选题库")
    lines.append("回复「采纳1 3 5」→ 笔尖专家开写")

    return '\n'.join(lines)


def main():
    print("🚀 选题专家启动\n")

    # 1. 抓取
    print("📡 正在抓取 tophub.today...")
    all_topics = fetch_tophub()
    print(f"   抓到 {len(all_topics)} 条原始数据\n")

    # 2. 打分
    print("📊 正在打分筛选...")
    scored = []
    for topic in all_topics:
        scores = score_topic(topic)
        if scores['total'] >= 60:  # 60分以上才入库
            scored.append({'topic': topic, 'scores': scores})

    scored.sort(key=lambda x: x['scores']['total'], reverse=True)
    print(f"   {len(scored)} 条达标（≥60分）\n")

    # 去重（同标题只保留热度最高的）
    seen = set()
    deduped = []
    for item in scored:
        key = item['topic']['title'][:20]  # 前20字符去重
        if key not in seen:
            seen.add(key)
            deduped.append(item)
    scored = deduped
    print(f"   去重后 {len(scored)} 条\n")

    if not scored:
        print("⚠️ 没有达标选题，结束")
        return

    # 3. 写入飞书
    print("📝 正在写入飞书选题库...")
    token = get_feishu_token()
    success = write_to_feishu(token, scored[:30])  # 最多写30条
    print(f"   ✅ {success} 条写入成功\n")

    # 4. 生成推送消息
    msg = format_telegram_message(scored)
    print("=" * 50)
    print(msg)
    print("=" * 50)

    # 保存推送消息供外部使用
    output = {
        "message": msg,
        "total_fetched": len(all_topics),
        "total_qualified": len(scored),
        "written_to_feishu": success,
        "timestamp": datetime.now().isoformat(),
        "top_topics": [
            {
                "title": item['topic']['title'],
                "platform": item['topic']['platform'],
                "hot": item['topic']['hot'],
                "score": item['scores']['total'],
                "tags": assign_tags(item['topic']['title']),
                "priority": assign_priority(item['scores']['total']),
            }
            for item in scored[:15]
        ]
    }

    output_path = Path(__file__).parent / "output" / "latest_run.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\n💾 结果已保存到 {output_path}")
    print("✅ 选题专家运行完成")


if __name__ == '__main__':
    main()
