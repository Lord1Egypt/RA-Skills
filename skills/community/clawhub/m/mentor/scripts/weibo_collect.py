#!/usr/bin/env python3
"""
weibo_collect.py — 微博帖子批量采集
用法: python3 weibo_collect.py --uid <微博uid> --mcp-endpoint <url> --api-key <key> --pages 15 --output <dir>

通过微博移动端 API 采集公开微博内容（需 ManoBrowser fetch_api 带 cookie）
"""

import subprocess, json, re, time, sys, os, argparse


def fetch_api(url, mcp_endpoint, api_key):
    """通过 ManoBrowser fetch_api 请求"""
    payload = json.dumps({
        "jsonrpc": "2.0", "id": 1,
        "method": "tools/call",
        "params": {"name": "fetch_api", "arguments": {"url": url, "method": "GET"}}
    })
    r = subprocess.run([
        "curl", "-s", "--max-time", "15", "-X", "POST", mcp_endpoint,
        "-H", f"Authorization: Bearer {api_key}",
        "-H", "Content-Type: application/json",
        "-d", payload
    ], capture_output=True, text=True, timeout=20)

    m = re.search(r'(https://deepmining[^\s"]*\.(json|html))', r.stdout)
    if m:
        dl = subprocess.run(["curl", "-sL", m.group(1)], capture_output=True, text=True, timeout=10)
        try:
            return json.loads(dl.stdout)
        except:
            pass
    return None


def collect_weibo(uid, pages, mcp_endpoint, api_key, output_dir):
    """采集指定用户的微博"""
    os.makedirs(output_dir, exist_ok=True)
    all_posts = []

    for page in range(1, pages + 1):
        url = f"https://m.weibo.cn/api/container/getIndex?type=uid&value={uid}&containerid=107603{uid}&page={page}"
        d = fetch_api(url, mcp_endpoint, api_key)

        if not d:
            print(f"  Page {page}: fetch failed")
            continue

        cards = d.get('data', {}).get('cards', [])
        count = 0
        for card in cards:
            mblog = card.get('mblog', {})
            if mblog:
                text = re.sub(r'<[^>]+>', '', mblog.get('text', '')).strip()
                if text and len(text) > 5:
                    all_posts.append({
                        'date': mblog.get('created_at', ''),
                        'text': text,
                        'likes': mblog.get('attitudes_count', 0),
                        'comments': mblog.get('comments_count', 0),
                        'reposts': mblog.get('reposts_count', 0),
                        'is_original': mblog.get('retweeted_status') is None
                    })
                    count += 1

        print(f"  Page {page}: {count} posts", end=" | " if page < pages else "\n", flush=True)
        time.sleep(1)

    # 去重
    seen = set()
    unique = []
    for p in all_posts:
        key = p['text'][:50]
        if key not in seen:
            seen.add(key)
            unique.append(p)

    # 过滤原创+非广告
    ad_keywords = ['旗舰店', '天猫', '京东', '全球代言', '品牌代言', '品牌大使', '品牌挚友']
    personal = [p for p in unique if p.get('is_original', True)
                and not any(kw in p['text'] for kw in ad_keywords)]

    # 保存
    all_file = os.path.join(output_dir, f"weibo_{uid}_all.json")
    personal_file = os.path.join(output_dir, f"weibo_{uid}_personal.json")
    with open(all_file, 'w', encoding='utf-8') as f:
        json.dump(unique, f, ensure_ascii=False, indent=2)
    with open(personal_file, 'w', encoding='utf-8') as f:
        json.dump(personal, f, ensure_ascii=False, indent=2)

    return {
        "total": len(unique),
        "personal": len(personal),
        "all_file": all_file,
        "personal_file": personal_file
    }


def main():
    parser = argparse.ArgumentParser(description='微博帖子批量采集')
    parser.add_argument('--uid', required=True, help='微博用户 UID')
    parser.add_argument('--mcp-endpoint', required=True, help='ManoBrowser MCP endpoint')
    parser.add_argument('--api-key', required=True, help='ManoBrowser API key')
    parser.add_argument('--pages', type=int, default=15, help='采集页数（每页约10条）')
    parser.add_argument('--output', default='/tmp/weibo_collect', help='输出目录')
    args = parser.parse_args()

    print(f"📱 采集微博 UID: {args.uid}, {args.pages} 页...")
    result = collect_weibo(args.uid, args.pages, args.mcp_endpoint, args.api_key, args.output)
    print(f"\n✅ 采集完成: 总{result['total']}条, 个人原创{result['personal']}条")
    print(f"📁 {result['all_file']}")
    print(f"📁 {result['personal_file']}")


if __name__ == '__main__':
    main()
