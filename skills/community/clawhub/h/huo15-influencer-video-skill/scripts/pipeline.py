"""火15 带货视频 v2 — 端到端 pipeline

输入：剧本 JSON（参见 examples/script_demo.json）
输出：带配音 + BGM + 可选字幕的成片 mp4

流程：
  1. 拼接剧本 → TTS 生成 voice.mp3 + 时长 D
  2. 视频时长 = clamp(ceil(D)+1, 4, 15)
  3. 调 Seedance 生成无声视频
  4. voice + BGM → mix.mp3（BGM 自动循环、降音量、淡出）
  5. 视频 + mix.mp3 → muxer
  6. 可选：按剧本行长度比例生成 SRT，再烧录字幕
  7. 输出 final.mp4
"""

import os
import sys
import json
import math
import time
import base64
import subprocess
from pathlib import Path
from typing import Optional

import requests

# 同级 import
sys.path.insert(0, str(Path(__file__).resolve().parent))
from templates import get_template, suggest_template, list_templates  # noqa: E402
from tts import synthesize  # noqa: E402
from bgm import mix_audio, mux_video_audio  # noqa: E402


ARK_API_KEY = os.environ.get("ARK_API_KEY", "")
ARK_BASE = "https://ark.cn-beijing.volces.com/api/v3"
ARK_MODEL = "doubao-seedance-2-0-260128"


# ---------- 辅助 ----------

def _build_prompt(tpl: dict) -> str:
    return (
        f"第一人称视角带货短视频。{tpl['character']}，手持图片中的产品，"
        f"{tpl['action']}。{tpl['scene']}。"
    )


def estimate_cost(duration: int) -> tuple:
    """(tokens, ¥)"""
    tokens = duration * 720 * 1280 * 24 / 1024
    return int(tokens), round(tokens * 46 / 1_000_000, 2)


def _video_duration_for(voice_seconds: float) -> int:
    """语音 D 秒 → 视频时长（4~15 秒，留 1 秒余量给开头铺垫）"""
    return max(4, min(15, math.ceil(voice_seconds) + 1))


# ---------- Seedance 调用 ----------

def _generate_silent_video(image_path: str,
                           prompt: str,
                           duration: int,
                           output: str) -> str:
    """调 Seedance 生成无声视频"""
    assert ARK_API_KEY, "请先设置 ARK_API_KEY"
    with open(image_path, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode()
    ext = Path(image_path).suffix.lstrip(".").lower()
    if ext == "jpg":
        ext = "jpeg"

    body = {
        "model": ARK_MODEL,
        "content": [
            {"type": "text", "text": prompt},
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/{ext};base64,{img_b64}"},
                "role": "reference_image",
            },
        ],
        "ratio": "9:16",
        "duration": duration,
        "watermark": False,
    }
    headers = {
        "Authorization": f"Bearer {ARK_API_KEY}",
        "Content-Type": "application/json",
    }

    r = requests.post(f"{ARK_BASE}/contents/generations/tasks",
                      headers=headers, json=body, timeout=60)
    res = r.json()
    if "id" not in res:
        raise RuntimeError(f"Seedance 提交失败: {res}")
    task_id = res["id"]
    print(f"[seedance] task_id={task_id}, 时长={duration}s")

    for _ in range(120):  # 最多 20 分钟
        time.sleep(10)
        d = requests.get(f"{ARK_BASE}/contents/generations/tasks/{task_id}",
                         headers=headers, timeout=30).json()
        st = d.get("status")
        print(f"  [{time.strftime('%H:%M:%S')}] {st}")
        if st == "succeeded":
            video_url = d["content"]["video_url"]
            with requests.get(video_url, stream=True, timeout=120) as vr:
                with open(output, "wb") as f:
                    for chunk in vr.iter_content(8192):
                        f.write(chunk)
            tokens = d.get("usage", {}).get("total_tokens", 0)
            print(f"[seedance] ok → {output} ({os.path.getsize(output)/1e6:.1f}MB) "
                  f"tokens={tokens} ¥{tokens*46/1e6:.2f}")
            return output
        if st == "failed":
            raise RuntimeError(f"Seedance 任务失败: {d}")
    raise TimeoutError("Seedance 超时（20 分钟）")


# ---------- 字幕（SRT） ----------

def _build_srt(lines: list, total_duration: float) -> str:
    """按行字数比例切时间轴，生成 SRT"""
    weights = [max(1, len(l["text"])) for l in lines]
    total_w = sum(weights)
    cur = 0.0
    parts = []
    for i, (line, w) in enumerate(zip(lines, weights), 1):
        seg = total_duration * w / total_w
        start, end = cur, cur + seg
        cur = end
        parts.append(
            f"{i}\n{_fmt_ts(start)} --> {_fmt_ts(end)}\n{line['text']}\n"
        )
    return "\n".join(parts)


