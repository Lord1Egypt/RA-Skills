#!/usr/bin/env python3
"""
Memory-Inhabit TTS — 语音消息生成器（智能匹配版）

支持 edge-tts 和 MiniMax TTS，根据 SoulPod profile.json 自动匹配音色。

用法：
  python3 tts.py "要转换的文字" -o output.mp3
  python3 tts.py "要转换的文字" -o output.mp3 --provider minimax
  python3 tts.py --list-voices
"""

import asyncio
import sys
import argparse
import json
import os
import requests
from pathlib import Path

# Edge-TTS 可用性检查
try:
    import edge_tts
    EDGE_TTS_AVAILABLE = True
except ImportError:
    EDGE_TTS_AVAILABLE = False

# MiniMax TTS 配置
MINIMAX_API_URL = "https://api.minimaxi.com/v1/t2a_v2"

# ── 音色目录（从 voice_catalog.json 加载） ──────────────────────────────────
CATALOG_PATH = Path(__file__).parent / "voice_catalog.json"
_catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8")) if CATALOG_PATH.exists() else {}

# 构建 MiniMax voice_map: voice_key → voice_id
MINIMAX_VOICES = {}
if "minimax" in _catalog:
    for lang, lang_data in _catalog["minimax"].items():
        for gender_key in ("male", "female"):
            if gender_key in lang_data:
                for vk, vinfo in lang_data[gender_key].items():
                    MINIMAX_VOICES[vk] = vinfo.get("id", vk)

# Edge-TTS 中文音色 ID
EDGE_VOICES = {
    "xiaoxiao": "zh-CN-XiaoxiaoNeural",
    "xiaoyi":   "zh-CN-XiaoyiNeural",
    "yunxi":    "zh-CN-YunxiNeural",
    "yunjian":  "zh-CN-YunjianNeural",
    "yunyang":  "zh-CN-YunyangNeural",
    "yunxia":   "zh-CN-YunxiaNeural",
    "xiaobei":  "zh-CN-liaoning-XiaobeiNeural",
    "xiaoni":   "zh-CN-shaanxi-XiaoniNeural",
}

# Edge voice_key → edge voice_id（从 catalog 的 edge 节提取 key）
EDGE_VOICE_MOOD = {}
if "edge" in _catalog:
    for lang, lang_data in _catalog["edge"].items():
        for gender_key in ("male", "female", "special"):
            if gender_key in lang_data:
                for vk in lang_data[gender_key].keys():
                    EDGE_VOICE_MOOD[vk] = vk  # key 即 edge voice key

DEFAULT_MINIMAX_VOICE = "male-qn-badao"
DEFAULT_EDGE_VOICE = "yunxi"


def load_profile(persona_path=None):
    """加载 SoulPod profile.json"""
    if persona_path is None:
        # 查找最近的 persona 目录
        candidates = [
            Path(__file__).parent.parent / "personas",
            Path.home() / ".openclaw" / "workspace" / "skills" / "memory-inhabit" / "personas",
            Path.home() / ".openclaw" / "workspace-coding" / "skills" / "memory-inhabit" / "personas",
            Path.home() / ".openclaw" / "workspace-coding" / "memory-series" / "inhabit" / "personas",
            Path.home() / ".openclaw" / "workspace-roleplay" / "skills" / "memory-inhabit" / "personas",
        ]
        for cand in candidates:
            if cand.exists():
                # 找第一个有 profile.json 的子目录
                for sub in cand.iterdir():
                    if sub.is_dir() and (sub / "profile.json").exists():
                        persona_path = sub
                        break
                break
    
    if persona_path and (Path(persona_path) / "profile.json").exists():
        with open(Path(persona_path) / "profile.json") as f:
            return json.load(f)
    return {}


def load_config(persona_path=None):
    """加载 config.json"""
    if persona_path is None:
        candidates = [
            Path(__file__).parent.parent / "personas",
            Path.home() / ".openclaw" / "workspace" / "skills" / "memory-inhabit" / "personas",
            Path.home() / ".openclaw" / "workspace-coding" / "skills" / "memory-inhabit" / "personas",
            Path.home() / ".openclaw" / "workspace-coding" / "memory-series" / "inhabit" / "personas",
            Path.home() / ".openclaw" / "workspace-roleplay" / "skills" / "memory-inhabit" / "personas",
        ]
        for cand in candidates:
            if cand.exists():
                for sub in cand.iterdir():
                    if sub.is_dir() and (sub / "config.json").exists():
                        with open(sub / "config.json") as f:
                            return json.load(f)
                break
    return {}


