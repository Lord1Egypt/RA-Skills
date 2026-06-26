#!/usr/bin/env python3
"""
Image Assets Resize — 图片物料尺寸延展

以参考KV/海报/拍脸图为输入，调用 gpt-image-2 或 Nano Banana 模型，
按目标规格批量生成精确尺寸的图片文件，交付前AI自检文字裁切、元素完整性等问题。

流程:
  1. 查询平台规格 → 确定目标尺寸
  2. 直接调用 gpt-image-2 edit 模式生成（原图直接作为输入，无需 AI 视觉分析）
  3. 极微缩放至精确尺寸（如有必要）
  4. AI 自检验证（可选）
  5. 规范命名保存

用法:
  python generate_image.py -i 参考图.png -p wechat-cover -s "五一活动"
  python generate_image.py -i 参考图.png -p wechat-cover,douyin-cover -s "五一福利" -q high
  python generate_image.py --list-platforms
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Optional

try:
    from PIL import Image
except ImportError:
    Image = None

SCRIPT_DIR = Path(__file__).parent.resolve()
sys.path.insert(0, str(SCRIPT_DIR))

from spec_manager import (
    get_spec, list_platforms, record_generation, learn_from_feedback, load_brand,
    save_custom_spec, delete_custom_spec, parse_inline_spec, load_custom_specs,
)
from backend import (
    create_backend,
    calc_gpt_size,
    load_config,
    save_config,
    show_config_info,
    run_setup_wizard,
    get_backend_name,
    BACKEND_LABELS,
)
from utils import resize_image, encode_image_base64, build_filename


# ── Prompt 构建 ──────────────────────────────────────────────


def build_edit_prompt(platform_name: str, width: int, height: int, scene: str = "", extra: str = "") -> str:
    """构建 edit prompt

    两种模式：
      - 完整版（默认）：保留原图所有元素包括文案，仅调整构图适配
      - 纯净版：去除原图文案/LOGO，只保留角色/背景
    通过 --extra-prompt 中的关键词触发纯净版：
      "不要logo"、"去掉文案"、"无文字"、"干净"、"clean" 等
    """
    # 检测是否请求纯净版
    _clean_keywords = ["不要logo", "不要带logo", "去掉logo", "去除logo", "无logo",
                        "不要文案", "不要文字", "去掉文字", "去除文字", "无文字",
                        "不要装饰", "去掉装饰", "纯净", "简洁", "干净", "净版", "clean"]
    is_clean = any(kw in extra.lower() for kw in _clean_keywords) if extra else False

    if is_clean:
        prompt = (
            f"以这张参考图为基准，适配生成一张【{platform_name}】，尺寸{width}x{height}。"
            f"仅保留角色和背景场景，去除所有文字、LOGO、图标和装饰元素，保持画面干净简洁。"
        )
    else:
        prompt = (
            f"以这张参考图为基准，适配生成一张【{platform_name}】，尺寸{width}x{height}。"
            f"严格保留原图所有视觉元素：角色、背景、所有文字、图标和装饰——一个都不能少。"
            f"仅调整元素位置来适配新比例，延伸的区域用背景纹理填充即可，不要添加任何新内容。"
        )
    if scene:
        prompt += f" 场景：{scene}。"
    if extra:
        prompt += f" 额外要求：{extra}"
    return prompt


def build_generate_prompt(
    platform_name: str, width: int, height: int, scene: str = "",
    brand_name: str = "", style_hint: str = "",
) -> str:
    """无参考图时使用 text-to-image 模式"""
    parts = [f"生成一张【{platform_name}】营销图片，尺寸{width}x{height}"]
    if scene:
        parts.append(f"，场景主题：{scene}")
    if brand_name:
        parts.append(f"，品牌：{brand_name}")
    if style_hint:
        parts.append(f"，风格：{style_hint}")
    return "。".join(parts)


# ── 图片生成（通过 backend 抽象层）─────────────────────────


def get_backend():
    """从配置加载后端实例"""
    config = load_config()
    if not config:
        print("\n⚠ 首次使用请先运行 --setup 配置 API\n", file=sys.stderr)
        sys.exit(1)
    return create_backend(config), config


# ── AI 自检 ──────────────────────────────────────────────────


def verify_image(image_path: str) -> dict:
    """检查生成图片是否存在文字裁切等质量问题"""
    if not os.path.exists(image_path):
        return {"passed": False, "issues": ["文件不存在"]}

    api_key = os.environ.get("GPT_IMAGE2_API_KEY", "")
    if not api_key:
        return {"passed": True, "issues": ["跳过：无 API 密钥"]}

    try:
        img_b64 = encode_image_base64(image_path)

        check_prompt = (
            "Check this marketing image for:\n"
            "1) TEXT CROPPING: Is any text partially cut off at edges? (CRITICAL)\n"
            "2) ELEMENT COMPLETENESS: Are any elements clipped?\n"
            "3) OVERALL QUALITY: Professional looking?\n"
            "Reply PASS or list specific issues."
        )

        import urllib.request
        import urllib.error

        body = json.dumps({
            "model": "gpt-4o",
            "messages": [{
                "role": "user",
                "content": [
                    {"type": "text", "text": check_prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_b64}"}},
                ],
            }],
            "max_tokens": 500,
            "temperature": 0.3,
        }).encode("utf-8")

        base_url = os.environ.get("GPT_IMAGE2_BASE_URL", "https://api.openai.com/v1")
        endpoint = f"{base_url.rstrip('/')}/chat/completions"

        req = urllib.request.Request(
            endpoint, data=body,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )

        with urllib.request.urlopen(req, timeout=60) as resp:
            raw = resp.read().decode("utf-8")

        resp_data = json.loads(raw)
        content = resp_data["choices"][0]["message"]["content"]

        passed = "PASS" in content.upper() and "crop" not in content.lower()
        issues = []
        if not passed:
            for line in content.split("\n"):
                line = line.strip().strip("- ").strip()
                if line and len(line) > 5:
                    issues.append(line[:200])

        return {"passed": passed, "issues": issues or (["未通过"] if not passed else [])}

    except Exception as e:
        return {"passed": True, "issues": [f"自检异常: {e}"]}


# ── 命名规范 ──────────────────────────────────────────────────


# ── 主流程 ──────────────────────────────────────────────────


def run_pipeline(
    image_path: Optional[str],
    brand_name: str,
    platforms: list[str],
    scene: str,
    quality: str,
    output_dir: str,
    backend,
    dry_run: bool = False,
    version: int = 1,
    verify: bool = False,
    extra_prompt: str = "",
):
    """流水线：edit/generate → 缩放 → 保存"""
    results = []

    for platform_key in platforms:
        spec = get_spec(platform_key)
        if not spec:
            print(f"    ⚠ 未知平台: {platform_key}，跳过")
            continue

        tw, th = spec["width"], spec["height"]
        platform_name = spec["name"]

        # 自动学习：内联格式的规格自动保存为自定义规格
        inline_spec = parse_inline_spec(platform_key)
        if inline_spec:
            from spec_manager import _gen_custom_key
            ck = _gen_custom_key(inline_spec["name"], inline_spec["width"], inline_spec["height"])
            custom_all = load_custom_specs()
            if ck not in custom_all:
                save_custom_spec(ck, inline_spec)
                print(f"\n    📖 已学习新平台规格 [{ck}]")
                print(f"       后续可直接用 -p {ck} 调用，无需再写尺寸")

        # 计算 GPT 尺寸
        gpt_size_str, scale = calc_gpt_size(tw, th)
        # 构建 prompt
        if image_path and os.path.exists(image_path):
            prompt = build_edit_prompt(platform_name, tw, th, scene, extra_prompt)
        else:
            prompt = build_generate_prompt(platform_name, tw, th, scene, brand_name)

        # 输出路径
        filename = build_filename(scene, platform_name, tw, th, version)
        final_output = os.path.join(output_dir, filename)

        print(f"\n    ── {platform_name} ({tw}×{th}) ──")

        if scale != 1.0:
            print(f"    GPT尺寸: {gpt_size_str}")
            if scale < 0.95:
                print(f"    等比缩小: {(1/scale):.2f}x → 目标尺寸")
            else:
                print(f"    缩放至: {tw}×{th}")
        else:
            print(f"    尺寸: {tw}×{th}")

        print(f"    输出: {final_output}")

        if dry_run:
            print(f"    Prompt: {prompt}")
            results.append({"platform": platform_key, "success": True, "dry_run": True})
            continue

        # 生成
        os.makedirs(output_dir, exist_ok=True)
        print(f"    生成中... ", end="", flush=True)

        if image_path and os.path.exists(image_path):
            gen = backend.edit(image_path, prompt, final_output, gpt_size_str, quality, 600)
        else:
            gen = backend.generate(prompt, final_output, gpt_size_str, quality, 600)

        print(f"{gen['time_elapsed']}s")
        gen["platform"] = platform_key

        if not gen["success"]:
            print(f"    ✗ 生成失败: {gen['error']}")
            results.append(gen)
            continue

        # 缩放至精确目标尺寸（如有必要）
        if scale != 1.0:
            tmp = final_output + ".tmp.png"
            if os.path.exists(final_output):
                os.replace(final_output, tmp)
                ok = resize_image(tmp, final_output, tw, th)
                os.unlink(tmp)
                if not ok:
                    print(f"    ⚠ 缩放失败")
            else:
                print(f"    ⚠ 未找到生成文件")
        else:
            ok = True

        if os.path.exists(final_output):
            file_size = os.path.getsize(final_output) / 1024
            print(f"    ✓ 保存完成 ({file_size:.0f} KB)")
        else:
            print(f"    ✗ 保存失败")

        # 可选自检
        if verify and os.path.exists(final_output):
            print(f"    AI自检... ", end="", flush=True)
            v_result = verify_image(final_output)
            if v_result["passed"]:
                print(f"✓ 通过")
            else:
                print(f"⚠ 发现问题")
                for issue in v_result["issues"][:3]:
                    print(f"      - {issue}")

        # 记录
        record_generation(brand_name, platform_key, scene, prompt, final_output)
        results.append(gen)

    return results


def main():
    parser = argparse.ArgumentParser(
        description="内容营销图片延展生成工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("-i", "--image-path", help="参考KV/海报路径（直接作为 edit 输入）")
    parser.add_argument("-b", "--brand", default="default", help="品牌名称")
    parser.add_argument("-p", "--platforms", default="", help="目标平台Key，逗号分隔（如 wechat-cover,douyin-cover）")
    parser.add_argument("-s", "--scene", help="活动/场景名称")
    parser.add_argument("-q", "--quality", default="medium", choices=["low", "medium", "high"])
    parser.add_argument("-o", "--output-dir", default="output", help="输出目录")
    parser.add_argument("--version", type=int, default=1, help="版本号（用于文件名）")
    parser.add_argument("--verify", action="store_true", help="生成后 AI 自检验证")
    parser.add_argument("--extra-prompt", default="", help="额外指令。添加元素：\"顶部加'五一狂欢'文字\"；去除元素(纯净版)：\"不要带logo\" / \"去掉文案\"")
    parser.add_argument("--dry-run", action="store_true", help="预览不生成")
    parser.add_argument("--setup", action="store_true", help="初始化配置向导（选择模型、设置API）")
    parser.add_argument("--show-config", action="store_true", help="显示当前配置")

    # 工具命令
    parser.add_argument("--list-platforms", action="store_true", help="列出所有平台规格")
    parser.add_argument("--get-spec", metavar="PLATFORM", help="查询平台规格")
    parser.add_argument("--show-brand", metavar="BRAND", help="查看品牌学习数据")
    parser.add_argument("--feedback", nargs=4, metavar=("BRAND", "IDX", "RATING", "TEXT"),
                        help="提交反馈评分")
    parser.add_argument("--add-spec", nargs=3, metavar=("NAME", "WIDTH", "HEIGHT"),
                        help="添加自定义平台规格，如 --add-spec 我的平台 1200 800")
    parser.add_argument("--remove-spec", metavar="KEY",
                        help="删除自定义平台规格，如 --remove-spec custom_我的平台_1200x800")
    parser.add_argument("--list-custom", action="store_true", help="列出所有自定义规格")
    parser.add_argument("--base64", action="store_true", help="云端模式：结果中包含 base64 编码图片，供 OpenClaw 直接展示")

    args = parser.parse_args()

    # ── 工具命令 ──
    if args.list_platforms:
        print(f"{'Platform Key':30s} {'Target Dim':15s} {'Ratio'}")
        print("-" * 60)
        for p in list_platforms():
            dim = f"{p['width']}×{p['height']}"
            print(f"{p['key']:30s} {dim:15s} {p['ratio']}")
        return

    if args.get_spec:
        spec = get_spec(args.get_spec)
        if spec:
            print(json.dumps(spec, ensure_ascii=False, indent=2))
        else:
            print(f"未知平台: {args.get_spec}")
        return

    if args.show_brand:
        print(json.dumps(load_brand(args.show_brand), ensure_ascii=False, indent=2))
        return

    if args.feedback:
        learn_from_feedback(args.feedback[0], int(args.feedback[1]), args.feedback[3], int(args.feedback[2]))
        print(f"✓ 反馈已记录至 '{args.feedback[0]}'")
        return

    # ── 自定义规格管理 ──
    if args.add_spec:
        name, w, h = args.add_spec[0], int(args.add_spec[1]), int(args.add_spec[2])
        key = f"custom_{''.join(c if c.isalnum() else '_' for c in name).strip('_').lower()}_{w}x{h}"
        from math import gcd
        g = gcd(w, h)
        spec = {
            "name": name, "width": w, "height": h,
            "safe_area": {"top": 0, "bottom": 0, "left": 0, "right": 0},
            "format": ["png", "jpeg"], "max_size_mb": 10,
            "ratio": f"{w//g}:{h//g}",
            "note": f"自定义规格（{name}）",
        }
        save_custom_spec(key, spec)
        print(f"✓ 已添加自定义规格: [{key}] {name} {w}×{h}")
        print(f"  后续可使用 -p {key} 或 -p \"{name}:{w}x{h}\" 调用")
        return

    if args.remove_spec:
        if delete_custom_spec(args.remove_spec):
            print(f"✓ 已删除自定义规格: {args.remove_spec}")
        else:
            print(f"未找到自定义规格: {args.remove_spec}")
        return

    if args.list_custom:
        custom = load_custom_specs()
        if not custom:
            print("暂无自定义规格")
            return
        print(f"{'Key':35s} {'Name':20s} {'Dim':15s} {'Ratio'}")
        print("-" * 75)
        for key, spec in custom.items():
            dim = f"{spec['width']}×{spec['height']}"
            print(f"{key:35s} {spec['name']:20s} {dim:15s} {spec.get('ratio','?')}")
        return

    # ── 配置相关 ──
    if args.setup:
        run_setup_wizard()
        return

    if args.show_config:
        show_config_info()
        return

    # ── 校验 ──
    if not args.platforms or not args.scene:
        parser.print_help()
        print("\nError: --platforms/-p 和 --scene/-s 为必填参数")
        sys.exit(1)

    if not args.dry_run:
        backend_obj, backend_config = get_backend()
        backend_name = get_backend_name(backend_config)
        print(f"  模型: {BACKEND_LABELS.get(backend_name, backend_name)}")

    if Image is None:
        print("WARNING: Pillow 未安装，将跳过缩放步骤")

    platforms = [p.strip() for p in args.platforms.split(",") if p.strip()]

    print(f"\n{'='*55}")
    print(f"  Image Assets Resize — 图片物料尺寸延展")
    print(f"  场景: {args.scene}")
    if args.image_path:
        print(f"  参考图: {args.image_path}")
    print(f"  质量: {args.quality}")
    print(f"  平台: {', '.join(platforms)}")
    if args.verify:
        print(f"  AI自检: 开启")
    print(f"{'='*55}")

    if args.extra_prompt:
        print(f"  额外指令: {args.extra_prompt}")

    results = run_pipeline(
        image_path=args.image_path,
        brand_name=args.brand,
        platforms=platforms,
        scene=args.scene,
        quality=args.quality,
        output_dir=args.output_dir,
        backend=backend_obj if not args.dry_run else None,
        dry_run=args.dry_run,
        version=args.version,
        verify=args.verify,
        extra_prompt=args.extra_prompt,
    )

    if not args.dry_run:
        ok = sum(1 for r in results if r.get("success"))
        total = len(results)
        print(f"\n{'='*55}")
        print(f"  ✓ 完成: {ok}/{total}")
        result_list = []
        for r in results:
            if r.get("success"):
                path = r.get("output_path", "")
                print(f"    ✓ {path}")
                result_list.append({
                    "platform": r.get("platform", ""),
                    "output_path": path,
                    "success": True,
                })
            else:
                result_list.append({
                    "platform": r.get("platform", ""),
                    "error": r.get("error", "未知错误"),
                    "success": False,
                })
        print(f"{'='*55}")

        # JSON 结果（供 agent/OpenClaw 解析）
        import json as _json
        _output = {
            "tool": "image-assets-resize",
            "success": ok == total and total > 0,
            "total": total,
            "ok": ok,
            "results": result_list,
            "output_dir": args.output_dir,
            "scene": args.scene,
        }
        # 云端模式：附带 base64 图片，供 Agent 直接展示给用户
        if args.base64:
            for r in _output["results"]:
                if r.get("success") and r.get("output_path") and os.path.exists(r["output_path"]):
                    r["image_base64"] = encode_image_base64(r["output_path"])
        print(f"\n## Result\n{_json.dumps(_output, ensure_ascii=False)}")

    if args.dry_run:
        return
    if any(not r.get("success") for r in results):
        sys.exit(1)


if __name__ == "__main__":
    main()
