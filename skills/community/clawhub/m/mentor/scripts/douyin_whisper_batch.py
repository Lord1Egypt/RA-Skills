#!/usr/bin/env python3
"""
douyin_whisper_batch.py — 抖音视频文字提取（Whisper 语音识别）
用法: python3 douyin_whisper_batch.py --video-ids <id1,id2,...> --mcp-endpoint <url> --api-key <key> --output <dir>

流程: ManoBrowser打开视频页 → 获取<video>播放直链 → curl下载 → ffmpeg提取音频 → Whisper转文字

前置依赖: brew install ffmpeg && pip install openai-whisper
"""

import subprocess, json, re, time, sys, os, argparse


def mcp_call(method, params, mcp_endpoint, api_key):
    """调用 ManoBrowser MCP 工具"""
    payload = json.dumps({
        "jsonrpc": "2.0", "id": 1,
        "method": "tools/call",
        "params": {"name": method, "arguments": params}
    })
    r = subprocess.run([
        "curl", "-s", "--max-time", "20", "-X", "POST", mcp_endpoint,
        "-H", f"Authorization: Bearer {api_key}",
        "-H", "Content-Type: application/json",
        "-d", payload
    ], capture_output=True, text=True, timeout=25)
    return r.stdout


def get_video_url(video_id, mcp_endpoint, api_key):
    """打开抖音视频页，获取播放直链"""
    result = mcp_call("chrome_navigate",
                      {"url": f"https://www.douyin.com/video/{video_id}"},
                      mcp_endpoint, api_key)
    tab_match = re.search(r'"tabId":(\d+)', result)
    if not tab_match:
        return None, None
    tab_id = int(tab_match.group(1))
    time.sleep(5)

    result = mcp_call("chrome_execute_script", {
        "tabId": tab_id, "world": "MAIN", "timeout": 8000,
        "jsScript": "() => { const v = document.querySelector('video'); return v ? (v.currentSrc || v.src || '') : ''; }"
    }, mcp_endpoint, api_key)

    data = json.loads(result)
    for c in data.get('result', {}).get('content', []):
        if c.get('type') == 'text' and c['text'].startswith('http'):
            return c['text'], tab_id

    return None, tab_id


def process_video(video_id, model, mcp_endpoint, api_key, output_dir):
    """处理单个视频: 下载 → 提取音频 → Whisper转写"""
    txt_file = os.path.join(output_dir, f"{video_id}.txt")
    if os.path.exists(txt_file) and os.path.getsize(txt_file) > 10:
        with open(txt_file) as f:
            text = f.read()
        return {"id": video_id, "chars": len(text), "status": "cached"}

    # 获取视频URL
    video_url, tab_id = get_video_url(video_id, mcp_endpoint, api_key)
    if not video_url:
        if tab_id:
            mcp_call("chrome_close_tabs", {"tabIds": [tab_id]}, mcp_endpoint, api_key)
        return {"id": video_id, "status": "no_url"}

    mp4_file = os.path.join(output_dir, f"{video_id}.mp4")
    mp3_file = os.path.join(output_dir, f"{video_id}.mp3")

    # 下载视频
    subprocess.run([
        "curl", "-sL", video_url, "-o", mp4_file,
        "-H", "Referer: https://www.douyin.com/",
        "-H", "User-Agent: Mozilla/5.0"
    ], capture_output=True, timeout=60)

    size = os.path.getsize(mp4_file) if os.path.exists(mp4_file) else 0
    if size < 5000:
        mcp_call("chrome_close_tabs", {"tabIds": [tab_id]}, mcp_endpoint, api_key)
        return {"id": video_id, "status": "download_failed", "size": size}

    # ffmpeg提取音频
    subprocess.run([
        "ffmpeg", "-i", mp4_file, "-vn", "-acodec", "libmp3lame", "-q:a", "4", mp3_file, "-y"
    ], capture_output=True, timeout=30)

    if os.path.exists(mp4_file):
        os.remove(mp4_file)

    if not os.path.exists(mp3_file):
        mcp_call("chrome_close_tabs", {"tabIds": [tab_id]}, mcp_endpoint, api_key)
        return {"id": video_id, "status": "ffmpeg_failed"}

    # Whisper 转写
    result = model.transcribe(mp3_file, language="zh")
    text = result['text']

    with open(txt_file, 'w', encoding='utf-8') as f:
        f.write(text)

    # 清理音频
    os.remove(mp3_file)

    # 关闭tab
    mcp_call("chrome_close_tabs", {"tabIds": [tab_id]}, mcp_endpoint, api_key)

    return {"id": video_id, "chars": len(text), "status": "success"}


def main():
    parser = argparse.ArgumentParser(description='抖音视频 Whisper 批量转写')
    parser.add_argument('--video-ids', required=True, help='视频ID列表，逗号分隔')
    parser.add_argument('--mcp-endpoint', required=True, help='ManoBrowser MCP endpoint')
    parser.add_argument('--api-key', required=True, help='ManoBrowser API key')
    parser.add_argument('--output', default='/tmp/douyin_subs', help='输出目录')
    parser.add_argument('--model', default='base', choices=['base', 'medium', 'large'], help='Whisper模型')
    args = parser.parse_args()

    os.makedirs(args.output, exist_ok=True)
    video_ids = [v.strip() for v in args.video_ids.split(',') if v.strip()]

    print(f"🔄 加载 Whisper 模型 ({args.model})...")
    import whisper
    model = whisper.load_model(args.model)
    print("✅ 模型加载完成")

    results = []
    for i, vid in enumerate(video_ids):
        print(f"[{i+1}/{len(video_ids)}] {vid}...", end=" ", flush=True)
        result = process_video(vid, model, args.mcp_endpoint, args.api_key, args.output)
        results.append(result)

        if result['status'] == 'success':
            print(f"✅ {result['chars']} 字")
        elif result['status'] == 'cached':
            print(f"⏭️ 已有 ({result['chars']} 字)")
        else:
            print(f"❌ {result['status']}")

        time.sleep(1)

    success = [r for r in results if r['status'] in ('success', 'cached')]
    total_chars = sum(r.get('chars', 0) for r in success)
    print(f"\n✅ 成功: {len(success)}/{len(video_ids)}, 总字数: {total_chars}")

    result_file = os.path.join(args.output, '_results.json')
    with open(result_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    main()
