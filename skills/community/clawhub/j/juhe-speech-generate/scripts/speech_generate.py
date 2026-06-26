#!/usr/bin/env python3
"""
AI语音合成脚本 — 由聚合数据 (juhe.cn) 提供数据支持
将文本内容合成为语音文件，支持多种拟人音色和多语言

用法:
    python speech_generate.py "今天天气真好！"
    python speech_generate.py --voice Kiki "你好，欢迎使用语音合成服务！"
    python speech_generate.py --voice Jennifer --language English "Hello, world!"
    python speech_generate.py --download "这段话将被保存为音频文件。"
    python speech_generate.py --output /tmp/audio.wav "指定保存位置。"
    python speech_generate.py --file my_text.txt --voice Cherry
    python speech_generate.py --list-voices

API Key 配置（任选其一，优先级从高到低）:
    1. 环境变量: export JUHE_SPEECH_KEY=your_api_key
    2. 脚本同目录的 .env 文件: JUHE_SPEECH_KEY=your_api_key
    3. 直接传参: python speech_generate.py --key your_api_key "文本内容"

免费申请 API Key: https://www.juhe.cn/docs/api/id/830
"""

import sys
import os
import json
import urllib.request
import urllib.parse
from pathlib import Path
from datetime import datetime

API_URL = "https://gpt.juhe.cn/text2speech/generate"
REGISTER_URL = "https://www.juhe.cn/docs/api/id/830"
MAX_TEXT_LEN = 500
REQUEST_TIMEOUT = 90

VOICES = {
    "Cherry":   "阳光积极、亲切自然小姐姐",
    "Ethan":    "标准普通话，阳光温暖，带部分北方口音",
    "Nofish":   "不会翘舌音的设计师",
    "Jennifer": "品牌级、电影质感般美语女声",
    "Ryan":     "节奏拉满，戏感炸裂，真实与张力共舞",
    "Katerina": "御姐音色，韵律回味十足",
    "Elias":    "学科严谨，叙事技巧将复杂知识转化为可消化的认知模块",
    "Jada":     "风风火火的沪上阿姐",
    "Dylan":    "北京胡同里长大的少年",
    "Sunny":    "甜到你心里的川妹子",
    "Li":       "耐心的瑜伽老师",
    "Marcus":   "面宽话短，心实声沉——老陕的味道",
    "Roy":      "诙谐直爽、市井活泼的台湾哥仔形象",
    "Peter":    "天津相声，专业捧哏",
    "Rocky":    "幽默风趣的阿强，在线陪聊",
    "Kiki":     "甜美的港妹闺蜜",
    "Eric":     "跳脱市井的四川成都男子",
}

LANGUAGES = {
    "Auto", "Chinese", "English", "German", "Italian",
    "Portuguese", "Spanish", "Japanese", "Korean", "French", "Russian",
}


def load_api_key(cli_key: str = None) -> str:
    if cli_key:
        return cli_key

    env_key = os.environ.get("JUHE_SPEECH_KEY", "").strip()
    if env_key:
        return env_key

    env_file = Path(__file__).parent / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("JUHE_SPEECH_KEY="):
                val = line.split("=", 1)[1].strip().strip('"').strip("'")
                if val:
                    return val

    return ""


