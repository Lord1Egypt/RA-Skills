#!/usr/bin/env python3
"""
SEO Pipeline — Semrush + Sitemap + Notion dedup
Integrates with the omni-channel selection agent.
"""

import sys, os, csv, io, json, re, urllib.request, urllib.parse
from datetime import datetime, timezone

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_DIR)
OUTPUT_DIR = os.path.join(PROJECT_DIR, "output")

# ─── Config ───
SEMRUSH_KEY = os.environ.get('SEMRUSH_API_KEY', '')
NOTION_TOKEN = os.environ.get('NOTION_IMAGE_BOT_TOKEN', '') or os.environ.get('NOTION_API_KEY', '')

COMPETITORS = [
    'fotor.com', 'kaze.ai', 'remaker.ai', 'aragon.ai',
    'picsart.com', 'mangoanimate.com', 'higgsfield.ai',
    'photoroom.com', 'remini.ai', 'faceapp.com', 'cutout.pro'
]
SITEMAP_URL = 'https://art.myshell.ai/sitemap.xml'
BASE44_API = 'https://app.base44.com/api'

# Filter thresholds from doc
MIN_VOLUME = 500
MAX_KD = 65

BRAND_TERMS = [
    'photoroom', 'remini', 'fotor', 'picsart', 'faceapp', 'cutout',
    'pixlr', 'photo room', 'pics art', 'kaze', 'remaker', 'aragon',
    'mangoanimate', 'higgsfield'
]
EXCLUDE_TERMS = ['font', 'text generator', 'cursive', 'bold text', 'fancy text',
                 'copy and paste', 'copy paste', 'ai writer', 'fonts']

TRANSLATIONS = {
    'background remover': '背景移除', 'remove background': '背景移除',
    'white background': '白色背景生成', 'blue background': '蓝色背景生成',
    'transparent background': '透明背景生成', 'png maker': 'PNG透明图制作',
    'unblur image': '图片去模糊', 'image quality enhancer': '图片质量增强',
    'photo enhancer': '照片增强', 'image enhancer': '图片增强工具',
    'remove object from image': '移除图片物体', 'ai remover': 'AI物体移除',
    'face swap': '换脸', 'photo editor': '照片编辑器',
    'passport photo': '证件照制作', 'ai photo': 'AI照片',
    'ai filter': 'AI滤镜', 'face filter': '面部滤镜',
    'ai art': 'AI艺术', 'ai generator': 'AI生成器',
    'ai image': 'AI图片', 'braces filter': '牙套滤镜',
    'ai image extender': '扩图工具', 'image upscaler': '图片放大',
    'ai portrait': 'AI肖像', 'ai headshot': 'AI证件照',
    'ai avatar': 'AI头像', 'ai baby': 'AI宝宝预测',
    'ai aging': 'AI变老', 'ai hairstyle': 'AI发型',
}


def _load_env():
    bashrc = os.path.expanduser("~/.bashrc")
    if os.path.exists(bashrc):
        with open(bashrc) as f:
            for line in f:
                line = line.strip()
                if line.startswith("export "):
                    line = line[7:]
                for key in ["SEMRUSH_API_KEY", "NOTION_API_KEY", "NOTION_IMAGE_BOT_TOKEN"]:
                    if line.startswith(f"{key}=") and not os.environ.get(key):
                        val = line.split("=", 1)[1].strip().strip('"').strip("'")
                        os.environ[key] = val

_load_env()
SEMRUSH_KEY = os.environ.get('SEMRUSH_API_KEY', '')
NOTION_TOKEN = os.environ.get('NOTION_IMAGE_BOT_TOKEN', '') or os.environ.get('NOTION_API_KEY', '')


def fetch_sitemap() -> set:
    """Fetch art.myshell.ai sitemap and extract URL slugs."""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (compatible; MyShellBot/1.0)'}
        req = urllib.request.Request(SITEMAP_URL, headers=headers)
        resp = urllib.request.urlopen(req, timeout=15)
        index_xml = resp.read().decode()
        sub_urls = re.findall(r'<loc>(https://art\.myshell\.ai/[^\s<]+\.xml)</loc>', index_xml)
        slugs = set()
        for sub_url in sub_urls[:2]:  # EN + first locale
            try:
                req2 = urllib.request.Request(sub_url, headers=headers)
                resp2 = urllib.request.urlopen(req2, timeout=15)
                xml = resp2.read().decode()
                urls = re.findall(r'<loc>(https://art\.myshell\.ai/[^<]+)</loc>', xml)
                for u in urls:
                    path = u.replace('https://art.myshell.ai/', '').lower().strip('/')
                    if path:
                        slugs.add(path)
                        parts = path.split('/')
                        if len(parts) > 1:
                            slugs.add(parts[-1])
            except:
                pass
        print(f"[SEO] Sitemap: {len(slugs)} pages found")
        return slugs
    except Exception as e:
        print(f"[SEO] Sitemap fetch failed: {e}")
        return set()


