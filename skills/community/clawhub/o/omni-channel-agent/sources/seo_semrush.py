#!/usr/bin/env python3
"""
SEO 竞品关键词调研脚本 — 全渠道选品 Agent
数据源: Semrush API + art.myshell.ai sitemap 去重

用法: SEMRUSH_API_KEY=xxx python3 scripts/seo_research.py [--output data/results.json]
"""
import csv, io, json, os, sys, urllib.request, argparse

SEMRUSH_KEY = os.environ.get('SEMRUSH_API_KEY', '')
COMPETITORS = ['photoroom.com', 'remini.ai', 'fotor.com', 'picsart.com', 'faceapp.com', 'cutout.pro']
SITEMAP_URL = 'https://art.myshell.ai/sitemap.xml'

# Brand terms to exclude
BRAND_TERMS = ['photoroom', 'remini', 'fotor', 'picsart', 'faceapp', 'cutout', 'pixlr',
               'photo room', 'pics art', 'pix art', 'cut pit', 'remin', 'fotorom']
# Non-core categories to exclude
EXCLUDE_TERMS = ['font', 'text generator', 'cursive', 'bold text', 'fancy text',
                 'copy and paste', 'copy paste', 'ai writer']

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
    'passport photo': '证件照制作', 'photo editor': '照片编辑器',
    'face editing': '脸部编辑', 'facial filter': '面部滤镜',
}

def fetch_sitemap():
    """Fetch sitemap and extract slugs for dedup."""
    try:
        resp = urllib.request.urlopen(SITEMAP_URL, timeout=10)
        index_xml = resp.read().decode()
        # Get sub-sitemaps
        import re
        sub_urls = re.findall(r'<loc>(https://art\.myshell\.ai/\w+page\.xml)</loc>', index_xml)
        slugs = set()
        for sub_url in sub_urls[:1]:  # Only EN for now
            resp2 = urllib.request.urlopen(sub_url, timeout=10)
            xml = resp2.read().decode()
            urls = re.findall(r'<loc>(https://art\.myshell\.ai/[^<]+)</loc>', xml)
            for u in urls:
                path = u.replace('https://art.myshell.ai/', '')
                if path:
                    slugs.add(path.lower())
                    # Also add last segment
                    parts = path.split('/')
                    if len(parts) > 1:
                        slugs.add(parts[-1].lower())
        return slugs
    except Exception as e:
        print(f"Warning: sitemap fetch failed: {e}", file=sys.stderr)
        return set()

def fetch_competitor_keywords(domain, database='us', limit=40):
    """Fetch organic keywords from Semrush."""
    if not SEMRUSH_KEY:
        print(f"Warning: no SEMRUSH_API_KEY, skipping {domain}", file=sys.stderr)
        return []
    url = (f"https://api.semrush.com/?type=domain_organic&key={SEMRUSH_KEY}"
           f"&display_limit={limit}&export_columns=Ph,Po,Nq,Cp,Co,Kd,Tr,Tc,Ur"
           f"&domain={domain}&database={database}")
    try:
        resp = urllib.request.urlopen(url, timeout=15)
        text = resp.read().decode()
        if 'ERROR' in text:
            return []
        reader = csv.DictReader(io.StringIO(text), delimiter=';')
        return list(reader)
    except Exception as e:
        print(f"Error fetching {domain}: {e}", file=sys.stderr)
        return []

def translate_keyword(kw):
    """Translate keyword to Chinese function description."""
    if kw in TRANSLATIONS:
        return TRANSLATIONS[kw]
    for k, v in TRANSLATIONS.items():
        if k in kw or kw in k:
            return v
    return kw

def check_coverage(kw, sitemap_slugs):
    """Check if keyword is already covered in sitemap."""
    kw_slug = kw.lower().replace(' ', '-')
    for slug in sitemap_slugs:
        slug_kw = slug.split('/')[-1].replace('-', ' ').lower()
        if kw_slug in slug or slug_kw == kw or kw in slug_kw or slug_kw in kw:
            return True, slug
    return False, ''

def main():
    parser = argparse.ArgumentParser(description='SEO Competitor Keyword Research')
    parser.add_argument('--output', '-o', default='data/seo_research_latest.json')
    parser.add_argument('--database', default='us')
    parser.add_argument('--min-volume', type=int, default=1000)
    parser.add_argument('--max-kd', type=int, default=80)
    parser.add_argument('--limit', type=int, default=40)
    args = parser.parse_args()

    print("Fetching sitemap for dedup...")
    sitemap_slugs = fetch_sitemap()
    print(f"  → {len(sitemap_slugs)} pages found")

    print("Fetching competitor keywords...")
    all_kws = {}
    for domain in COMPETITORS:
        rows = fetch_competitor_keywords(domain, args.database, args.limit)
        print(f"  → {domain}: {len(rows)} keywords")
        for row in rows:
            kw = row.get('Keyword', '').strip().lower()
            if not kw:
                continue
            vol = int(row.get('Search Volume', '0') or '0')
            kd = float(row.get('Keyword Difficulty', '0') or '0')
            url = row.get('Url', '')
            if any(kw == bt or kw.startswith(bt + ' ') for bt in BRAND_TERMS):
                continue
            if any(ord(c) > 127 for c in kw):
                continue
            if any(ex in kw for ex in EXCLUDE_TERMS):
                continue
            if kw not in all_kws or vol > all_kws[kw]['volume']:
                all_kws[kw] = {'keyword': kw, 'volume': vol, 'kd': kd, 'domain': domain, 'url': url}

    # Filter
    filtered = {k: v for k, v in all_kws.items() if v['volume'] >= args.min_volume and v['kd'] <= args.max_kd}

    # Dedup and format
    results = []
    for kw, data in sorted(filtered.items(), key=lambda x: -x[1]['volume']):
        covered, slug = check_coverage(kw, sitemap_slugs)
        results.append({
            'keyword': kw,
            'func': translate_keyword(kw),
            'kd': int(data['kd']),
            'volume': data['volume'],
            'region': args.database.upper(),
            'comp_url': data['url'],
            'coverage': '✅已覆盖' if covered else '✨新机会',
            'note': f'Sitemap: {slug}' if covered else '',
        })

    # Save
    os.makedirs(os.path.dirname(args.output) or '.', exist_ok=True)
    with open(args.output, 'w') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    # Print summary
    new = sum(1 for r in results if '新机会' in r['coverage'])
    covered = sum(1 for r in results if '已覆盖' in r['coverage'])
    print(f"\nResults: {len(results)} keywords | ✨New: {new} | ✅Covered: {covered}")
    print(f"Saved to {args.output}")

if __name__ == '__main__':
    main()
