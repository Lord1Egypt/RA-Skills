#!/usr/bin/env python3
"""
heyvideogen 流水线脚本
用法：
  python scripts/run_heyvideogen.py init "项目名"
  python scripts/run_heyvideogen.py gen "选题内容" --mode auto
  python scripts/run_heyvideogen.py render --project heyvideogen-project
"""
import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT  = Path(__file__).parent.parent.parent           # scripts/ → heyvideogen/ → skills/ → workspace/
SKILLS_ROOT   = PROJECT_ROOT                                   # /root/.openclaw/workspace
VIDEOS_SKILL  = SKILLS_ROOT / "videogen"
MINIMAX_SCRIPTS = SKILLS_ROOT / "minimax-multimodal" / "scripts"

sys.path.insert(0, str(VIDEOS_SKILL / "scripts" / "v2"))
from storyboard_generator import generate_storyboard


def cmd(cmd: str, cwd=None, shell=True):
    print(f"\n>>> {cmd}")
    result = subprocess.run(cmd, cwd=cwd, shell=shell, capture_output=False)
    return result.returncode == 0


def run_init(project_name: str):
    """初始化 HyperFrames 项目"""
    target = PROJECT_ROOT / project_name
    if target.exists():
        print(f"⚠️  项目 {project_name} 已存在")
        return

    rc = cmd(f"npx hyperframes init {project_name} --non-interactive", cwd=PROJECT_ROOT)
    if not rc:
        print("❌ hyperframes init 失败")
        return

    # 创建子目录
    for d in ["clips", "chunks", "slides", "compositions", "heyvideogen-output"]:
        (target / d).mkdir(exist_ok=True)
    print(f"\n✅ 项目已创建：{target}")
    print(f"   进入项目：cd {target}")
    print(f"   下一步：python {__file__} gen \"选题\" --project {project_name}")


def run_gen(topic: str, mode: str = "auto", project: str = None, duration: int = 60):
    """生成分镜 + TTS + AI 片段"""
    project_path = PROJECT_ROOT / project if project else PROJECT_ROOT
    output_dir   = project_path / "heyvideogen-output"
    clips_dir    = project_path / "clips"
    output_dir.mkdir(exist_ok=True)
    clips_dir.mkdir(exist_ok=True)

    print(f"\n{'='*50}")
    print(f"🎬 Heyvideogen 流水线启动")
    print(f"   选题：{topic}")
    print(f"   模式：{mode}")
    print(f"   项目：{project_path}")
    print(f"{'='*50}")

    # Step 1: 分析选题 → 分镜
    print("\n[1/4] 生成分镜...")
    storyboard = generate_storyboard(topic, mode=mode, duration=duration)
    storyboard_path = output_dir / "storyboard.json"
    with open(storyboard_path, "w", encoding="utf-8") as f:
        json.dump(storyboard, f, ensure_ascii=False, indent=2)
    print(f"   ✅ 分镜已保存：{storyboard_path}")

    # Step 2: TTS（复用 videogen harness）
    print("\n[2/4] 生成 TTS 配音...")
    narrations = [p.get("narration", "") for p in storyboard.get("panels", []) if p.get("narration")]
    script_text = " ".join(narrations)
    if script_text:
        tts_cmd = (
            f'python "{VIDEOS_SKILL}/scripts/v2/tts_harness.py" '
            f'"{script_text[:500]}" --output "{output_dir}"'
        )
        cmd(tts_cmd)
        print(f"   ✅ TTS 完成：{output_dir}/voiceover.mp3")
    else:
        print("   ⚠️  无旁白文本，跳过 TTS")

    # Step 3: 生成 AI 视频片段（Hailuo）
    print("\n[3/4] 生成 AI 视频片段...")
    panels = storyboard.get("panels", [])
    clips_ok, clips_fail = 0, 0
    for i, panel in enumerate(panels):
        prompt = panel.get("video_prompt", "")
        clip_path = clips_dir / f"clip_{i+1:02d}.mp4"
        if not prompt:
            print(f"   ⊝ clip_{i+1:02d}: 无 video_prompt，跳过")
            continue
        duration_sec = panel.get("duration", 6)
        hf_prompt = prompt.strip()
        if not hf_prompt:
            print(f"   ⊝ clip_{i+1:02d}: prompt 为空，跳过")
            continue
        gen_cmd = (
            f'python "{MINIMAX_SCRIPTS}/video/generate_video.py" '
            f'--mode t2v '
            f'--prompt "{hf_prompt}" '
            f'--duration {duration_sec} '
            f'--output "{clip_path}"'
        )
        print(f"\n   [{i+1}/{len(panels)}] 生成 clip_{i+1:02d}...")
        ok = cmd(gen_cmd)
        if ok:
            clips_ok += 1
            print(f"   ✅ clip_{i+1:02d} 完成")
        else:
            clips_fail += 1
            print(f"   ❌ clip_{i+1:02d} 失败，继续下一片段")
    print(f"\n   📊 AI片段：{clips_ok} 成功 / {clips_fail} 失败")

    # Step 4: 输出指令
    print("\n[4/4] 下一步操作：")
    print(f"   1. 编辑 HTML：cp {PROJECT_ROOT}/skills/heyvideogen/templates/apple-style/index.html {project_path}/index.html")
    print(f"   2. 更新 clips 路径：编辑 index.html 里的 src=\"clips/clip_XX.mp4\"")
    print(f"   3. 渲染：cd {project_path} && npx hyperframes render --output heyvideogen-output/final.mp4")
    print(f"   4. 合并音频：ffmpeg -y -i heyvideogen-output/final.mp4 -i heyvideogen-output/voiceover.mp3 \\")
    print(f"                 -c:v copy -c:a aac -b:a 192k -shortest heyvideogen-output/video_final.mp4")
    print(f"\n   ✅ 分镜 JSON：{storyboard_path}")


def run_render(project: str):
    """渲染 HyperFrames 项目"""
    project_path = PROJECT_ROOT / project
    output = project_path / "heyvideogen-output" / "final.mp4"
    print(f"\n🎬 开始渲染：{project_path}")
    ok = cmd(f"npx hyperframes lint", cwd=project_path)
    if not ok:
        print("⚠️  Lint 有警告，继续渲染...")
    cmd(f"npx hyperframes render --output {output} --fps 30 --quality standard", cwd=project_path)
    print(f"✅ 渲染完成：{output}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="heyvideogen 流水线")
    sub = parser.add_subparsers()

    p_init = sub.add_parser("init", help="初始化 HyperFrames 项目")
    p_init.add_argument("name", help="项目名称")

    p_gen = sub.add_parser("gen", help="生成视频（选题→分镜→TTS→AI片段）")
    p_gen.add_argument("topic", help="选题内容")
    p_gen.add_argument("--mode", default="auto", choices=["auto", "A", "B", "C"])
    p_gen.add_argument("--project", default=None)
    p_gen.add_argument("--duration", type=int, default=60)

    p_render = sub.add_parser("render", help="渲染 HyperFrames 项目")
    p_render.add_argument("--project", required=True)

    args = parser.parse_args()

    if hasattr(args, "name"):
        run_init(args.name)
    elif hasattr(args, "topic"):
        run_gen(args.topic, mode=args.mode, project=args.project, duration=args.duration)
    elif hasattr(args, "project"):
        run_render(args.project)
    else:
        parser.print_help()
