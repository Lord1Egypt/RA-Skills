#!/usr/bin/env python3
"""
call_video_api.py  (v7 - 基于调试版本整理)

依赖：pip install 'volcengine-python-sdk[ark]' requests

用法：
  # 批量生成所有镜头视频
  python call_video_api.py batch \
      --input  ../storyboard.json \
      --output ../videos/

  # 手动指定分镜图目录（图片不在默认位置时）
  python call_video_api.py batch \
      --input  ../storyboard.json \
      --output ../videos/ \
      --frames-dir ../storyboard/frames/

  # 重新生成单个镜头视频（检查点后修正用）
  python call_video_api.py single \
      --shot-id S01_03 \
      --input ../storyboard.json \
      --output ../videos/
"""

import argparse, base64, json, os, sys, time, requests
from pathlib import Path

# ══════════════════════════════════════════════════════
#  ★ 配置区
# ══════════════════════════════════════════════════════
ARK_API_KEY = os.getenv("ARK_API_KEY", "在这里填你的方舟APIKey")

# 模型选择（二选一）：
#   lite 版：调试 / 快速预览，速度快
#   pro  版：正式出片，质量更高
ARK_VIDEO_MODEL = "doubao-seedance-1-0-lite-i2v-250428"
# ARK_VIDEO_MODEL = "doubao-seedance-1-0-pro-250528"

POLL_INTERVAL = 8    # 轮询间隔（秒）
MAX_POLLS     = 45   # 最多等待 45 × 8s = 6 分钟


# ──────────────────────────────────────────────────────
# 启动检查
# ──────────────────────────────────────────────────────
def startup_check():
    print("=" * 55)
    print("  漫剧视频生成脚本  (v7 - 图生视频)")
    print("=" * 55)
    key_ok = ARK_API_KEY and ARK_API_KEY != "在这里填你的方舟APIKey"
    print(f"  🔑 ARK API Key  : {'✅ 已配置' if key_ok else '❌ 未配置'}")
    print(f"  🎬 视频模型     : {ARK_VIDEO_MODEL}")
    print(f"  ⏱  轮询设置    : 每 {POLL_INTERVAL}s，最多 {MAX_POLLS} 次（约 {MAX_POLLS * POLL_INTERVAL // 60} 分钟）")
    print()
    if not key_ok:
        print("❌ 请在脚本顶部填写 ARK_API_KEY，或设置环境变量：")
        print("   export ARK_API_KEY=your_key_here")
        sys.exit(1)
    try:
        from volcenginesdkarkruntime import Ark
        print("  📦 volcengine SDK : ✅ 已安装\n")
    except ImportError:
        print("  📦 volcengine SDK : ❌ 未安装，请运行：")
        print("     pip install 'volcengine-python-sdk[ark]'")
        sys.exit(1)


# ──────────────────────────────────────────────────────
# 自动查找参考图
# ──────────────────────────────────────────────────────
def auto_find_image(shot_id: str, sb_path: Path, frames_dir: str | None) -> str | None:
    """
    按优先级查找 {shot_id}.png/.jpg：
    1. --frames-dir 指定目录
    2. storyboard.json 同级的 storyboard/frames/
    3. storyboard.json 同级的 frames/
    4. storyboard.json 同级目录
    """
    candidate_dirs = []
    if frames_dir:
        candidate_dirs.append(Path(frames_dir))
    candidate_dirs += [
        sb_path.parent / "storyboard" / "frames",
        sb_path.parent / "frames",
        sb_path.parent,
    ]
    for d in candidate_dirs:
        for ext in (".png", ".jpg", ".jpeg", ".webp"):
            p = d / f"{shot_id}{ext}"
            if p.exists():
                return str(p)
    return None