def infer_voice(profile):
    """
    根据 profile.json 推断最优音色，返回 (minimax_key, edge_key)。
    按 gender → age_group → mood 三维查表，返回真实 catalog key。
    """
    keywords = profile.get("personality", {}).get("keywords", [])
    occupation = profile.get("occupation", "")
    gender = profile.get("gender", "male")
    age_estimate = infer_age(profile)

    # 合并关键词
    text = " ".join(keywords).lower() + " " + occupation.lower()

    # 主导情绪
    cold   = any(k in text for k in ["霸道", "冷漠", "强势", "冷酷", "严肃", "冷淡", "高冷", "独断", "腹黑", "偏执"])
    warm   = any(k in text for k in ["温柔", "善良", "体贴", "温暖", "柔和", "关怀", "善解", "宠溺"])
    sunny  = any(k in text for k in ["开朗", "阳光", "活泼", "乐观", "热情", "积极", "外向", "爽朗"])
    deep   = any(k in text for k in ["深沉", "内敛", "忧郁", "敏感", "细腻", "沉默", "克制"])
    humor  = any(k in text for k in ["幽默", "风趣", "诙谐", "搞笑", "逗比"])

    if cold:    mood = "cold"
    elif warm:  mood = "warm"
    elif sunny: mood = "sunny"
    elif deep:  mood = "deep"
    elif humor: mood = "humor"
    else:       mood = "default"

    is_female = gender.lower() in ("female", "f", "女")
    age_group = "elder" if age_estimate >= 50 else ("young" if age_estimate <= 25 else "middle")

    # MiniMax 音色表：按 (is_female, age_group, mood) → catalog key
    _mm = {
        # 男-青年
        (False, "young", "cold"):   "male-qn-badao",
        (False, "young", "warm"):   "Chinese (Mandarin)_Gentleman",
        (False, "young", "sunny"):  "Chinese (Mandarin)_Pure-hearted_Boy",
        (False, "young", "deep"):   "Chinese (Mandarin)_Lyrical_Voice",
        (False, "young", "humor"):  "Chinese (Mandarin)_Straightforward_Boy",
        (False, "young", "default"): "Chinese (Mandarin)_Gentleman",
        # 男-中年
        (False, "middle", "cold"):  "Chinese (Mandarin)_Male_Announcer",
        (False, "middle", "warm"):   "Chinese (Mandarin)_Gentleman",
        (False, "middle", "sunny"):  "Chinese (Mandarin)_Reliable_Executive",
        (False, "middle", "deep"):   "Chinese (Mandarin)_Male_Announcer",
        (False, "middle", "humor"):  "Chinese (Mandarin)_Radio_Host",
        (False, "middle", "default"): "Chinese (Mandarin)_Reliable_Executive",
        # 男-老年
        (False, "elder", "default"): "Chinese (Mandarin)_Humorous_Elder",
        (False, "elder", "humor"):   "Chinese (Mandarin)_Humorous_Elder",
        # 女-青年
        (True, "young", "cold"):    "female-yujie",
        (True, "young", "warm"):    "female-tianmei",
        (True, "young", "sunny"):   "female-shaonv",
        (True, "young", "deep"):    "Chinese (Mandarin)_Warm_Girl",
        (True, "young", "humor"):   "Chinese (Mandarin)_Crisp_Girl",
        (True, "young", "default"):  "Chinese (Mandarin)_Warm_Girl",
        # 女-中年
        (True, "middle", "cold"):   "Chinese (Mandarin)_Mature_Woman",
        (True, "middle", "warm"):   "Chinese (Mandarin)_Sweet_Lady",
        (True, "middle", "sunny"):  "female-chengshu",
        (True, "middle", "deep"):   "Chinese (Mandarin)_Wise_Women",
        (True, "middle", "humor"):  "Chinese (Mandarin)_Warm_Bestie",
        (True, "middle", "default"): "Chinese (Mandarin)_Mature_Woman",
        # 女-老年
        (True, "elder", "default"):  "Chinese (Mandarin)_Kind-hearted_Elder",
        (True, "elder", "humor"):    "Chinese (Mandarin)_Kind-hearted_Elder",
    }

    # Edge 音色表
    _edge = {
        # Edge 的 mood 映射较粗，按性别+年龄选代表性音色
        (False, "young"):  "yunxi",   # 阳光少年
        (False, "middle"): "yunjian", # 热情男声
        (False, "elder"):  "yunyang", # 专业稳重
        (True, "young"):   "xiaoyi",  # 活泼女声
        (True, "middle"):  "xiaoxiao", # 温暖女声
        (True, "elder"):   "xiaoxiao", # 温暖女声（偏成熟）
    }

    minimax_key = _mm.get((is_female, age_group, mood),
                           _mm.get((is_female, age_group, "default"),
                                   _mm.get((False, "young", "default"))))
    edge_key = _edge.get((is_female, age_group), _edge.get((False, "young")))

    return minimax_key, edge_key


