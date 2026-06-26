"""背景音乐（Suno v5）."""
from __future__ import annotations

import argparse
import collections
import json
import os
import pathlib
import sys
import time

import requests

HERE = pathlib.Path(__file__).resolve()
REPO_ROOT = HERE.parents[2]  # monorepo 根 / 独立安装时的 skills 父目录
# _shared/ 定位：优先 bundled（scripts/_shared/），fallback monorepo 根
for _cand in (HERE.parent / "_shared", REPO_ROOT / "_shared"):
    if (_cand / "config.py").exists():
        sys.path.insert(0, str(_cand))
        break

from config import PRICING, ENDPOINTS, MODELS
from cost_guard import CostGuard


SUNO_API = ENDPOINTS["suno_base"]  # https://api.sunoapi.org（Suno 无公开官方 API，走第三方）


def top_moods(script: dict, n: int = 3) -> list[str]:
    counter = collections.Counter()
    for s in script.get("scenes", []):
        m = s.get("mood", "")
        if m:
            counter[m] += 1
    return [m for m, _ in counter.most_common(n)]


def build_prompt(moods: list[str], duration: int) -> str:
    mood_str = "、".join(moods) if moods else "苍凉壮阔"
    return (
        f"国风古风纯音乐，{mood_str}氛围，"
        f"古筝为主旋律，点缀琵琶和笛子，"
        f"时长约 {duration} 秒，纯音乐无人声，"
        f"适合仙侠/国风动画背景。"
    )


def suno_generate(prompt: str, duration: int) -> str:
    key = os.environ.get("SUNO_API_KEY", "")
    if not key:
        raise RuntimeError("缺少 SUNO_API_KEY")
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    body = {
        "prompt": prompt,
        "duration": duration,
        "instrumental": True,
        "model": MODELS["music"],  # suno-v5.5
    }
    r = requests.post(f"{SUNO_API}/v1/generate", headers=headers, json=body, timeout=60)
    r.raise_for_status()
    task_id = r.json().get("id") or r.json().get("task_id")

    deadline = time.time() + 600
    while time.time() < deadline:
        time.sleep(10)
        g = requests.get(f"{SUNO_API}/v1/tasks/{task_id}", headers=headers, timeout=30)
        d = g.json()
        status = d.get("status")
        if status in ("succeeded", "complete"):
            return d.get("audio_url") or d.get("output", [{}])[0].get("audio_url")
        if status in ("failed", "error"):
            raise RuntimeError(f"suno 失败: {d}")
    raise TimeoutError("suno 超时")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--script", required=True)
    p.add_argument("--duration", type=int, required=True)
    p.add_argument("--out", required=True)
    args = p.parse_args()

    out = pathlib.Path(args.out)
    if out.exists():
        print(f"  ⏭️  {out.name} 已存在")
        return 0

    script = json.loads(pathlib.Path(args.script).read_text())
    moods = top_moods(script)
    prompt = build_prompt(moods, args.duration)
    print(f"🎵 BGM prompt: {prompt}")

    project_dir = out.parent
    guard = CostGuard.load(project_dir)

    try:
        url = suno_generate(prompt, args.duration)
        r = requests.get(url, stream=True)
        out.parent.mkdir(parents=True, exist_ok=True)
        with open(out, "wb") as f:
            for chunk in r.iter_content(8192):
                f.write(chunk)
        guard.charge("bgm", "main", PRICING["bgm_per_track"])
        print(f"✅ {out}")
    except Exception as e:
        # Fallback：找本地素材
        fallback = REPO_ROOT / "templates" / "bgm_library" / "国风" / f"{moods[0] if moods else 'default'}.mp3"
        if fallback.exists():
            print(f"⚠️  Suno 失败 ({e})，fallback → {fallback.name}")
            import shutil
            shutil.copy(fallback, out)
        else:
            print(f"❌ BGM 生成失败且无 fallback: {e}")
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
