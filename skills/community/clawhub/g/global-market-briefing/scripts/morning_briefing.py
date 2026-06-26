#!/usr/bin/env python3
"""
News 技能 - 财经早报
数据源：中国新闻网RSS（新闻）+ 腾讯行情（A股指数）
输出：完整MD存桌面 + 精简版给微信推送
"""
import requests, re, sys, os, xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
CST = timezone(timedelta(hours=8))

RSS_SOURCES = [
    ('finance.xml', '💰 财经'),
    ('china.xml', '🇨🇳 时政'),
    ('world.xml', '🌍 国际'),
    ('scroll-news.xml', '📋 滚动'),
    ('importnews.xml', '📌 要闻'),
]
RSS_BASE = 'https://www.chinanews.com.cn/rss'
OUTPUT_DIR = os.path.expanduser('~/Desktop/早间新闻')


def fetch_rss(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=8)
        tree = ET.fromstring(r.content)
        items = []
        for item in tree.findall('.//item'):
            title = item.findtext('title', '').strip()
            pub_date = item.findtext('pubDate', '')
            link = item.findtext('link', '').strip()
            desc = item.findtext('description', '')
            desc = re.sub(r'<[^>]+>', '', desc or '').strip()
            desc = re.sub(r'\s+', ' ', desc)[:150]
            if title:
                items.append({'title': title, 'pub_date': pub_date, 'link': link, 'desc': desc})
        return items
    except:
        return []


def parse_time(pub_str):
    try:
        clean = re.sub(r'\s+\+0800|\s+GMT', '', pub_str)
        dt = datetime.strptime(clean, '%a, %d %b %Y %H:%M:%S')
        return dt.replace(tzinfo=CST)
    except:
        return None


def get_a_shares():
    try:
        r = requests.get("http://qt.gtimg.cn/q=sh000001,sz399001,sz399006,sh000688,sh000016",
                         headers=HEADERS, timeout=8)
        r.encoding = 'gbk'
        items = []
        for line in r.text.strip().split(';'):
            if '~' in line:
                f = line.split('~')
                if len(f) > 32 and f[3]:
                    pct = float(f[32])
                    arrow = '🟢' if pct > 0 else '🔴'
                    items.append({'name': f[1], 'price': f[3], 'pct': pct, 'arrow': arrow})
        return items
    except:
        return []


def classify(title):
    kw = {
        '💰 财经/市场': [
            '股市','基金','债券','期货','银行','央行','货币','通胀','GDP','利率',
            '外汇','人民币','美元','黄金','油价','关税','投资','融资','上市','财报',
            '营收','利润','经济','贸易','指数','保险','北向','南向','沪股通','深股通',
            'A股','港股','美股','降息','加息','放水','信贷','财政','税务','税收',
            '海关','出口','进口','跨境','金融','证券','资本','市值',
            '企业','公司','产业','行业','市场','消费','降准','LPR',
            '工业','制造','工厂','产值','收入','支出','预算','赤字',
            '涨价','降价','下跌','上涨','震荡','反弹','牛市','熊市',
            '沪指','深指','创指','大盘','板块','概念','涨停','跌停',
            '商品','原油','天然气','煤炭','钢铁','矿产','现货',
            'AI','人工智能','芯片','半导体','算力','数据','数字',
            '电商','零售','餐饮','旅游','航空','物流','航运',
            '房地产','楼市','房价','保障房','租赁','土地',
            '新能源','光伏','风电','锂电','电池','电动车','汽车',
            '医药','医疗','药企','生物','科技','创新',
        ],
        '🇨🇳 时政/政策': [
            '习近平','总理','国务院','全国人大','政协','中共中央',
            '发改委','商务部','住建部','外交部','国防部','司法',
            '政策','法规','意见','改革','制度','监督',
            '中国','北京','上海','广东','深圳','重庆',
            '党代会','两会','全会','座谈会','调研',
            '反腐败','审查调查','违法','违纪','巡视',
            '公告','发布','规划','方案','通知',
            '公安','法院','检察','法治','法律',
            '军事','军队','国防','航天','发射','卫星',
            '脱贫攻坚','乡村振兴','农业','农村','农民',
            '教育','学校','大学','学生','考试',
            '医疗','医保','社保','养老','就业',
        ],
        '🌍 国际/地缘': [
            '美国','欧洲','俄罗斯','日本','韩国','印度','东盟',
            '联合国','北约','G7','G20','伊朗','乌克兰',
            '特朗普','美联储','欧央行','中东','非洲',
            '拜登','普京','欧洲央行','IMF','世界银行',
            '战争','冲突','停火','制裁','谈判','协议','外交',
            '使馆','领事','抗议','示威','大选','选举',
            '海峡','全球','海外','国际','同盟',
            '香港','澳门','台湾','新加坡','朝鲜',
            '英国','法国','德国','意大利','西班牙','加拿大',
            '澳大利亚','新西兰','巴西','南非','沙特','阿联酋',
            '一带一路','丝路','RCEP','APEC',
        ],
    }
    for cat, words in kw.items():
        if any(w in title for w in words):
            return cat
    return '📌 其他要闻'


