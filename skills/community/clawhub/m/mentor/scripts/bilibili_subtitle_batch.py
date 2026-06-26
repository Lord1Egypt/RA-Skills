#!/usr/bin/env python3
"""
bilibili_subtitle_batch.py — B站字幕批量提取
用法: python3 bilibili_subtitle_batch.py --bvids BV1xxx,BV2xxx --mcp-endpoint <url> --api-key <key> --output <dir>

流程: view API(无需cookie) → fetch_api player/v2(需cookie) → curl下载字幕JSON
"""

import subprocess, json, re, time, sys, os, argparse


def fetch_api_mano(url, mcp_endpoint, api_key):
    """通过 ManoBrowser fetch_api 请求（带cookie）"""
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


def extract_subtitle(bvid, mcp_endpoint, api_key, output_dir):
    """提取单个视频的字幕"""
    # Step 1: 获取 aid/cid（不需要cookie）
    r = subprocess.run([
        "curl", "-s", f"https://api.bilibili.com/x/web-interface/view?bvid={bvid}",
        "-H", "User-Agent: Mozilla/5.0",
        "-H", "Referer: https://www.bilibili.com/"
    ], capture_output=True, text=True, timeout=10)

    try:
        view = json.loads(r.stdout)
    except:
        return {"bvid": bvid, "status": "view_api_failed"}

    if view.get('code') != 0:
        return {"bvid": bvid, "status": "view_error", "message": view.get('message', '')}

    aid = view['data']['aid']
    cid = view['data']['cid']
    title = view['data']['title']

    # Step 2: 获取字幕URL（需要cookie）
    player = fetch_api_mano(
        f"https://api.bilibili.com/x/player/v2?aid={aid}&cid={cid}",
        mcp_endpoint, api_key
    )

    if not player or player.get('code') != 0:
        return {"bvid": bvid, "title": title, "status": "player_api_failed"}

    subs = player.get('data', {}).get('subtitle', {}).get('subtitles', [])
    if not subs:
        return {"bvid": bvid, "title": title, "status": "no_subtitle"}

    sub_url = "https:" + subs[0]['subtitle_url']

    # Step 3: 下载字幕
    dl = subprocess.run(["curl", "-sL", sub_url], capture_output=True, text=True, timeout=15)
    try:
        sub_data = json.loads(dl.stdout)
        lines = [item['content'] for item in sub_data['body']]
        text = '\n'.join(lines)

        # 保存
        out_file = os.path.join(output_dir, f"{bvid}.txt")
        with open(out_file, 'w', encoding='utf-8') as f:
            f.write(text)

        return {
            "bvid": bvid,
            "title": title,
            "status": "success",
            "lines": len(lines),
            "chars": len(text),
            "file": out_file
        }
    except:
        return {"bvid": bvid, "title": title, "status": "download_failed"}


def main():
    parser = argparse.ArgumentParser(description='B站字幕批量提取')
    parser.add_argument('--bvids', required=True, help='BV号列表，逗号分隔')
    parser.add_argument('--mcp-endpoint', required=True, help='ManoBrowser MCP endpoint')
    parser.add_argument('--api-key', required=True, help='ManoBrowser API key')
    parser.add_argument('--output', default='/tmp/bilibili_subs', help='输出目录')
    parser.add_argument('--delay', type=float, default=1.0, help='请求间隔秒数')
    args = parser.parse_args()

    os.makedirs(args.output, exist_ok=True)
    bvids = [b.strip() for b in args.bvids.split(',') if b.strip()]

    results = []
    for i, bvid in enumerate(bvids):
        print(f"[{i+1}/{len(bvids)}] {bvid}...", end=" ", flush=True)
        result = extract_subtitle(bvid, args.mcp_endpoint, args.api_key, args.output)
        results.append(result)

        status = result['status']
        if status == 'success':
            print(f"✅ {result.get('title','')} ({result['lines']}行)")
        else:
            print(f"❌ {status} {result.get('title','')}")

        if i < len(bvids) - 1:
            time.sleep(args.delay)

    # 汇总
    success = [r for r in results if r['status'] == 'success']
    total_lines = sum(r.get('lines', 0) for r in success)
    total_chars = sum(r.get('chars', 0) for r in success)

    print(f"\n{'='*40}")
    print(f"✅ 成功: {len(success)}/{len(bvids)}")
    print(f"📊 总计: {total_lines} 行, {total_chars} 字")

    # 保存结果
    result_file = os.path.join(args.output, '_results.json')
    with open(result_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"📁 结果保存: {result_file}")


if __name__ == '__main__':
    main()