# ──────────────────────────────────────────────────────
# 本地图片 → base64 data URI
# ──────────────────────────────────────────────────────
def image_to_data_uri(image_path: str) -> str:
    suffix = Path(image_path).suffix.lower().lstrip(".")
    mime   = {"png": "image/png", "jpg": "image/jpeg",
              "jpeg": "image/jpeg", "webp": "image/webp"}.get(suffix, "image/png")
    with open(image_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    return f"data:{mime};base64,{b64}"


# ──────────────────────────────────────────────────────
# 提交视频生成任务
# ──────────────────────────────────────────────────────
def submit_video_task(image_path: str, prompt: str, duration: int) -> str | None:
    from volcenginesdkarkruntime import Ark
    client = Ark(
        base_url="https://ark.cn-beijing.volces.com/api/v3",
        api_key=ARK_API_KEY,
    )
    # 方舟视频时长只支持 5s / 10s
    actual_duration = 5 if duration <= 6 else 10
    text_with_flags = (
        f"{prompt} "
        f"--duration {actual_duration} "
        f"--resolution 720p "
        f"--camerafixed false"
    )
    image_url = image_to_data_uri(image_path)

    print(f"    → 提交任务（时长 {actual_duration}s，模型 {ARK_VIDEO_MODEL}）...")
    try:
        task = client.content_generation.tasks.create(
            model=ARK_VIDEO_MODEL,
            content=[
                {"type": "text",      "text": text_with_flags},
                {"type": "image_url", "image_url": {"url": image_url}},
            ],
        )
        task_id = task.id
        print(f"    ✅ 任务已提交: {task_id}")
        return task_id
    except Exception as e:
        print(f"    ❌ 提交失败: {type(e).__name__}: {e}")
        return None


# ──────────────────────────────────────────────────────
# 轮询任务结果
# ──────────────────────────────────────────────────────
def poll_video_task(task_id: str) -> str | None:
    from volcenginesdkarkruntime import Ark
    client = Ark(
        base_url="https://ark.cn-beijing.volces.com/api/v3",
        api_key=ARK_API_KEY,
    )
    for i in range(1, MAX_POLLS + 1):
        time.sleep(POLL_INTERVAL)
        try:
            task   = client.content_generation.tasks.get(task_id=task_id)
            status = task.status
            print(f"    ⏳ [{i}/{MAX_POLLS}] 状态: {status}")

            if status == "succeeded":
                content   = task.content
                video_url = getattr(content, "video_url", None)
                if video_url:
                    print(f"    ✅ 视频就绪: {str(video_url)[:70]}...")
                    return str(video_url)
                print(f"    ⚠️  succeeded 但未找到 video_url，完整 content: {content}")
                return None

            elif status == "failed":
                reason = getattr(task, "error", getattr(task, "message", "未知原因"))
                print(f"    ❌ 任务失败: {reason}")
                return None

        except Exception as e:
            print(f"    ⚠️  轮询异常（第 {i} 次）: {e}")

    print(f"    ❌ 超时（等待 {MAX_POLLS * POLL_INTERVAL}s）")
    return None


# ──────────────────────────────────────────────────────
# 下载视频
# ──────────────────────────────────────────────────────
def download_video(url: str, out_path: str) -> bool:
    try:
        print(f"    ↓ 下载视频...")
        r = requests.get(url, timeout=120, stream=True)
        r.raise_for_status()
        Path(out_path).parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "wb") as f:
            for chunk in r.iter_content(65536):
                f.write(chunk)
        size_mb = Path(out_path).stat().st_size / 1024 / 1024
        print(f"    💾 已保存 → {out_path}  ({size_mb:.1f} MB)")
        return True
    except Exception as e:
        print(f"    ❌ 下载失败: {e}")
        return False


# ──────────────────────────────────────────────────────
# 处理单个 shot（供批量和单个重生成复用）
# ──────────────────────────────────────────────────────
def process_shot(shot: dict, sb_path: Path, output_dir: str, frames_dir: str | None) -> dict:
    shot_id  = shot["shot_id"]
    duration = shot.get("duration", 5)
    ref_img  = shot.get("reference_image")

    print(f"\n━━━ [{shot_id}]  ({duration}s) ━━━")

    # 1. 优先用 storyboard.json 里记录的路径
    if ref_img and Path(ref_img).exists():
        print(f"  🖼  参考图: {ref_img}")
    else:
        # 2. 自动按约定路径查找
        found = auto_find_image(shot_id, sb_path, frames_dir)
        if found:
            print(f"  🔍 自动找到参考图: {found}")
            shot["reference_image"] = found
            ref_img = found
        else:
            # 3. 报告搜索过的位置，方便排查
            search_dirs = []
            if frames_dir: search_dirs.append(frames_dir)
            search_dirs += [
                str(sb_path.parent / "storyboard" / "frames"),
                str(sb_path.parent / "frames"),
                str(sb_path.parent),
            ]
            print(f"  ❌ 找不到 [{shot_id}] 的参考图")
            print(f"     已搜索目录：")
            for d in search_dirs: print(f"       {d}")
            print(f"     → 请先运行 call_image_api.py storyboard 生成分镜图")
            print(f"       或用 --frames-dir 手动指定图片目录")
            return {"status": "skipped", "reason": "reference_image not found"}

    # 提交 → 轮询 → 下载
    task_id = submit_video_task(ref_img, shot["video_prompt"], duration)
    if not task_id:
        return {"status": "failed", "reason": "submit failed"}

    video_url = poll_video_task(task_id)
    if not video_url:
        return {"status": "failed", "reason": "no video url after polling"}

    out_path = str(Path(output_dir) / f"{shot_id}.mp4")
    if download_video(video_url, out_path):
        return {"status": "ok", "path": out_path, "url": video_url}
    return {"status": "failed", "reason": "download failed"}


