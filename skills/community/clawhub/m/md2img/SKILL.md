---
name: md2img
description: Convert Markdown (inline text or a `.md` file path) into a single PNG image using local code (Markdown -> HTML -> headless browser screenshot). Use when the user asks for a PNG image output from Markdown content or a `.md` file.
metadata:
  openclaw:
    emoji: 🖼️
    requires:
      bins: [python3]
---

# md2img

## 目标
把 Markdown 渲染成 PNG，并确保最终只返回/输出 **一张**图片。

## 支持的输入
1. 行内 Markdown 文本（用户直接贴内容）
2. Markdown 文件路径（用户提供类似 `/path/to/input.md`，且以 `.md` 结尾）

## 输出契约（必须遵守）
1. 用户指定的 `output` 会被解释为“最终 PNG 的文件路径”。
2. 如果用户给的是目录路径（不以 `.png` 结尾），则在该目录下输出默认文件名：`md2img.png`。
3. 本 skill 使用 headless 浏览器的 `fullPage=True` 截图，确保最终输出为 **单张** PNG（不分页）。

## 移动端（固定宽度更好看）
当你主要用于手机端预览时，建议设置浏览器渲染宽度，从而让文字换行/表格布局符合移动端比例。

1. 使用参数：`--image-width <px>`
2. 推荐宽度：
   - `375`（iPhone 常见宽度）
   - `390`（Android 常见宽度）
   - `414`（大屏 iPhone 常见宽度）
3. 示例（在虚拟环境中运行）：
   - `./.venv/bin/python scripts/md_to_png.py --input <in.md> --output <out.png> --image-width 375`

## 暗黑模式（best-effort）
脚本使用 `@media (prefers-color-scheme: dark)` 做了样式适配，所以暗黑效果取决于 headless 浏览器/系统的深色偏好。

1. 默认：跟随系统/浏览器的 `prefers-color-scheme`（best-effort）
2. 如你希望“无论系统如何都强制深色”，当前实现还没有 CLI 参数；你可以告诉我你的期望，我可以继续加 `--theme dark|light` 之类的参数来强制渲染。

## 转换流程（When invoked）
1. （依赖准备）若缺少依赖，请在项目内用虚拟环境避免系统级 `pip install`（PEP 668 外部托管环境）：
   - `python3 -m venv .venv`
   - `source .venv/bin/activate`
   - `python -m pip install -U pip`
   - `python -m pip install -U markdown playwright bleach pygments`
   - `python -m playwright install chromium`
2. 解析输入来源，并决定是否需要临时目录：
   - 若用户给了 `.md` 路径：直接使用该路径作为 `input_md_path`，**不创建/不删除临时文件**
   - 否则（行内 Markdown 文本）：
     - 创建临时目录：`tmp_dir=$(mktemp -d)`
     - 把用户提供的 Markdown 文本写入 `$tmp_dir/input.md`
     - 令 `input_md_path=$tmp_dir/input.md`
3. 解析 `output`：
   - 若 `output` 以 `.png` 结尾：把它当作最终 PNG 文件路径
   - 否则：把它当作目录路径，并输出到 `output/md2img.png`
4. 渲染为单张 PNG（不分页）：
   - 必须在虚拟环境中运行脚本（避免再次触发系统级 pip/环境限制）：
     - 推荐：`./.venv/bin/python scripts/md_to_png.py --input $input_md_path --output <final_png_path> --image-width <移动端宽度像素(如375)>`
     - 或先 `source .venv/bin/activate` 再用 `python scripts/md_to_png.py ...`
   - 脚本内部会把 Markdown -> HTML（包含 HTML 清洗、可选语法高亮、并默认把 `<img>` 图片资源 base64 内联），再用无头 Chromium 截图 `fullPage=True`，并等待字体/资源加载，确保只有一张 PNG
5. 临时文件清理与返回结果：
   - 若输入为“行内 Markdown 文本”（即创建了 `tmp_dir`），转换结束后执行删除：`rm -rf "$tmp_dir"`
   - 返回最终 PNG 的路径（不返回临时目录）

## 失败条件（出错要明确）
- `scripts/md_to_png.py` 执行失败：需要报错并包含你实际执行的命令与以下其一，方便用户排查：
  - 行内 Markdown 场景：`$tmp_dir/input.md`
  - `.md` 文件路径场景：用户提供的 `.md` 路径

## 示例
### 例 1：行内 Markdown -> 单张 PNG
用户：把下面 Markdown 转成图片，并输出到 `/tmp/out.png`
```markdown
# Hello

This is a **Markdown** example.
```

Agent steps：
1. 写入临时文件 `$tmp_dir/input.md`
2. 运行 `./.venv/bin/python scripts/md_to_png.py --input $tmp_dir/input.md --output /tmp/out.png`
3. 删除临时目录：`rm -rf "$tmp_dir"`

### 例 2：`.md` 文件路径 -> 单张 PNG
用户：把文件 `/tmp/input.md` 转成图片，输出到 `/tmp/images/`

Agent steps：
1. 直接使用 `/tmp/input.md` 为 `input.md`
2. 运行 `./.venv/bin/python scripts/md_to_png.py --input /tmp/input.md --output /tmp/images/md2img.png`
3. 不删除 `/tmp/input.md`（它来自用户提供）