if __name__ == "__main__":
    stdout_mode = '--stdout' in sys.argv
    
    now = datetime.now(CST)
    today = now.strftime('%Y-%m-%d')
    weekdays = ['周一','周二','周三','周四','周五','周六','周日']
    wd = weekdays[now.weekday()]

    # ===== 收集新闻 =====
    all_news = []
    for rss_file, label in RSS_SOURCES:
        items = fetch_rss(f"{RSS_BASE}/{rss_file}")
        all_news.extend(items)

    for item in all_news:
        item['dt'] = parse_time(item['pub_date'])
    all_news = [n for n in all_news if n['dt'] is not None]
    all_news.sort(key=lambda x: x['dt'], reverse=True)

    seen = set()
    unique = []
    for item in all_news:
        key = item['title'][:20]
        if key not in seen:
            seen.add(key)
            unique.append(item)

    categorized = {}
    for item in unique:
        cat = classify(item['title'])
        categorized.setdefault(cat, []).append(item)

    cat_order = ['💰 财经/市场', '🇨🇳 时政/政策', '🌍 国际/地缘', '📌 其他要闻']

    # ===== 生成完整MD =====
    full = []
    full.append(f"# 📰 财经早报 — {today}（{wd}）")
    full.append("")

    a_shares = get_a_shares()
    if a_shares:
        full.append("## 📈 A股盘前")
        full.append("")
        full.append("| 指数 | 点位 | 涨跌幅 |")
        full.append("|:----:|:----:|:------:|")
        for s in a_shares:
            full.append(f"| {s['name']} | {s['price']} | {s['arrow']} {s['pct']:+.2f}% |")
        full.append("")

    full.append("## 📰 新闻摘要")
    full.append("")

    total_news = 0
    for cat in cat_order:
        items = categorized.get(cat, [])
        if not items:
            continue
        full.append(f"### {cat}")
        full.append("")
        for i, item in enumerate(items[:15], 1):
            t = item['dt'].strftime('%H:%M')
            full.append(f"**{i}. [{t}] {item['title']}**")
            if item['link']:
                full.append(f"   🔗 {item['link']}")
            if item['desc']:
                full.append(f"   {item['desc']}")
            full.append("")
            total_news += 1

    full.append("---")
    full.append(f"*数据来源：中国新闻网 RSS / 腾讯财经 | 共{total_news}条 | 生成时间 {now.strftime('%H:%M')}*")

    full_text = '\n'.join(full)

    # ===== 保存到桌面 =====
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filepath = os.path.join(OUTPUT_DIR, f"morning_briefing_{today}.md")
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(full_text)

    if stdout_mode:
        # ===== 全量输出（其他平台用，不保存文件）=====
        print(full_text)
    else:
        # ===== 精简版输出（微信推送用）=====
        brief = []
        brief.append(f"📰 **财经早报 — {today}（{wd}）**")
        brief.append("")

        if a_shares:
            brief.append("📈 **A股盘前**")
            for s in a_shares:
                brief.append(f"  {s['name']} {s['price']} {s['arrow']} {s['pct']:+.2f}%")
            brief.append("")

        for cat in cat_order:
            items = categorized.get(cat, [])
            if not items:
                continue
            brief.append(f"**{cat}**")
            for item in items[:3]:
                t = item['dt'].strftime('%H:%M')
                brief.append(f"  [{t}] {item['title']}")
            if len(items) > 3:
                brief.append(f"  ... 共{len(items)}条")
            brief.append("")

        brief.append(f"---")
        brief.append(f"📎 完整早报含链接已保存至桌面/早间新闻/")
        brief.append(f"📊 共{total_news}条")

        print('\n'.join(brief))