def infer_voice_mood(profile):
    """兼容旧接口，推荐使用 infer_voice()"""
    minimax_key, _ = infer_voice(profile)
    return minimax_key


def infer_age(profile):
    """推断年龄阶段"""
    # 尝试从 birth_year 推断
    birth_year = profile.get("birth_year")
    if birth_year:
        try:
            age = 2026 - int(birth_year)
            if age < 25:
                return 20
            elif age < 40:
                return 30
            else:
                return 50
        except:
            pass
    
    # 从职业/身份推断
    occupation = profile.get("occupation", "")
    relation = profile.get("relation", "")
    
    # 学生/少年/年轻人
    student_keywords = ["学生", "少年", "青年", "新手", "学员"]
    # 中年/资深
    mid_keywords = ["队长", "主管", "长官", "资深", "老练"]
    # 老年
    elder_keywords = ["爷爷", "老人", "长辈"]
    
    text = occupation + relation
    for k in elder_keywords:
        if k in text:
            return 60
    for k in mid_keywords:
        if k in text:
            return 40
    for k in student_keywords:
        if k in text:
            return 20
    
    return 30  # 默认青年


def get_minimax_api_key():
    """获取 MiniMax API Key，仅从环境变量读取"""
    return os.environ.get("MINIMAX_API_KEY", "")


async def generate_edge_tts(text, output_path, voice_key, rate="+0%", volume="+0%"):
    """使用 Edge-TTS 生成语音"""
    if not EDGE_TTS_AVAILABLE:
        raise RuntimeError("edge-tts 未安装")
    
    voice_id = EDGE_VOICES.get(voice_key, EDGE_VOICES[DEFAULT_EDGE_VOICE])
    communicate = edge_tts.Communicate(text, voice_id, rate=rate, volume=volume)
    await communicate.save(output_path)
    return output_path


async def list_edge_voices():
    """列出 Edge-TTS 可用语音"""
    if not EDGE_TTS_AVAILABLE:
        print("❌ edge-tts 未安装")
        return
    
    voices = await edge_tts.list_voices()
    zh_voices = [v for v in voices if v["Locale"].startswith("zh")]
    
    print("🎤 Edge-TTS 可用中文语音：\n")
    for v in zh_voices:
        short = v["ShortName"].replace("zh-CN-", "").replace("zh-TW-", "")
        gender = "♀" if v["Gender"] == "Female" else "♂"
        styles = ", ".join(v.get("StyleList", [])) or "通用"
        print(f"  {gender} {short:<30} {styles}")