def fetch_semrush_keywords(domain: str, database: str = 'us', limit: int = 50) -> list:
    """Fetch organic keywords from Semrush API."""
    if not SEMRUSH_KEY:
        print(f"[SEO] No SEMRUSH_API_KEY, skipping {domain}")
        return []
    url = (f"https://api.semrush.com/?type=domain_organic&key={SEMRUSH_KEY}"
           f"&display_limit={limit}&export_columns=Ph,Po,Nq,Cp,Co,Kd,Tr,Tc,Ur"
           f"&domain={domain}&database={database}")
    try:
        resp = urllib.request.urlopen(url, timeout=20)
        text = resp.read().decode()
        if 'ERROR' in text[:100]:
            print(f"[SEO] Semrush error for {domain}: {text[:100]}")
            return []
        rows = list(csv.DictReader(io.StringIO(text), delimiter=';'))
        return rows
    except Exception as e:
        print(f"[SEO] Semrush fetch error for {domain}: {e}")
        return []


def fetch_notion_bots() -> set:
    """Fetch bot names from Notion Bot Database for dedup."""
    if not NOTION_TOKEN:
        return set()
    # The Notion Bot Database ID from the requirements doc
    db_id = "1113f81ff51e802f8056d66c76a9f9e6"
    url = f"https://api.notion.com/v1/databases/{db_id}/query"
    try:
        data = json.dumps({"page_size": 100}).encode()
        req = urllib.request.Request(url, data=data, method="POST", headers={
            "Authorization": f"Bearer {NOTION_TOKEN}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json",
        })
        with urllib.request.urlopen(req, timeout=15) as resp:
            result = json.loads(resp.read().decode())
        
        bot_names = set()
        for page in result.get("results", []):
            props = page.get("properties", {})
            # Try common name fields
            for key in ["Bot_Name", "Name", "name", "Title", "title"]:
                if key in props:
                    prop = props[key]
                    if prop.get("type") == "title":
                        for t in prop.get("title", []):
                            name = t.get("plain_text", "").lower()
                            if name:
                                bot_names.add(name)
                    elif prop.get("type") == "rich_text":
                        for t in prop.get("rich_text", []):
                            name = t.get("plain_text", "").lower()
                            if name:
                                bot_names.add(name)
        print(f"[SEO] Notion bots: {len(bot_names)} found")
        return bot_names
    except Exception as e:
        print(f"[SEO] Notion fetch failed: {e}")
        return set()


def translate_keyword(kw: str) -> str:
    kw_lower = kw.lower()
    if kw_lower in TRANSLATIONS:
        return TRANSLATIONS[kw_lower]
    for k, v in TRANSLATIONS.items():
        if k in kw_lower or kw_lower in k:
            return v
    return kw


def check_coverage(kw: str, sitemap_slugs: set, notion_bots: set) -> tuple:
    """Check coverage status across all dedup sources."""
    kw_slug = kw.lower().replace(' ', '-')
    kw_words = set(kw.lower().split())
    
    # Check sitemap
    for slug in sitemap_slugs:
        slug_kw = slug.split('/')[-1].replace('-', ' ').lower()
        if kw_slug in slug or slug_kw == kw.lower() or kw.lower() in slug_kw:
            return 'exists_sitemap', f'Sitemap: {slug}'
    
    # Check Notion bots
    for bot in notion_bots:
        if kw.lower() in bot or bot in kw.lower():
            return 'exists_notion', f'Notion: {bot}'
    
    return 'new', ''


