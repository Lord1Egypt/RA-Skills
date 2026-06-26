#!/usr/bin/env python3
"""
全渠道选品 Agent — 一键执行完整调研
输出固定结构的 JSON + Slack 格式表格

环境变量:
  SEMRUSH_API_KEY  — Semrush API
  FB_ADS_TOKEN     — Facebook Ads Library API

输出:
  data/research_YYYY-MM-DD.json  — 完整结构化数据
  stdout                         — Slack 代码块表格

固定输出结构 (每行):
{
  "keyword": "blue background",
  "func_cn": "蓝色背景生成",
  "kd": 42,
  "volume": 49500,
  "region": "US",
  "comp_url": "https://www.photoroom.com/tools/...",
  "comp_domain": "photoroom.com",
  "coverage": "new|exists_sitemap|exists_cms|exists_notion|duplicate",
  "dedup_source": "",
  "fb_ads_count": 0,
  "fb_top_advertiser": "",
  "gap_score": 85.2,
  "priority": "high|medium|low"
}
"""
import csv, io, json, os, sys, re, urllib.request, urllib.parse
from datetime import datetime

# ─── Config ───
SEMRUSH_KEY = os.environ.get('SEMRUSH_API_KEY', '')
FB_TOKEN = os.environ.get('FB_ADS_TOKEN', '')
COMPETITORS = ['photoroom.com', 'remini.ai', 'fotor.com', 'picsart.com', 'faceapp.com', 'cutout.pro']
SITEMAP_URL = 'https://art.myshell.ai/sitemap.xml'
MIN_VOLUME = 1000
MAX_KD = 80

BRAND_TERMS = ['photoroom', 'remini', 'fotor', 'picsart', 'faceapp', 'cutout',
               'pixlr', 'photo room', 'pics art', 'pix art', 'cut pit', 'remin',
               'fotorom', 'photorrom', 'photorom', 'faxeapp']
EXCLUDE_TERMS = ['font', 'text generator', 'cursive', 'bold text', 'fancy text',
                 'copy and paste', 'copy paste', 'ai writer', 'fonts']

TRANSLATIONS = {
    'background remover': '背景移除', 'remove background': '背景移除',
    'white background': '白色背景生成', 'blue background': '蓝色背景生成',
    'transparent background': '透明背景生成', 'png maker': 'PNG透明图制作',
    'unblur image': '图片去模糊', 'image quality enhancer': '图片质量增强',
    'photo enhancer': '照片增强', 'photo enhancer ai': 'AI照片增强',
    'image enhancer': '图片增强工具', 'picture enhancer': '图片增强工具',
    'remove object from image': '移除图片物体', 'ai remover': 'AI物体移除',
    'test of attractiveness': '颜值测试', 'attractiveness test': '颜值测试',
    'how attractive am i': '颜值测试', 'am i pretty': '我好看吗测试',
    'what will my baby look like': '宝宝长相预测', 'face swap': '换脸',
    'color a background': '背景换色', 'rainbow background': '彩虹背景生成',
    'image in landscape': '竖图转横图', 'video enhancer': '视频增强工具',
    'photo editor': '照片编辑器', 'photo editor free': '免费照片编辑器',
    'image editor': '图片编辑器', 'face editing': '脸部编辑',
    'facial filter': '面部滤镜', 'background removal': '背景移除',
    'free background remover': '免费背景移除', 'background remover free': '免费背景移除',
    'ai background remover': 'AI背景移除', 'image background remover': '图片背景移除',
    'photo enhancer free': '免费照片增强', 'image enhancer free': '免费图片增强',
    'picture quality enhancer': '图片质量增强', 'increase image quality': '提升图片质量',
    'increase photo resolution': '提升照片分辨率', 'improve picture quality': '提升图片质量',
    'enhance image': '图片增强', 'enhance picture': '照片增强',
    'enhance picture quality': '图片质量增强', 'enhance a pic': '照片增强',
    'passport photo': '证件照制作', 'edit pic on pic': '图片叠加编辑',
}