def generate_speech(text: str, api_key: str, voice: str = "", language: str = "") -> dict:
    """调用聚合数据 API 合成语音，返回结果字典"""
    params = urllib.parse.urlencode({
        "key": api_key,
        "text": text,
        "voice": voice,
        "language": language,
    }).encode("utf-8")

    req = urllib.request.Request(
        API_URL,
        data=params,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        return {"success": False, "error": f"网络请求失败: {e}"}

    error_code = data.get("error_code", -1)
    if error_code == 0:
        result = data.get("result", {})
        return {
            "success": True,
            "orderid": result.get("orderid", ""),
            "audio_url": result.get("audio_url", ""),
        }

    reason = data.get("reason", "合成失败")
    hint = ""
    if error_code in (10001, 10002):
        hint = f"\n   请检查 API Key 是否正确，免费申请：{REGISTER_URL}"
    elif error_code == 10003:
        hint = f"\n   API Key 已过期，请前往 {REGISTER_URL} 重新申请"
    elif error_code == 10012:
        hint = "\n   今日免费调用次数已用尽，请升级套餐"
    elif error_code == 10014:
        hint = "\n   系统内部异常，请稍后重试或联系聚合数据客服"
    elif error_code == 10020:
        hint = "\n   接口维护中，请稍后重试"

    return {
        "success": False,
        "error": f"{reason}{hint}",
        "error_code": error_code,
    }


def download_audio(url: str, save_path: str) -> bool:
    """下载音频文件到本地，返回是否成功"""
    try:
        with urllib.request.urlopen(url, timeout=30) as resp:
            content = resp.read()
        Path(save_path).write_bytes(content)
        return True
    except Exception as e:
        print(f"❌ 下载失败: {e}")
        return False


def list_voices() -> None:
    print("\n可用音色列表：\n")
    print(f"  {'音色名':<12} {'风格描述'}")
    print("  " + "-" * 55)
    for name, desc in VOICES.items():
        print(f"  {name:<12} {desc}")
    print()


def parse_args(args: list) -> dict:
    result = {
        "cli_key": None,
        "text": None,
        "voice": "",
        "language": "",
        "download": False,
        "output": None,
        "file": None,
        "list_voices": False,
        "error": None,
    }

    i = 0
    positional = []

    while i < len(args):
        arg = args[i]
        if arg == "--key":
            if i + 1 < len(args):
                result["cli_key"] = args[i + 1]
                i += 2
            else:
                result["error"] = "错误: --key 后需要提供 API Key 值"
                return result
        elif arg == "--voice":
            if i + 1 < len(args):
                result["voice"] = args[i + 1]
                i += 2
            else:
                result["error"] = "错误: --voice 后需要提供音色名称（如：Cherry、Kiki）"
                return result
        elif arg == "--language":
            if i + 1 < len(args):
                result["language"] = args[i + 1]
                i += 2
            else:
                result["error"] = f"错误: --language 后需要提供语种（可选：{', '.join(sorted(LANGUAGES))}）"
                return result
        elif arg == "--output":
            if i + 1 < len(args):
                result["output"] = args[i + 1]
                result["download"] = True
                i += 2
            else:
                result["error"] = "错误: --output 后需要提供保存路径（如：/tmp/audio.wav）"
                return result
        elif arg == "--download":
            result["download"] = True
            i += 1
        elif arg == "--file":
            if i + 1 < len(args):
                result["file"] = args[i + 1]
                i += 2
            else:
                result["error"] = "错误: --file 后需要提供文件路径"
                return result
        elif arg == "--list-voices":
            result["list_voices"] = True
            i += 1
        else:
            positional.append(arg)
            i += 1

    if result["list_voices"]:
        return result

    if result["file"]:
        file_path = Path(result["file"])
        if not file_path.exists():
            result["error"] = f"错误: 文件不存在：{result['file']}"
            return result
        result["text"] = file_path.read_text(encoding="utf-8").strip()
    elif positional:
        result["text"] = " ".join(positional)
    else:
        result["error"] = (
            "错误: 需要提供要合成的文本内容\n"
            "用法: python speech_generate.py [选项] \"文本内容\"\n"
            "示例: python speech_generate.py \"今天天气真好！\"\n"
            "      python speech_generate.py --voice Kiki \"你好，欢迎使用语音合成！\"\n"
            f"\n免费申请 API Key: {REGISTER_URL}"
        )
        return result

    if result["voice"] and result["voice"] not in VOICES:
        valid = ", ".join(VOICES.keys())
        result["error"] = f"错误: 无效的音色名称 '{result['voice']}'，可用音色: {valid}"
        return result

    if result["language"] and result["language"] not in LANGUAGES:
        valid = ", ".join(sorted(LANGUAGES))
        result["error"] = f"错误: 无效的语种 '{result['language']}'，可用语种: {valid}"
        return result

    return result


def main():
    args = sys.argv[1:]

    if not args:
        print("用法: python speech_generate.py [选项] \"文本内容\"")
        print("      python speech_generate.py --file my_text.txt")
        print()
        print("示例:")
        print("  python speech_generate.py \"今天天气真好！\"")
        print("  python speech_generate.py --voice Kiki \"你好，欢迎使用聚合数据！\"")
        print("  python speech_generate.py --voice Jennifer --language English \"Hello!\"")
        print("  python speech_generate.py --download \"合成后自动下载音频\"")
        print("  python speech_generate.py --output /tmp/audio.wav \"指定保存位置\"")
        print()
        print("选项:")
        print("  --voice <名称>    音色选择（不指定则随机）")
        print("  --language <语种> 合成语种（默认 Auto 自动识别）")
        print("  --download        合成成功后自动下载音频到当前目录")
        print("  --output <路径>   合成成功后保存到指定路径")
        print("  --file <路径>     从文本文件读取合成内容")
        print("  --list-voices     列出所有可用音色")
        print()
        print(f"免费申请 API Key: {REGISTER_URL}")
        sys.exit(1)

    parsed = parse_args(args)

    if parsed["list_voices"]:
        list_voices()
        sys.exit(0)

    if parsed["error"]:
        print(parsed["error"])
        sys.exit(1)

    text = parsed["text"]
    if len(text) > MAX_TEXT_LEN:
        print(f"❌ 文本长度 {len(text)} 超出限制（最多 {MAX_TEXT_LEN} 字符），请截断后重试。")
        sys.exit(1)

    api_key = load_api_key(parsed["cli_key"])
    if not api_key:
        print("❌ 未找到 API Key，请通过以下方式之一配置：")
        print("   1. 环境变量: export JUHE_SPEECH_KEY=your_api_key")
        print("   2. .env 文件: 在脚本目录创建 .env，写入 JUHE_SPEECH_KEY=your_api_key")
        print("   3. 命令行参数: python speech_generate.py --key your_api_key \"文本内容\"")
        print(f"\n免费申请 Key: {REGISTER_URL}")
        sys.exit(1)

    voice = parsed["voice"]
    language = parsed["language"]

    voice_display = f"{voice}（{VOICES[voice]}）" if voice else "随机"
    language_display = language if language else "Auto（自动识别）"
    text_preview = text if len(text) <= 50 else text[:50] + "..."

    print(f"\n🔊 正在合成语音（接口响应可能需要 10-60 秒，请耐心等待）\n")
    print(f"   音色: {voice_display}")
    print(f"   语种: {language_display}")
    print(f"   文本: {text_preview}")
    print()

    result = generate_speech(text, api_key, voice=voice, language=language)

    if not result["success"]:
        print(f"❌ 合成失败: {result['error']}")
        sys.exit(1)

    audio_url = result["audio_url"]
    orderid = result["orderid"]

    print(f"✅ 语音合成成功！\n")
    print(f"   订单号: {orderid}")
    print(f"   音频链接（24小时内有效）:")
    print(f"   {audio_url}")
    print()

    if parsed["download"] or parsed["output"]:
        if parsed["output"]:
            save_path = parsed["output"]
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_path = f"speech_{timestamp}.wav"

        print(f"⬇️  正在下载音频到: {save_path}")
        if download_audio(audio_url, save_path):
            size_kb = Path(save_path).stat().st_size // 1024
            print(f"✅ 下载完成！文件大小: {size_kb} KB")
        else:
            print("   提示: 可手动复制上方链接在浏览器下载")
    else:
        print("   提示: 添加 --download 参数可自动下载音频文件")


if __name__ == "__main__":
    main()
