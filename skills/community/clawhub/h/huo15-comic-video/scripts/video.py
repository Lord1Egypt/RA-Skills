"""图生视频（Seedance 2.0），支持并发与续跑."""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve()
# _shared/ 定位：优先 bundled（scripts/_shared/），fallback monorepo 根
for _cand in (HERE.parent / "_shared", HERE.parents[2] / "_shared"):
    if (_cand / "config.py").exists():
        sys.path.insert(0, str(_cand))
        break

from ark_api import ArkClient, cost_from_video_response
from config import DEFAULTS, video_unit_price
from cost_guard import CostGuard
from checkpoint import Checkpoint


def build_video_prompt(scene: dict) -> str:
    parts = [
        scene.get("action", ""),
        scene.get("camera", ""),
        scene.get("mood", "") + "氛围",
    ]
    return "，".join(p for p in parts if p) + "。"


def gen_one(
    client: ArkClient,
    scene: dict,
    frame_path: pathlib.Path,
    out_path: pathlib.Path,
    duration: int,
    resolution: str = "720p",
    fast: bool = False,
) -> dict:
    task_id = client.submit_video(
        prompt=build_video_prompt(scene),
        first_frame=str(frame_path),
        duration=duration,
        ratio="9:16",
        resolution=resolution,
        return_last_frame=True,
        fast=fast,
    )
    print(f"  ⏳ {scene['id']} task={task_id} ({resolution}{'/fast' if fast else ''})")
    data = client.poll_video(task_id)
    video_url = data["content"]["video_url"]
    client.download_video(video_url, out_path)
    info = {
        "sid": scene["id"],
        "task_id": task_id,
        "tokens": data.get("usage", {}).get("total_tokens", 0),
        "last_frame_url": data.get("content", {}).get("last_frame_url"),
        "cost": cost_from_video_response(data, resolution),
    }
    return info


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--script", required=True)
    p.add_argument("--frame-dir", required=True)
    p.add_argument("--out-dir", required=True)
    p.add_argument("--resolution", default=DEFAULTS["resolution"],
                   choices=["480p", "720p", "1080p", "2K"])
    p.add_argument("--fast", action="store_true")
    args = p.parse_args()

    script = json.loads(pathlib.Path(args.script).read_text())
    frame_dir = pathlib.Path(args.frame_dir)
    out_dir = pathlib.Path(args.out_dir)
    resolution = script.get("resolution", args.resolution)
    fast = script.get("fast_mode", args.fast)
    out_dir.mkdir(parents=True, exist_ok=True)
    last_dir = out_dir / "last_frames"
    last_dir.mkdir(parents=True, exist_ok=True)

    project_dir = out_dir.parent
    guard = CostGuard.load(project_dir)
    cp = Checkpoint(project_dir)

    client = ArkClient()
    scenes = script.get("scenes", [])
    duration = script.get("scene_duration", DEFAULTS["scene_duration"])

    pending = []
    for scene in scenes:
        sid = scene["id"]
        out = out_dir / f"{sid}.mp4"
        if out.exists() or cp.sub_done("videos", sid):
            print(f"  ⏭️  {sid} 已完成")
            continue
        frame = frame_dir / f"{sid}.png"
        if not frame.exists():
            print(f"  ❌ {sid} 关键帧不存在: {frame}")
            return 1
        pending.append((scene, frame, out))

    if not pending:
        print("✅ 所有视频已完成")
        return 0

    print(f"[video] {len(pending)} 个镜头待生成，并发 {DEFAULTS['concurrency']}")

    with cf.ThreadPoolExecutor(max_workers=DEFAULTS["concurrency"]) as ex:
        futures = {
            ex.submit(gen_one, client, sc, fr, ou, duration, resolution, fast): sc["id"]
            for sc, fr, ou in pending
        }
        for fut in cf.as_completed(futures):
            sid = futures[fut]
            try:
                info = fut.result()
                # 下载 last_frame 供下镜衔接
                if info.get("last_frame_url"):
                    import requests
                    r = requests.get(info["last_frame_url"])
                    (last_dir / f"{sid}_last.png").write_bytes(r.content)
                # 按实际 token 计费（若无则降级估算）
                actual_cost = info.get("cost") or (duration * video_unit_price(resolution, fast))
                guard.charge("videos", sid, actual_cost)
                cp.sub_mark("videos", sid)
                print(f"  ✅ {sid} ¥{actual_cost:.2f} ({info.get('tokens', 0):,} tok)")
            except Exception as e:
                cp.sub_mark("videos", sid, f"failed: {e}")
                print(f"  ❌ {sid}: {e}")

    # 检查是否全部完成
    remaining = [s for s in scenes if not cp.sub_done("videos", s["id"])]
    if remaining:
        print(f"⚠️  剩余 {len(remaining)} 镜头未完成，重跑本脚本续跑")
        return 2
    print(f"✅ 视频: {len(scenes)} 镜")
    return 0


if __name__ == "__main__":
    sys.exit(main())
