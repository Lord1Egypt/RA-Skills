#!/usr/bin/env python3
"""
call_image_api.py  (v6 - 基于调试版本整理)

依赖：pip install 'volcengine-python-sdk[ark]' requests

用法：
  # 生成角色人设参考图（从脚本内 CHARACTER_PROMPTS 读取）
  python call_image_api.py characters --output ../characters/images/

  # 生成分镜图（从 storyboard.json 读取 art_style_prefix + image_prompt）
  python call_image_api.py storyboard \
      --input ./storyboard.json \
      --output ../storyboard/frames/

  # 重新生成单个镜头图（用于检查点后修正某帧）
  python call_image_api.py single \
      --shot-id S01_03 \
      --input ./storyboard.json \
      --output ../storyboard/frames/
"""

import argparse, json, os, sys, time, requests
from pathlib import Path

# ══════════════════════════════════════════════════════
#  ★ 配置区：在这里填写你的方舟 API Key
# ══════════════════════════════════════════════════════
ARK_API_KEY     = os.getenv("ARK_API_KEY", "在这里填你的方舟APIKey")
ARK_IMAGE_MODEL = "doubao-seedream-5-0-260128"

RETRY_TIMES  = 3
RETRY_SLEEP  = 5
IMAGE_SIZE   = "2K"   # 支持 1K / 2K / 4K，2K = 2560×1440，满足像素下限

# ══════════════════════════════════════════════════════
#  ★ 角色人设 Prompt 配置区
#    在阶段3（人设设定）完成后，将每个角色的图像生成 Prompt 填入此处
#    key = 角色ID（与 storyboard.json 中 characters 字段一致）
#    value = 完整英文 Prompt
# ══════════════════════════════════════════════════════
CHARACTER_PROMPTS = {
    # 示例（运行前替换为你的实际角色）：
    # "CHAR_001": (
    #     "17-year-old teenage boy, black slightly wavy short hair with loose bangs, "
    #     "dark brown eyes with golden crack patterns, lean athletic build, "
    #     "golden crystalline fracture lines on chest, wearing worn dark gray hoodie, "
    #     "black slim pants, dark sneakers, "
    #     "full body front view, white background, "
    #     "anime style, cel shading, shonen manga, high quality, masterpiece, sharp focus"
    # ),
}


# ──────────────────────────────────────────────────────
# 启动检查
# ──────────────────────────────────────────────────────
def startup_check():
    print("=" * 55)
    print("  漫剧图像生成脚本  (v6)")
    print("=" * 55)
    key_ok = ARK_API_KEY and ARK_API_KEY != "在这里填你的方舟APIKey"
    print(f"  🔑 ARK API Key  : {'✅ 已配置' if key_ok else '❌ 未配置'}")
    print(f"  🖼  图像模型    : {ARK_IMAGE_MODEL}")
    print(f"  📐 图像尺寸    : {IMAGE_SIZE}")
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
# 核心：文生图
# ──────────────────────────────────────────────────────
def ark_text2img(prompt: str, size: str = IMAGE_SIZE) -> str | None:
    """调用方舟图像生成，返回图片 URL（失败返回 None）"""
    from volcenginesdkarkruntime import Ark
    client = Ark(
        base_url="https://ark.cn-beijing.volces.com/api/v3",
        api_key=ARK_API_KEY,
    )
    for attempt in range(1, RETRY_TIMES + 1):
        print(f"    → 请求中... (第 {attempt}/{RETRY_TIMES} 次)")
        try:
            resp = client.images.generate(
                model=ARK_IMAGE_MODEL,
                prompt=prompt,
                response_format="url",
                size=size,
                watermark=False,
            )
            url = resp.data[0].url
            print(f"    ✅ 成功: {str(url)[:70]}...")
            return str(url)
        except Exception as e:
            print(f"    ❌ 第 {attempt} 次失败: {type(e).__name__}: {e}")
            if attempt < RETRY_TIMES:
                print(f"    ↩️  {RETRY_SLEEP}s 后重试...")
                time.sleep(RETRY_SLEEP)
    return None


# ──────────────────────────────────────────────────────
# 下载图片到本地
# ──────────────────────────────────────────────────────
def download_image(url: str, out_path: str) -> bool:
    try:
        r = requests.get(url, timeout=60)
        r.raise_for_status()
        Path(out_path).parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "wb") as f:
            f.write(r.content)
        size_kb = len(r.content) // 1024
        print(f"    💾 已保存 → {out_path}  ({size_kb} KB)")
        return True
    except Exception as e:
        print(f"    ❌ 下载失败: {e}")
        return False


# ──────────────────────────────────────────────────────
# 角色人设图批量生成
# ──────────────────────────────────────────────────────
def generate_characters(output_dir: str):
    if not CHARACTER_PROMPTS:
        print("⚠️  CHARACTER_PROMPTS 为空！")
        print("   请在脚本顶部的 CHARACTER_PROMPTS 字典中填入角色 Prompt。")
        print("   参考人设卡 characters/CHAR_XXX.md 中的「图像生成 Prompt」字段。")
        sys.exit(1)

    print(f"\n📂 输出目录: {output_dir}")
    print(f"🎨 将生成 {len(CHARACTER_PROMPTS)} 个角色立绘\n")

    results = {}
    for char_id, prompt in CHARACTER_PROMPTS.items():
        print(f"━━━ [{char_id}] ━━━")
        print(f"  Prompt 预览: {prompt[:80]}...")
        url = ark_text2img(prompt)
        if url:
            out_path = str(Path(output_dir) / f"{char_id}_front.png")
            if download_image(url, out_path):
                results[char_id] = {"status": "ok", "path": out_path}
                continue
        results[char_id] = {"status": "failed"}
        print(f"  ❌ {char_id} 生成失败，跳过")

    # 汇总
    ok_count = sum(1 for v in results.values() if v["status"] == "ok")
    print(f"\n{'='*55}")
    print(f"✅ 角色图生成完毕：{ok_count}/{len(CHARACTER_PROMPTS)} 成功")
    print(f"   输出目录: {output_dir}")
    if ok_count < len(CHARACTER_PROMPTS):
        failed = [k for k, v in results.items() if v["status"] != "ok"]
        print(f"   ❌ 失败角色: {failed}，可修改 Prompt 后重新运行")
    print(f"\n👀 请打开输出目录查看人设图，确认外貌是否符合预期")
    print(f"   如需调整，修改 CHARACTER_PROMPTS 后重新运行此命令")


