"""对口型（Kling 2.5 Lip Sync）."""
from __future__ import annotations

import argparse
import json
import os
import pathlib
import shutil
import sys
import time

import requests

HERE = pathlib.Path(__file__).resolve()
# _shared/ 定位：优先 bundled（scripts/_shared/），fallback monorepo 根
for _cand in (HERE.parent / "_shared", HERE.parents[2] / "_shared"):
    if (_cand / "config.py").exists():
        sys.path.insert(0, str(_cand))
        break

from config import PRICING, ENDPOINTS, MODELS
from cost_guard import CostGuard
from checkpoint import Checkpoint


KLING_API = ENDPOINTS["kling_base"]  # https://api.klingai.com/v1


def submit_lipsync(video_path: pathlib.Path, audio_path: pathlib.Path) -> str:
    key = os.environ.get("KLING_API_KEY", "")
    if not key:
        raise RuntimeError("缺少 KLING_API_KEY")
    headers = {"Authorization": f"Bearer {key}"}
    files = {
        "video": open(video_path, "rb"),
        "audio": open(audio_path, "rb"),
    }
    data = {"model": MODELS["lipsync"]}  # kling-v2.6
    r = requests.post(f"{KLING_API}/videos/lip-sync", headers=headers, files=files, data=data)
    r.raise_for_status()
    return r.json()["task_id"]


def poll_lipsync(task_id: str, timeout_s: int = 600) -> str:
    key = os.environ.get("KLING_API_KEY", "")
    headers = {"Authorization": f"Bearer {key}"}
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        time.sleep(8)
        r = requests.get(f"{KLING_API}/videos/lip-sync/{task_id}", headers=headers)
        data = r.json()
        if data.get("status") == "succeeded":
            return data["video_url"]
        if data.get("status") == "failed":
            raise RuntimeError(f"lipsync 失败: {data}")
    raise TimeoutError(f"lipsync 超时 {task_id}")


def first_dialogue_audio(sid: str, audio_dir: pathlib.Path) -> pathlib.Path | None:
    cands = sorted(audio_dir.glob(f"{sid}_*.wav"))
    return cands[0] if cands else None


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--video-dir", required=True)
    p.add_argument("--audio-dir", required=True)
    p.add_argument("--out-dir", required=True)
    args = p.parse_args()

    video_dir = pathlib.Path(args.video_dir)
    audio_dir = pathlib.Path(args.audio_dir)
    out_dir = pathlib.Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    project_dir = out_dir.parent
    guard = CostGuard.load(project_dir)
    cp = Checkpoint(project_dir)

    for video in sorted(video_dir.glob("S*.mp4")):
        sid = video.stem
        out = out_dir / f"{sid}.mp4"
        if out.exists() or cp.sub_done("lipsync", sid):
            print(f"  ⏭️  {sid}")
            continue

        audio = first_dialogue_audio(sid, audio_dir)
        if not audio:
            print(f"  🤫 {sid} 无对白，复制原视频")
            shutil.copy(video, out)
            cp.sub_mark("lipsync", sid)
            continue

        try:
            print(f"  👄 {sid} → lipsync")
            task_id = submit_lipsync(video, audio)
            url = poll_lipsync(task_id)
            r = requests.get(url, stream=True)
            with open(out, "wb") as f:
                for chunk in r.iter_content(8192):
                    f.write(chunk)
            guard.charge("lipsync", sid, PRICING["lipsync_per_5s"])
            cp.sub_mark("lipsync", sid)
        except Exception as e:
            print(f"  ❌ {sid}: {e}, 降级为原视频")
            shutil.copy(video, out)
            cp.sub_mark("lipsync", sid, "fallback")

    print(f"✅ 口型同步完成")
    return 0


if __name__ == "__main__":
    sys.exit(main())