def _fmt_ts(t: float) -> str:
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = t % 60
    return f"{h:02d}:{m:02d}:{int(s):02d},{int((s - int(s)) * 1000):03d}"


def _burn_subtitles(video_in: str, srt_path: str, video_out: str,
                    font: str = "PingFang SC", size: int = 14) -> str:
    """用 ffmpeg subtitles 滤镜烧录字幕"""
    style = (f"FontName={font},FontSize={size},PrimaryColour=&H00FFFFFF,"
             f"OutlineColour=&H80000000,BorderStyle=1,Outline=2,Shadow=0,"
             f"Alignment=2,MarginV=80")
    # subtitles 滤镜里 : , = 都要转义
    safe_srt = srt_path.replace(":", "\\:").replace(",", "\\,")
    cmd = [
        "ffmpeg", "-y", "-i", video_in,
        "-vf", f"subtitles={safe_srt}:force_style='{style}'",
        "-c:a", "copy",
        video_out,
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    return video_out


# ---------- 主流程 ----------

def render(script: dict, work_dir: str = "/tmp/huo15_video", dry_run: bool = False) -> dict:
    """
    script schema:
      {
        "template": "traditional_lady",        # 必填，或用 "auto" + category
        "category": "茶叶",                    # template=="auto" 时启用
        "image": "/path/to/product.jpg",       # 必填（dry_run=True 时可不存在）
        "lines": [{"text": "...", "action": "..."}],  # 必填，至少 1 条
        "bgm": "warm" | "/path/file.mp3" | null,
        "bgm_volume": 0.20,                    # 可覆盖模板默认
        "subtitle": true,                      # 默认 true
        "voice_override": "zh-CN-XxxNeural",   # 可覆盖模板默认音色
        "rate_override": "+0%",
        "output": "/tmp/final.mp4"
      }

    dry_run=True：跳过 Seedance 调用（省钱），只跑 TTS + SRT，
                  返回预估 token / ¥ / 视频时长，方便测剧本节奏。
    """
    Path(work_dir).mkdir(parents=True, exist_ok=True)

    # 1. 选模板
    tpl_key = script.get("template", "traditional_lady")
    if tpl_key == "auto":
        tpl_key = suggest_template(script.get("category", ""))
    tpl = get_template(tpl_key)
    print(f"[模板] {tpl_key} — {tpl['label']}")

    # 2. 拼台词 + TTS
    full_text = "，".join(l["text"].strip("。.！!？?") for l in script["lines"]) + "。"
    voice_id = script.get("voice_override") or tpl["voice"]
    rate = script.get("rate_override") or tpl["voice_rate"]
    voice = synthesize(
        full_text, voice=voice_id, rate=rate,
        pitch=tpl["voice_pitch"],
        output=f"{work_dir}/voice.mp3",
    )
    print(f"[配音] {voice['engine']} | {voice_id} | {voice['duration']:.2f}s")

    if voice["duration"] > 14.5:
        raise ValueError(
            f"剧本配音 {voice['duration']:.1f}s 超过单段 15s 上限，请精简台词"
            f"（约 50~70 字）"
        )

    # 3. 算视频时长 + 改 prompt 加入第一句动作
    duration = _video_duration_for(voice["duration"])
    if script["lines"][0].get("action"):
        tpl = {**tpl, "action": script["lines"][0]["action"]}
    prompt = _build_prompt(tpl)
    print(f"[视频] 时长={duration}s, prompt={prompt}")

    tokens, yuan = estimate_cost(duration)
    print(f"[费用] Seedance 预估 {tokens:,} tokens ≈ ¥{yuan}")

    if dry_run:
        srt = f"{work_dir}/sub.srt"
        Path(srt).write_text(_build_srt(script["lines"], voice["duration"]), encoding="utf-8")
        print(f"[dry-run] 已跳过 Seedance / 混音 / 烧字幕")
        print(f"[dry-run] voice={voice['path']}  srt={srt}")
        return {
            "dry_run": True,
            "voice_path": voice["path"],
            "srt_path": srt,
            "template": tpl_key,
            "voice_duration": voice["duration"],
            "video_duration": duration,
            "tokens": tokens,
            "cost_yuan": yuan,
            "prompt": prompt,
        }

    # 4. 生成视频
    silent = _generate_silent_video(
        script["image"], prompt, duration,
        f"{work_dir}/silent.mp4",
    )

    # 5. 混音
    mixed = mix_audio(
        voice["path"],
        bgm_key=script.get("bgm", tpl["bgm"]),
        bgm_volume=script.get("bgm_volume", tpl["bgm_volume"]),
        output=f"{work_dir}/mixed.mp3",
    )
    print(f"[混音] BGM={script.get('bgm', tpl['bgm'])} → {mixed}")

    # 6. 合成
    output = script.get("output") or f"{work_dir}/final.mp4"
    if script.get("subtitle", True):
        with_audio = f"{work_dir}/with_audio.mp4"
        mux_video_audio(silent, mixed, with_audio)
        srt = f"{work_dir}/sub.srt"
        Path(srt).write_text(_build_srt(script["lines"], voice["duration"]), encoding="utf-8")
        _burn_subtitles(with_audio, srt, output)
        print(f"[字幕] 烧录 → {output}")
    else:
        mux_video_audio(silent, mixed, output)
        print(f"[输出] → {output}")

    return {
        "output": output,
        "template": tpl_key,
        "voice_duration": voice["duration"],
        "video_duration": duration,
        "tokens": tokens,
        "cost_yuan": yuan,
        "size_mb": round(os.path.getsize(output) / 1e6, 2),
    }


# ---------- 自检 ----------

def preflight() -> dict:
    """检查依赖、凭证、BGM 库是否就绪。返回一份 status 报告。"""
    import shutil
    from bgm import BGM_DIR, list_available_bgm

    status = {"ok": True, "checks": []}

    def add(name, ok, msg=""):
        status["checks"].append({"name": name, "ok": ok, "msg": msg})
        if not ok:
            status["ok"] = False

    # 1. ffmpeg / ffprobe
    add("ffmpeg",  bool(shutil.which("ffmpeg")),  "" if shutil.which("ffmpeg") else "brew install ffmpeg")
    add("ffprobe", bool(shutil.which("ffprobe")), "" if shutil.which("ffprobe") else "随 ffmpeg 一起装")

    # 2. edge-tts
    try:
        import edge_tts  # noqa: F401
        add("edge-tts (Python)", True)
    except ImportError:
        add("edge-tts (Python)", False, "pip install edge-tts")

    # 3. ARK_API_KEY
    add("ARK_API_KEY", bool(ARK_API_KEY),
        "export ARK_API_KEY=ak-xxxxx（方舟控制台获取）" if not ARK_API_KEY else "")

    # 4. 火山 TTS（可选）
    has_volc = bool(os.environ.get("VOLC_TTS_APP_ID") and os.environ.get("VOLC_TTS_TOKEN"))
    add("火山 TTS（可选）", True, "已配置 → 使用火山 TTS" if has_volc else "未配置 → 降级 edge-tts（免费）")

    # 5. BGM 库
    bgms = list_available_bgm()
    add("BGM 库", bool(bgms),
        f"目录 {BGM_DIR} 下没有 BGM 文件，将无 BGM 模式（不影响视频生成）"
        if not bgms else f"已就位: {', '.join(bgms)}")

    # 6. 中文字体（PingFang）
    pingfang = os.path.exists("/System/Library/Fonts/PingFang.ttc")
    add("中文字体 PingFang", pingfang,
        "字幕烧录需中文字体；可在剧本中 subtitle:false 跳过"
        if not pingfang else "")

    return status


def _print_preflight(status: dict):
    print(f"\n=== 火15 带货视频 v2 自检 ===\n")
    for c in status["checks"]:
        icon = "✅" if c["ok"] else "❌"
        line = f"  {icon} {c['name']}"
        if c["msg"]:
            line += f"  — {c['msg']}"
        print(line)
    print(f"\n总体状态: {'✅ 可以发车' if status['ok'] else '❌ 有缺项，按上面提示修复'}\n")


# ---------- CLI ----------

USAGE = """\
火15 带货视频 v2 — pipeline.py

用法：
  python pipeline.py preflight                     自检依赖/凭证/BGM
  python pipeline.py templates                     列出 8 套人设模板
  python pipeline.py voices                        列出推荐音色
  python pipeline.py dry-run <script.json>         只跑 TTS + 字幕，不调 Seedance（省钱测剧本）
  python pipeline.py render <script.json>          完整端到端
  python pipeline.py <script.json>                 等同 render（向后兼容）
"""


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(USAGE)
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "preflight":
        s = preflight()
        _print_preflight(s)
        sys.exit(0 if s["ok"] else 1)

    if cmd == "templates":
        for t in list_templates():
            print(f"  - {t['key']:20s} {t['label']}  品类: {','.join(t['categories'])}")
        sys.exit(0)

    if cmd == "voices":
        from tts import list_voices
        for v in list_voices():
            print(f"  - {v['id']:32s} {v['label']}")
        sys.exit(0)

    if cmd in ("render", "dry-run"):
        if len(sys.argv) < 3:
            print(f"❌ 缺剧本路径：python pipeline.py {cmd} <script.json>")
            sys.exit(1)
        script_path = sys.argv[2]
    else:
        # 向后兼容：第一个参数直接当 script.json
        script_path = cmd
        cmd = "render"

    with open(script_path, encoding="utf-8") as f:
        script = json.load(f)
    result = render(script, dry_run=(cmd == "dry-run"))
    print(json.dumps(result, ensure_ascii=False, indent=2))