def fetch_sitemap():
    try:
        resp = urllib.request.urlopen(SITEMAP_URL, timeout=10)
        index_xml = resp.read().decode()
        sub_urls = re.findall(r'<loc>(https://art\.myshell\.ai/\w+page\.xml)</loc>', index_xml)
        slugs = set()
        for sub_url in sub_urls[:1]:  # EN only
            resp2 = urllib.request.urlopen(sub_url, timeout=10)
            xml = resp2.read().decode()
            urls = re.findall(r'<loc>(https://art\.myshell\.ai/[^<]+)</loc>', xml)
            for u in urls:
                path = u.replace('https://art.myshell.ai/', '').lower()
                if path:
                    slugs.add(path)
                    parts = path.split('/')
                    if len(parts) > 1:
                        slugs.add(parts[-1])
        return slugs
    except Exception as e:
        print(f"⚠️ Sitemap fetch failed: {e}", file=sys.stderr)
        return set()

def fetch_semrush(domain, db='us', limit=40):
    if not SEMRUSH_KEY:
        return []
    url = (f"https://api.semrush.com/?type=domain_organic&key={SEMRUSH_KEY}"
           f"&display_limit={limit}&export_columns=Ph,Po,Nq,Cp,Co,Kd,Tr,Tc,Ur"
           f"&domain={domain}&database={db}")
    try:
        resp = urllib.request.urlopen(url, timeout=15)
        text = resp.read().decode()
        if 'ERROR' in text:
            return []
        return list(csv.DictReader(io.StringIO(text), delimiter=';'))
    except:
        return []

def fetch_fb_ads(keyword):
    """Query Facebook Ads Library for a keyword."""
    if not FB_TOKEN:
        return 0, ''
    try:
        params = urllib.parse.urlencode({
            'access_token': FB_TOKEN,
            'search_terms': keyword,
            'ad_type': 'ALL',
            'ad_reached_countries': '["US"]',
            'fields': 'page_name',
            'limit': 25,
        })
        url = f"https://graph.facebook.com/v21.0/ads_archive?{params}"
        resp = urllib.request.urlopen(url, timeout=10)
        data = json.loads(resp.read().decode())
        if 'data' in data:
            ads = data['data']
            # Find top advertiser
            pages = {}
            for ad in ads:
                pn = ad.get('page_name', '')
                pages[pn] = pages.get(pn, 0) + 1
            top = max(pages, key=pages.get) if pages else ''
            return len(ads), top
        return 0, ''
    except:
        return 0, ''

def translate(kw):
    if kw in TRANSLATIONS:
        return TRANSLATIONS[kw]
    for k, v in TRANSLATIONS.items():
        if k in kw or kw in k:
            return v
    return kw

def check_coverage(kw, slugs):
    kw_slug = kw.lower().replace(' ', '-')
    for slug in slugs:
        slug_kw = slug.split('/')[-1].replace('-', ' ')
        if kw_slug in slug or slug_kw == kw or kw in slug_kw or slug_kw in kw:
            return 'exists_sitemap', slug
    return 'new', ''

def calc_gap_score(vol, kd, fb_ads, coverage):
    """Gap Score = opportunity score (0-100)."""
    vol_score = min(vol / 2000, 40)  # max 40
    kd_score = max(0, (80 - kd) / 80) * 30  # max 30
    ads_score = min(fb_ads / 5, 15) if fb_ads > 0 else 5  # some ads = validated demand
    dedup_penalty = -30 if coverage != 'new' else 0
    return round(min(100, max(0, vol_score + kd_score + ads_score + 15 + dedup_penalty)), 1)

def priority_label(score):
    if score >= 70: return 'high'
    if score >= 45: return 'medium'
    return 'low'