def generate_minimax_tts(text, output_path, voice_key, speed=1, pitch=0, vol=1, emotion="calm"):
    """使用 MiniMax TTS 生成语音"""
    api_key = get_minimax_api_key()
    if not api_key:
        raise RuntimeError("MiniMax API Key 未配置")
    
    voice_id = MINIMAX_VOICES.get(voice_key, MINIMAX_VOICES[DEFAULT_MINIMAX_VOICE])
    
    payload = {
        "model": "speech-2.8-hd",
        "text": text,
        "stream": False,
        "voice_setting": {
            "voice_id": voice_id,
            "speed": speed,
            "pitch": pitch,
            "vol": vol,
            "emotion": emotion,
        },
        "audio_setting": {
            "sample_rate": 32000,
            "bitrate": 128000,
            "format": "mp3",
            "channel": 1,
        },
        "output_format": "hex",
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    
    resp = requests.post(MINIMAX_API_URL, json=payload, headers=headers, timeout=30)
    resp.raise_for_status()
    
    data = resp.json()
    audio_hex = data.get("data", {}).get("audio", "")
    if not audio_hex:
        raise RuntimeError(f"MiniMax TTS 失败: {data.get('base_resp', {}).get('status_msg', 'unknown')}")
    
    audio_bytes = bytes.fromhex(audio_hex)
    with open(output_path, "wb") as f:
        f.write(audio_bytes)
    
    return output_path


def main():
    parser = argparse.ArgumentParser(description="Memory-Inhabit TTS（智能匹配版）")
    parser.add_argument("text", nargs="?", help="要转换的文字")
    parser.add_argument("-o", "--output", default="/tmp/mi_voice.mp3", help="输出文件路径")
    parser.add_argument("-p", "--provider", choices=["edge", "minimax"], default=None,
                        help="TTS 提供者（默认从 config.json 读取）")
    parser.add_argument("--voice-key", default=None, help="强制指定音色 key")
    parser.add_argument("-r", "--rate", default="+0%", help="语速调整（仅 edge）")
    parser.add_argument("--volume", default="+0%", help="音量调整（仅 edge）")
    parser.add_argument("--emotion", default="calm", help="情感（minimax：happy/sad/calm）")
    parser.add_argument("--persona", default=None, help="指定角色目录路径")
    parser.add_argument("--list-voices", action="store_true", help="列出可用音色")
    parser.add_argument("--preview", action="store_true", help="预览音色匹配结果")
    
    args = parser.parse_args()
    
    # 加载 profile 和 config
    profile = load_profile(args.persona)
    config = load_config(args.persona)
    
    if args.list_voices:
        print("📋 MiniMax 音色库：")
        for k, v in MINIMAX_VOICES.items():
            print(f"  {k}: {v}")
        print()
        if EDGE_TTS_AVAILABLE:
            asyncio.run(list_edge_voices())
        else:
            print("⚠️ Edge-TTS 未安装")
        return
    
    if args.preview:
        mood = infer_voice_mood(profile)
        age = infer_age(profile)
        mm_key, edge_key = infer_voice(profile)
        gender_label = "女" if profile.get("gender") == "female" else "男"
        print(f"👤 角色: {profile.get('name', '未知')}")
        print(f"🚻 性别: {gender_label}（自动推断）")
        print(f"📅 推断年龄阶段: {age}")
        print(f"🔊 推荐 MiniMax 音色: {mm_key} → {MINIMAX_VOICES.get(mm_key, mm_key)}")
        print(f"🔊 推荐 Edge-TTS 音色: {edge_key} → {EDGE_VOICES.get(edge_key, edge_key)}")
        return
    
    if not args.text:
        parser.print_help()
        sys.exit(1)
    
    # 确定 provider
    provider = args.provider or config.get("tts_provider", "minimax")
    
    # 确定音色 key
    if args.voice_key:
        voice_key = args.voice_key
        edge_key = args.voice_key  # 手动指定时两者相同（会 lookup 失败但 fallback）
    else:
        voice_key, edge_key = infer_voice(profile)

    try:
        if provider == "minimax":
            emotion = {"happy": "happy", "sad": "sad", "calm": "calm", "angry": "angry"}.get(args.emotion, "calm")
            generate_minimax_tts(args.text, args.output, voice_key, emotion=emotion)
            print(f"✅ MiniMax TTS 已生成: {args.output}")
            print(f"   音色: {MINIMAX_VOICES.get(voice_key, voice_key)}")
        else:
            if not EDGE_TTS_AVAILABLE:
                print("⚠️ edge-tts 未安装，切换到 minimax...")
                generate_minimax_tts(args.text, args.output, voice_key)
                print(f"✅ MiniMax TTS（备用）已生成: {args.output}")
                return
            asyncio.run(generate_edge_tts(args.text, args.output, edge_key, args.rate, args.volume))
            print(f"✅ Edge-TTS 已生成: {args.output}")
            print(f"   音色: {EDGE_VOICES.get(edge_key, edge_key)}")
    except Exception as e:
        print(f"❌ 生成失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()