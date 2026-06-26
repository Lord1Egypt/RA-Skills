"""主编排入口。串起家族 8 个子 skill 完成漫剧生成。

用法:
    python run.py --theme "少年剑仙三年归来" --duration 240 --cap 600
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import subprocess
import sys
import time

HERE = pathlib.Path(__file__).resolve()
REPO_ROOT = HERE.parents[2]  # monorepo 根 / 独立安装时的 skills 父目录
# _shared/ 定位：优先 bundled（scripts/_shared/），fallback monorepo 根
for _cand in (HERE.parent / "_shared", REPO_ROOT / "_shared"):
    if (_cand / "config.py").exists():
        sys.path.insert(0, str(_cand))
        break

from config import DEFAULTS
from cost_guard import CostGuard, BudgetExceeded, estimate_total
from checkpoint import Checkpoint


def slugify(text: str) -> str:
    s = re.sub(r"[^\w\u4e00-\u9fff]+", "-", text).strip("-")
    return s[:40] or f"project-{int(time.time())}"


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--theme", required=True, help="主题一句话")
    p.add_argument("--duration", type=int, default=DEFAULTS["duration_total"])
    p.add_argument("--style", default=DEFAULTS["style"])
    p.add_argument("--genre", default=DEFAULTS["genre"])
    p.add_argument("--cap", type=float, default=DEFAULTS["cost_cap"])
    p.add_argument("--no-lipsync", action="store_true")
    p.add_argument("--no-bgm", action="store_true")
    p.add_argument("--output-root", default=str(REPO_ROOT / "output"))
    p.add_argument("--auto-confirm", action="store_true", help="跳过交互确认")
    return p.parse_args()


def run_substep(skill_name: str, script: str, *args: str) -> subprocess.CompletedProcess:
    """调用子 skill 的脚本."""
    cmd = [
        sys.executable,
        str(REPO_ROOT / skill_name / "scripts" / script),
        *args,
    ]
    print(f"  $ {' '.join(cmd)}")
    return subprocess.run(cmd, check=True)


def confirm(prompt: str) -> bool:
    try:
        return input(prompt).strip().lower() in {"y", "yes", "是", "开始", "确认", "go"}
    except EOFError:
        return False


def main() -> int:
    args = parse_args()

    project_slug = slugify(args.theme)
    project_dir = pathlib.Path(args.output_root) / project_slug
    project_dir.mkdir(parents=True, exist_ok=True)

    n_scenes = args.duration // DEFAULTS["scene_duration"]

    # -------- Step 1: 预估成本（硬熔断）--------
    est = estimate_total(
        n_scenes=n_scenes,
        n_characters=3,
        total_chars=int(args.duration * 3.5),  # 经验值：每秒 3-4 字对白
        scene_duration=DEFAULTS["scene_duration"],
        enable_lipsync=not args.no_lipsync,
        enable_bgm=not args.no_bgm,
    )
    guard = CostGuard.load(project_dir, cap=args.cap)

    print(f"\n📜 项目: {project_slug}")
    print(f"   时长 {args.duration}s · {n_scenes} 镜头 · {args.style} · {args.genre}")
    print(f"   预估: 图 ¥{est['image']} / 视频 ¥{est['video']} / TTS ¥{est['tts']} "
          f"/ 口型 ¥{est['lipsync']} / BGM ¥{est['bgm']}")
    print(f"   合计 ¥{est['total']}（熔断上限 ¥{guard.cap}）\n")

    try:
        guard.preflight(est["total"])
    except BudgetExceeded as e:
        print(f"❌ {e}")
        return 2

    if not args.auto_confirm and not confirm("确认开始? [y/N] "):
        print("已取消。")
        return 0

    # -------- Step 2-10: 按 checkpoint 续跑各步骤 --------
    cp = Checkpoint(project_dir)
    steps = [
        ("script",      "huo15-comic-script",      "script_gen.py",
            ["--theme", args.theme, "--duration", str(args.duration),
             "--style", args.style, "--genre", args.genre,
             "--out", str(project_dir / "script.json")]),
        ("characters",  "huo15-comic-character",   "character.py",
            ["--script", str(project_dir / "script.json"),
             "--out-dir", str(project_dir / "characters")]),
        ("storyboard",  "huo15-comic-storyboard",  "storyboard.py",
            ["--script", str(project_dir / "script.json"),
             "--char-dir", str(project_dir / "characters"),
             "--out-dir", str(project_dir / "storyboard")]),
        ("videos",      "huo15-comic-video",       "video.py",
            ["--script", str(project_dir / "script.json"),
             "--frame-dir", str(project_dir / "storyboard"),
             "--out-dir", str(project_dir / "videos")]),
        ("dubs",        "huo15-comic-dub",         "dub.py",
            ["--script", str(project_dir / "script.json"),
             "--out-dir", str(project_dir / "audio")]),
    ]
    if not args.no_lipsync:
        steps.append(("lipsync", "huo15-comic-lipsync", "lipsync.py",
            ["--video-dir", str(project_dir / "videos"),
             "--audio-dir", str(project_dir / "audio"),
             "--out-dir", str(project_dir / "lipsync")]))
    if not args.no_bgm:
        steps.append(("bgm", "huo15-comic-bgm", "bgm.py",
            ["--script", str(project_dir / "script.json"),
             "--duration", str(args.duration),
             "--out", str(project_dir / "bgm.mp3")]))
    steps.append(("edit", "huo15-comic-edit", "edit.py",
        ["--project-dir", str(project_dir)]))

    t0 = time.time()
    for step, skill, script, sub_args in steps:
        if cp.is_done(step):
            print(f"⏭️  {step}: 已完成，跳过")
            continue
        cp.mark_running(step)
        try:
            run_substep(skill, script, *sub_args)
            cp.mark_done(step)
        except subprocess.CalledProcessError as e:
            cp.mark_failed(step, str(e))
            print(f"❌ {step} 失败: {e}")
            return 3
        except BudgetExceeded as e:
            print(f"🛑 熔断: {e}")
            return 4

    # -------- Step 11: 交付 --------
    final = project_dir / "final.mp4"
    elapsed = time.time() - t0
    report = guard.report()
    print(f"\n🎉 {final} (耗时 {elapsed/60:.1f} 分钟)")
    print(f"   实际成本: ¥{report['spent']} / ¥{report['cap']}")
    print(f"   成本分布: {json.dumps(report['by_step'], ensure_ascii=False)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