def run_seo_pipeline(competitors: list = None, database: str = 'us', limit: int = 50) -> list:
    """Run the full SEO pipeline: Semrush → filter → dedup → score."""
    if competitors is None:
        competitors = COMPETITORS
    
    print(f"\n[SEO] Starting pipeline for {len(competitors)} competitors...")
    
    # Step 1: Fetch sitemap
    sitemap_slugs = fetch_sitemap()
    
    # Step 2: Fetch Notion bots
    notion_bots = fetch_notion_bots()
    
    # Step 3: Fetch Semrush keywords
    all_kws = {}
    for domain in competitors:
        rows = fetch_semrush_keywords(domain, database, limit)
        print(f"[SEO] {domain}: {len(rows)} keywords")
        for row in rows:
            kw = row.get('Keyword', '').strip().lower()
            if not kw:
                continue
            vol = int(row.get('Search Volume', '0') or '0')
            kd = float(row.get('Keyword Difficulty', '0') or '0')
            url = row.get('Url', '')
            
            # Skip brand terms
            if any(kw == bt or kw.startswith(bt + ' ') or kw.endswith(' ' + bt) for bt in BRAND_TERMS):
                continue
            # Skip non-ASCII
            if any(ord(c) > 127 for c in kw):
                continue
            # Skip excluded terms
            if any(ex in kw for ex in EXCLUDE_TERMS):
                continue
            
            if kw not in all_kws or vol > all_kws[kw]['volume']:
                all_kws[kw] = {
                    'keyword': kw, 'volume': vol, 'kd': kd,
                    'domain': domain, 'url': url
                }
    
    print(f"[SEO] Total unique keywords: {len(all_kws)}")
    
    # Step 4: Filter
    filtered = {k: v for k, v in all_kws.items()
                if v['volume'] >= MIN_VOLUME and v['kd'] <= MAX_KD}
    print(f"[SEO] After filter (Vol>{MIN_VOLUME}, KD<{MAX_KD}): {len(filtered)}")
    
    # Step 5: Dedup and score
    results = []
    for kw, data in sorted(filtered.items(), key=lambda x: -x[1]['volume']):
        coverage, note = check_coverage(kw, sitemap_slugs, notion_bots)
        results.append({
            'keyword': kw,
            'func_cn': translate_keyword(kw),
            'kd': int(data['kd']),
            'volume': data['volume'],
            'region': database.upper(),
            'comp_url': data['url'],
            'comp_domain': data['domain'],
            'coverage': coverage,
            'note': note,
        })
    
    # Annotate coverage labels
    for r in results:
        if r['coverage'] == 'new':
            r['coverage_label'] = '✨新机会'
        elif r['coverage'] == 'exists_sitemap':
            r['coverage_label'] = '✅已有覆盖'
        elif r['coverage'] == 'exists_notion':
            r['coverage_label'] = '🔄需优化'
        else:
            r['coverage_label'] = '❓未知'
    
    print(f"[SEO] Results: {len(results)} keywords")
    new_count = sum(1 for r in results if r['coverage'] == 'new')
    print(f"[SEO] ✨New: {new_count} | ✅Covered: {len(results) - new_count}")
    
    return results


def format_seo_slack_report(results: list) -> str:
    """Format SEO results as Slack code block matching doc template."""
    def fv(v):
        if v >= 10000: return f"{v/1000:.0f}K"
        if v >= 1000: return f"{v/1000:.1f}K"
        return str(v)
    
    lines = []
    lines.append(f"🔍 *SEO 竞品关键词调研 — {datetime.now(timezone.utc).strftime('%Y-%m-%d')}*")
    lines.append(f"📊 竞品: {', '.join(COMPETITORS[:5])}... | 筛选: Volume>{MIN_VOLUME}, KD<{MAX_KD}\n")
    lines.append("```")
    lines.append(f" #  {'关键词':<26s}  {'功能内容':<12s}  {'KD':>4s}  {'搜索量':>7s}  {'地区':>4s}  {'竞品参考':<25s}  {'覆盖状态'}")
    lines.append("─" * 100)
    
    for i, r in enumerate(results[:30], 1):
        kw = r['keyword'][:24]
        func = r['func_cn'][:10]
        comp = r['comp_domain'][:23]
        cov = r['coverage_label']
        lines.append(
            f"{i:>2d}  {kw:<26s}  {func:<12s}  {r['kd']:>4d}  {fv(r['volume']):>7s}  {r['region']:>4s}  {comp:<25s}  {cov}"
        )
    
    lines.append("```")
    
    new = sum(1 for r in results if r['coverage'] == 'new')
    total = len(results)
    lines.append(f"\n📊 总计 {total} 条 | ✨新机会 {new} | ✅已覆盖 {total - new}")
    
    return "\n".join(lines)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--database", default="us")
    parser.add_argument("--limit", type=int, default=50)
    args = parser.parse_args()
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    results = run_seo_pipeline(database=args.database, limit=args.limit)
    
    # Save
    ts = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M')
    with open(os.path.join(OUTPUT_DIR, f"seo_{ts}.json"), "w") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    # Print Slack report
    report = format_seo_slack_report(results)
    print(report)
    
    with open(os.path.join(OUTPUT_DIR, f"seo_report_{ts}.txt"), "w") as f:
        f.write(report)
