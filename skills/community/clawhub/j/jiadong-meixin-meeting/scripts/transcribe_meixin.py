#!/usr/bin/env python3
"""
镁信健康会议纪要转录脚本
调用阿里云百炼 Fun-ASR，完整转录会议音频
用法: python3 transcribe_meixin.py <音频文件路径> [输出目录]
"""
import sys, os, json, time, urllib.request, urllib.error

API_KEY = os.getenv("DASHSCOPE_API_KEY", "sk-46dec88b0761409dbd416405d53f73a5")
OUTPUT_DIR = sys.argv[2] if len(sys.argv) > 2 else "/workspace/memory/meetings"

def submit_task(audio_url: str) -> str:
    url = "https://dashscope.aliyuncs.com/api/v1/services/audio/asr/transcription"
    payload = {
        "model": "fun-asr",
        "input": {"file_urls": [audio_url]},
        "parameters": {"language_hints": ["zh"], "diarization_enabled": True, "speaker_count": 8}
    }
    req = urllib.request.Request(url, data=json.dumps(payload, ensure_ascii=False).encode(),
        headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json",
                 "X-DashScope-Async": "enable"}, method="POST")
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.loads(r.read())["output"]["task_id"]

def poll_result(task_id: str) -> dict:
    url = f"https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}"
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    while True:
        req = urllib.request.Request(url, headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read())
        status = data["output"]["task_status"]
        print(f"[{time.time()-start:.0f}s] {status}")
        if status == "SUCCEEDED":
            return data["output"]["results"][0]
        if status in ("FAILED", "CANCELLED"):
            raise Exception(f"转录失败: {status}")
        time.sleep(5)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python3 transcribe_meixin.py <音频文件路径> [CDN_URL]")
        sys.exit(1)

    file_path = sys.argv[1]
    cdn_url = sys.argv[2] if len(sys.argv) > 2 else None

    if not cdn_url:
        print("请提供CDN公开访问URL（通过 upload_to_cdn 工具上传后获取）")
        sys.exit(1)

    print(f"[1/3] 提交任务: {file_path}")
    start = time.time()
    task_id = submit_task(cdn_url)
    print(f"[2/3] 轮询结果，任务ID: {task_id}")
    result = poll_result(task_id)

    print(f"[3/3] 转录完成，时长: {result.get('content_duration_in_milliseconds',0)/1000:.0f}s")

    # 保存
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    name = os.path.splitext(os.path.basename(file_path))[0]
    out_txt = os.path.join(OUTPUT_DIR, f"{name}_FunASR_raw.txt")
    with open(out_txt, "w", encoding="utf-8") as f:
        f.write(result["text"])
    print(f"已保存: {out_txt}")
    print(f"\n转录字数: {len(result['text'])}字")