def main():
    print("🔍 全渠道选品 Agent — 执行完整调研", file=sys.stderr)

    # Step 1: Sitemap
    print("  → Fetching sitemap...", file=sys.stderr)
    slugs = fetch_sitemap()
    print(f"    {len(slugs)} pages", file=sys.stderr)

    # Step 2: Semrush
    print("  → Fetching Semrush keywords...", file=sys.stderr)
    all_kws = {}
    for domain in COMPETITORS:
        rows = fetch_semrush(domain)
        print(f"    {domain}: {len(rows)}", file=sys.stderr)
        for row in rows:
            kw = row.get('Keyword', '').strip().lower()
            if not kw: continue
            vol = int(row.get('Search Volume', '0') or '0')
            kd = float(row.get('Keyword Difficulty', '0') or '0')
            url = row.get('Url', '')
            if any(kw == bt or kw.startswith(bt + ' ') or kw.endswith(' ' + bt) for bt in BRAND_TERMS): continue
            if any(ord(c) > 127 for c in kw): continue
            if any(ex in kw for ex in EXCLUDE_TERMS): continue
            if kw not in all_kws or vol > all_kws[kw]['volume']:
                all_kws[kw] = {'keyword': kw, 'volume': vol, 'kd': kd, 'domain': domain, 'url': url}

    filtered = {k: v for k, v in all_kws.items() if v['volume'] >= MIN_VOLUME and v['kd'] <= MAX_KD}
    print(f"  → {len(all_kws)} total → {len(filtered)} after filter", file=sys.stderr)

    # Step 3: FB Ads (top 20 keywords only to save API calls)
    sorted_kws = sorted(filtered.items(), key=lambda x: -x[1]['volume'])[:40]
    print(f"  → Querying FB Ads for top {len(sorted_kws)} keywords...", file=sys.stderr)

    results = []
    for kw, data in sorted_kws:
        coverage, dedup_src = check_coverage(kw, slugs)
        fb_count, fb_top = fetch_fb_ads(kw)
        gap = calc_gap_score(data['volume'], data['kd'], fb_count, coverage)

        results.append({
            'keyword': kw,
            'func_cn': translate(kw),
            'kd': int(data['kd']),
            'volume': data['volume'],
            'region': 'US',
            'comp_url': data['url'],
            'comp_domain': data['domain'],
            'coverage': coverage,
            'dedup_source': dedup_src,
            'fb_ads_count': fb_count,
            'fb_top_advertiser': fb_top,
            'gap_score': gap,
            'priority': priority_label(gap),
        })

    results.sort(key=lambda x: -x['gap_score'])

    # Save JSON
    today = datetime.utcnow().strftime('%Y-%m-%d')
    outpath = f'data/research_{today}.json'
    os.makedirs('data', exist_ok=True)
    with open(outpath, 'w') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"  → Saved to {outpath}", file=sys.stderr)

    # Output Slack table
    def fv(v):
        return f"{v/1000:.1f}K" if v < 10000 else f"{v/1000:.0f}K"

    print(f"{'关键词':<30} {'功能内容':<14} {'KD':<5} {'搜索量':<8} {'地区':<5} {'FB广告':<7} {'Gap分':<7} {'优先级':<7} {'覆盖状态':<12} {'竞品参考'}")
    print('─' * 140)
    for r in results:
        url_short = r['comp_domain'][:20]
        cov = '✨新' if r['coverage'] == 'new' else '✅已有'
        pri = {'high': '🔴高', 'medium': '🟡中', 'low': '🟢低'}[r['priority']]
        fb = str(r['fb_ads_count']) if r['fb_ads_count'] > 0 else '-'
        print(f"{r['keyword']:<30} {r['func_cn']:<14} {r['kd']:<5} {fv(r['volume']):<8} {r['region']:<5} {fb:<7} {r['gap_score']:<7} {pri:<7} {cov:<12} {url_short}")

    # Summary
    high = sum(1 for r in results if r['priority'] == 'high')
    med = sum(1 for r in results if r['priority'] == 'medium')
    low = sum(1 for r in results if r['priority'] == 'low')
    new = sum(1 for r in results if r['coverage'] == 'new')
    print(f"\n总计 {len(results)} 条 | 🔴高优 {high} | 🟡中优 {med} | 🟢低优 {low} | ✨新机会 {new}", file=sys.stderr)

if __name__ == '__main__':
    main()
