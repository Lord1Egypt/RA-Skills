"""
spec_to_prompt: 读 spec.json -> 拼出给图像编辑模型 (gpt-image-1/2 系) 的中文 prompt。

设计原则:
1. 不写色板 hex —— 模型对 "必须用 #FAF4C8" 服从度差。色板交给量化阶段。
2. 让模型显式画出网格线: 后处理可以"按格取色"避开格内连续色,
   比 LANCZOS 整图缩放在格边界平均更准。色号文字仍由 Python 加。
3. 强约束 "色块化": 明确目标网格数, 当作软约束让模型自己缩放风格。
4. 风格意向 + preserve_features 直接逐句嵌入。

usage:
    python scripts/spec_to_prompt.py path/to/spec.json
    python scripts/spec_to_prompt.py path/to/spec.json -o outputs/run/image_prompt.txt
"""

import argparse
import json
from pathlib import Path


STYLE_INSTRUCTIONS = {
    "realistic": "请保留主体的明暗关系、五官细节和材质特征,看起来仍然像照片但被像素化。",
    "cartoon": "请把主体卡通化:增强边缘对比、简化阴影、轮廓清晰,适合做潮玩拼豆。",
    "flat": "请用极简的纯色色块绘制,不要渐变、不要描边、不要阴影,每个色块边界清晰。",
    "binary": "请用二值化方式绘制——只用两种主色 (主体色 + 背景色),类似黑白剪影。",
}

BACKGROUND_INSTRUCTIONS = {
    "keep": "保留原图背景。",
    "remove": "把背景替换为纯白色 (#FFFFFF),主体之外的所有像素必须是纯白,不要灰色阴影、不要渐变过渡。",
    "solid": "把背景替换为纯色 {color},主体之外的所有像素必须是这个颜色,不要渐变。",
}


def build_prompt(spec: dict) -> str:
    grid_w, grid_h = spec["grid_w"], spec["grid_h"]
    style = spec.get("style", "realistic")
    bg_mode = spec.get("background_mode", "keep")
    bg_color = spec.get("background_color")

    lines: list[str] = []

    ai_draws_grid = spec.get("ai_draws_grid", True)

    if ai_draws_grid:
        lines.append(
            f"请把这张照片重绘为一幅按 {grid_w} 列 × {grid_h} 行 (共 {grid_w * grid_h} 个方块) "
            "排列的像素画, 并且显式画出网格线。"
        )
        lines.append(
            "技术要求:\n"
            "1. 每个像素方块的内部必须是单一纯色, 没有渐变、没有描边、没有阴影。\n"
            "2. 相邻方块之间用一条浅灰色细网格线 (大约 1-2 像素宽, "
            "RGB 接近 (200, 200, 200)) 分隔。\n"
            f"3. 整张图严格按 {grid_w} 列 × {grid_h} 行等大网格排列, 网格线必须笔直、等宽。\n"
            "4. 不要在方块里写数字、色号或任何文字, 不要画格外的装饰、边框或花边。"
        )
        lines.append(
            "为什么要画网格线: 后续程序会按格扫描取色, 网格线让每格边界清晰, "
            "可以避免相邻格颜色被错混。"
        )
    else:
        lines.append(
            f"请把这张照片重绘为一幅 {grid_w} 列 × {grid_h} 行的方形像素画 "
            f"(总共 {grid_w * grid_h} 个像素方块),"
            "每个方块内部为单一纯色 (无渐变、无描边、无文字)。"
        )
        lines.append(
            "重要: 不要在画面上添加任何网格线、行列编号、坐标轴或色号文字。"
            "我只需要纯净的像素色块图本身——网格和编号将由后续程序自动加上。"
        )

    lines.append(STYLE_INSTRUCTIONS.get(style, STYLE_INSTRUCTIONS["realistic"]))

    if bg_mode == "solid" and bg_color:
        lines.append(BACKGROUND_INSTRUCTIONS["solid"].format(color=bg_color))
    else:
        lines.append(BACKGROUND_INSTRUCTIONS.get(bg_mode, BACKGROUND_INSTRUCTIONS["keep"]))

    features = spec.get("preserve_features") or []
    if features:
        bullets = "\n".join(f"  - {f}" for f in features)
        lines.append("以下视觉要素必须在像素画里清晰可辨:\n" + bullets)

    max_colors = spec.get("max_colors")
    if max_colors:
        lines.append(
            f"整张图最多使用约 {max_colors} 种不同颜色;"
            "相近颜色请合并成同一个色块,优先表达主体而不是层次。"
        )
    else:
        lines.append(
            "用尽量少的、彼此区分度高的颜色 (相近色合并),不要追求渐变层次。"
        )

    if spec.get("safety") == "kids":
        lines.append("画面应当适合儿童观看:不要血腥、恐怖、暴力或成人元素。")

    if spec.get("commercial"):
        lines.append("不要包含任何品牌 LOGO、商标或可识别的版权 IP 形象。")

    lines.append("最终输出: 仅一张 PNG 像素色块图,不要附加说明文字。")

    return "\n\n".join(lines)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("spec", help="path to spec.json")
    ap.add_argument("-o", "--output", default=None,
                    help="write prompt to file; default is print to stdout")
    args = ap.parse_args()

    spec = json.loads(Path(args.spec).read_text(encoding="utf-8"))
    prompt = build_prompt(spec)

    if args.output:
        out = Path(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(prompt, encoding="utf-8")
        print(f"[spec_to_prompt] wrote -> {out}")
    else:
        print(prompt)


if __name__ == "__main__":
    main()