# ──────────────────────────────────────────────────────
# 批量生成
# ──────────────────────────────────────────────────────
def batch_generate(storyboard_json: str, output_dir: str, frames_dir: str | None,
                   only_shot_id: str | None = None):
    sb_path = Path(storyboard_json).resolve()
    if not sb_path.exists():
        print(f"❌ 找不到: {storyboard_json}")
        sys.exit(1)

    with open(sb_path, encoding="utf-8") as f:
        sb = json.load(f)

    shots = sb.get("shots", [])

    # 单帧重生成模式
    if only_shot_id:
        shots = [s for s in shots if s["shot_id"] == only_shot_id]
        if not shots:
            print(f"❌ 未找到 shot_id={only_shot_id}")
            sys.exit(1)
        print(f"\n🔄 重新生成单帧视频: {only_shot_id}")
    else:
        print(f"\n📋 {sb.get('title','未命名')}  共 {len(shots)} 镜头")
        if frames_dir:
            print(f"🖼  参考图目录: {frames_dir}")
    print()

    log = {}
    sb_modified = False

    for shot in shots:
        result = process_shot(shot, sb_path, output_dir, frames_dir)
        log[shot["shot_id"]] = result
        if result.get("status") == "ok":
            # 如果自动查找更新了 reference_image，标记需要回写
            sb_modified = True

    # 回写 storyboard.json（更新 reference_image 路径）
    if sb_modified:
        with open(sb_path, "w", encoding="utf-8") as f:
            json.dump(sb, f, ensure_ascii=False, indent=2)
        print(f"\n📝 storyboard.json 已同步更新 → {sb_path}")

    # 保存日志
    log_path = str(sb_path.parent / "generation_log.json")
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(log, f, ensure_ascii=False, indent=2)

    # 汇总
    ok_count      = sum(1 for v in log.values() if v["status"] == "ok")
    failed_shots  = [k for k, v in log.items() if v["status"] == "failed"]
    skipped_shots = [k for k, v in log.items() if v["status"] == "skipped"]

    print(f"\n{'='*55}")
    print(f"✅ 视频生成完毕：{ok_count}/{len(shots)} 成功")
    if failed_shots:
        print(f"   ❌ 失败: {failed_shots}")
        print(f"      可修改 video_prompt 后用 --shot-id 重新生成")
    if skipped_shots:
        print(f"   ⏭  跳过（无参考图）: {skipped_shots}")
        print(f"      请先运行 call_image_api.py storyboard 生成对应分镜图")
    print(f"   📋 详细日志: {log_path}")


# ──────────────────────────────────────────────────────
# CLI 入口
# ──────────────────────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="漫剧视频生成脚本（图生视频模式）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
命令说明：
  batch   批量生成所有镜头
  single  重新生成某一个指定镜头（检查点后修正用）
        """
    )
    sub = parser.add_subparsers(dest="mode", required=True)

    # batch
    pb = sub.add_parser("batch", help="批量生成所有镜头视频")
    pb.add_argument("--input",      required=True, help="storyboard.json 路径")
    pb.add_argument("--output",     required=True, help="视频输出目录")
    pb.add_argument("--frames-dir", default=None,  help="（可选）分镜图目录，默认为 storyboard/frames/")

    # single（重新生成单帧）
    ps = sub.add_parser("single", help="重新生成单个镜头视频")
    ps.add_argument("--shot-id",    required=True, help="要重新生成的 shot_id，如 S01_03")
    ps.add_argument("--input",      required=True, help="storyboard.json 路径")
    ps.add_argument("--output",     required=True, help="视频输出目录")
    ps.add_argument("--frames-dir", default=None,  help="（可选）分镜图目录")

    args = parser.parse_args()
    startup_check()

    if args.mode == "batch":
        batch_generate(args.input, args.output, args.frames_dir)
    elif args.mode == "single":
        batch_generate(args.input, args.output, args.frames_dir, only_shot_id=args.shot_id)