# ──────────────────────────────────────────────────────
# 分镜图批量生成
# ──────────────────────────────────────────────────────
def generate_storyboard(storyboard_json: str, output_dir: str, only_shot_id: str | None = None):
    sb_path = Path(storyboard_json).resolve()
    if not sb_path.exists():
        print(f"❌ 找不到: {storyboard_json}")
        sys.exit(1)

    with open(sb_path, encoding="utf-8") as f:
        sb = json.load(f)

    style_prefix = sb.get("art_style_prefix", "")
    shots = sb.get("shots", [])

    # 过滤单个 shot（重新生成模式）
    if only_shot_id:
        shots = [s for s in shots if s["shot_id"] == only_shot_id]
        if not shots:
            print(f"❌ 未找到 shot_id={only_shot_id}")
            sys.exit(1)
        print(f"\n🔄 重新生成单帧: {only_shot_id}")
    else:
        print(f"\n📋 {sb.get('title','未命名')}  共 {len(shots)} 镜头")

    if not style_prefix:
        print("⚠️  storyboard.json 中 art_style_prefix 为空！")
        print("   建议在阶段3画风设定完成后填写此字段，否则各帧风格可能不统一")
        print()

    print(f"🎨 画风前缀: {style_prefix[:60]}..." if len(style_prefix) > 60 else f"🎨 画风前缀: {style_prefix or '（未设置）'}")
    print(f"📂 输出目录: {output_dir}\n")

    modified = False
    for shot in shots:
        shot_id = shot["shot_id"]
        raw_prompt = shot.get("image_prompt", "")
        if not raw_prompt:
            print(f"⚠️  [{shot_id}] 无 image_prompt，跳过")
            continue

        full_prompt = f"{style_prefix}, {raw_prompt}" if style_prefix else raw_prompt
        print(f"━━━ [{shot_id}] {shot.get('description_cn', '')[:30]} ━━━")
        print(f"  Prompt: {full_prompt[:90]}...")

        url = ark_text2img(full_prompt)
        if url:
            out_path = str(Path(output_dir) / f"{shot_id}.png")
            if download_image(url, out_path):
                shot["reference_image"] = out_path
                modified = True
                continue
        shot["reference_image"] = None
        print(f"  ❌ [{shot_id}] 生成失败")

    # 将 reference_image 路径写回 storyboard.json
    if modified:
        with open(sb_path, "w", encoding="utf-8") as f:
            json.dump(sb, f, ensure_ascii=False, indent=2)
        print(f"\n📝 storyboard.json 已更新（reference_image 路径已写入）")

    ready = sum(1 for s in sb.get("shots", []) if s.get("reference_image"))
    total = len(sb.get("shots", []))
    print(f"\n{'='*55}")
    print(f"✅ 分镜图生成完毕：{ready}/{total} 帧已就绪")
    print(f"   输出目录: {output_dir}")
    print(f"\n👀 请打开输出目录查看分镜图，确认每帧画面符合预期")
    print(f"   如有问题，用以下命令重新生成指定帧：")
    print(f"   python call_image_api.py single --shot-id <shot_id> --input {storyboard_json} --output {output_dir}")


# ──────────────────────────────────────────────────────
# CLI 入口
# ──────────────────────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="漫剧图像生成脚本",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
命令说明：
  characters  生成角色人设参考图（从脚本内 CHARACTER_PROMPTS 读取）
  storyboard  批量生成分镜图（从 storyboard.json 读取）
  single      重新生成某一个指定镜头（检查点后修正用）
        """
    )
    sub = parser.add_subparsers(dest="mode", required=True)

    # characters
    pc = sub.add_parser("characters", help="生成角色人设图")
    pc.add_argument("--output", required=True, help="图片输出目录")

    # storyboard
    ps = sub.add_parser("storyboard", help="批量生成分镜图")
    ps.add_argument("--input",  required=True, help="storyboard.json 路径")
    ps.add_argument("--output", required=True, help="分镜图输出目录")

    # single（重新生成单帧）
    pn = sub.add_parser("single", help="重新生成单个镜头图")
    pn.add_argument("--shot-id", required=True, help="要重新生成的 shot_id，如 S01_03")
    pn.add_argument("--input",   required=True, help="storyboard.json 路径")
    pn.add_argument("--output",  required=True, help="分镜图输出目录")

    args = parser.parse_args()
    startup_check()

    if args.mode == "characters":
        generate_characters(args.output)
    elif args.mode == "storyboard":
        generate_storyboard(args.input, args.output)
    elif args.mode == "single":
        generate_storyboard(args.input, args.output, only_shot_id=args.shot_id)
