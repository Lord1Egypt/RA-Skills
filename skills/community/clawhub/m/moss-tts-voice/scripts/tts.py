import requests, base64, argparse, os, json, subprocess, sys, time

# 不同渠道推荐格式 (飞书需要 opus/ogg 才能显示为语音消息)
CHANNEL_FORMATS = {
    "feishu": "ogg",   # opus 编码的 ogg → 飞书语音消息
    "discord": "mp3", 
    "telegram": "ogg", # opus 编码
    "whatsapp": "ogg",
    "signal": "mp3",
    "slack": "mp3",
    "default": "mp3"
}

def convert_audio(input_file, output_file, target_format):
    """使用 ffmpeg 转换音频格式"""
    try:
        if target_format == "ogg":
            cmd = ["ffmpeg", "-y", "-i", input_file, "-c:a", "libopus", "-b:a", "64k", output_file]
        else:
            cmd = ["ffmpeg", "-y", "-i", input_file, "-c:a", "libmp3lame", "-q:a", "2", output_file]
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False

def tts():
    parser = argparse.ArgumentParser(description="MOSS-TTS 语音合成")
    parser.add_argument("--text", required=True, help="待合成的文本")
    parser.add_argument("--voice_id", default=None, help="音色ID（预注册的）")
    parser.add_argument("--reference_audio", default=None, help="参考音频路径（实时克隆）")
    parser.add_argument("--output", default=None, help="输出文件路径 (可选)")
    parser.add_argument("--channel", default=None, help="目标渠道: feishu, discord, telegram, whatsapp, signal, slack")
    parser.add_argument("--target", default=None, help="发送目标 (用户ID/频道ID，可选)")
    parser.add_argument("--format", default=None, help="输出格式: mp3, ogg, wav (可选，默认根据 channel 自动选择)")
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式结果")
    args = parser.parse_args()

    api_key = os.getenv("MOSS_API_KEY")
    if not api_key:
        result = {"error": "MOSS_API_KEY 环境变量未设置"}
        print(json.dumps(result) if args.json else f"Error: {result['error']}")
        sys.exit(1)

    # 必须提供 voice_id 或 reference_audio
    if not args.voice_id and not args.reference_audio:
        result = {"error": "必须提供 --voice_id 或 --reference_audio 参数"}
        print(json.dumps(result) if args.json else f"Error: {result['error']}")
        sys.exit(1)

    # 确定输出格式
    target_format = args.format
    if not target_format and args.channel:
        target_format = CHANNEL_FORMATS.get(args.channel, CHANNEL_FORMATS["default"])
    if not target_format:
        target_format = "wav"
    
    # 确定输出路径
    if args.output:
        output_file = args.output
    else:
        tmp_dir = "/tmp/openclaw/moss-tts"
        # 检测 /tmp 目录是否可写
        try:
            test_file = "/tmp/.openclaw_write_test"
            with open(test_file, "w") as f:
                f.write("test")
            os.remove(test_file)
        except (PermissionError, OSError) as e:
            result = {"error": f"/tmp 目录无写入权限: {e}"}
            print(json.dumps(result) if args.json else f"Error: {result['error']}")
            sys.exit(1)
        os.makedirs(tmp_dir, exist_ok=True)
        output_file = f"{tmp_dir}/voice-{int(time.time()*1000)}.{target_format}"

    # 构建请求
    url = "https://studio.mosi.cn/v1/audio/tts"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {
        "model": "moss-tts",
        "text": args.text,
    }
    
    if args.voice_id:
        payload["voice_id"] = args.voice_id
    elif args.reference_audio:
        with open(args.reference_audio, "rb") as f:
            payload["reference_audio"] = base64.b64encode(f.read()).decode("utf-8")

    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=60)
        data = resp.json()
    except Exception as e:
        result = {"error": f"API 请求失败: {e}"}
        print(json.dumps(result) if args.json else f"Error: {result['error']}")
        sys.exit(1)

    if "audio_data" not in data:
        result = {"error": data.get("error", data.get("message", str(data)))}
        print(json.dumps(result) if args.json else f"Error: {result['error']}")
        sys.exit(1)

    # 保存原始 WAV
    raw_output = output_file if target_format == "wav" else output_file.replace(f".{target_format}", ".wav")
    with open(raw_output, "wb") as f:
        f.write(base64.b64decode(data["audio_data"]))

    # 格式转换
    if target_format != "wav":
        if convert_audio(raw_output, output_file, target_format):
            os.remove(raw_output)
        else:
            output_file = raw_output
            target_format = "wav"

    # 输出结果
    result = {
        "success": True,
        "file": output_file,
        "format": target_format,
        "channel": args.channel,
        "target": args.target
    }
    
    if args.json:
        print(json.dumps(result))
    else:
        print(f"✅ 音频已生成: {output_file}")
        if args.channel:
            print(f"   渠道: {args.channel}")
        if args.target:
            print(f"   目标: {args.target}")

if __name__ == "__main__":
    tts()
