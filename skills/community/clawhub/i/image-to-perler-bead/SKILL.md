---
name: image-to-perler-bead
description: "This skill should be used when the user wants to convert a photo into a perler bead / Hama bead / 熨斗豆 / 拼豆 pattern. Triggers include - 照片转拼豆, 拼豆图纸, perler bead pattern, 熨斗豆图纸, Hama beads, 把照片做成拼豆, 像素化照片做手工, 拼豆设计图, bead art pattern. Generates printable HTML grid, PNG preview, color-coded material list with bead counts, and optional JSON data. Works for portraits, cartoons, logos, pet photos, and any image the user wants to recreate as a bead craft."
agent_created: true
---

# 照片转拼豆图纸 Skill

将任意照片像素化并映射到 5mm 拼豆调色板，生成可打印的 HTML 图纸、PNG 预览和材料清单。

## When to Use

Use this skill whenever the user wants to:
- 把照片变成拼豆（perler beads / Hama 熨斗豆）手工图纸
- 看到 `*.jpg / *.png` 并要求生成拼豆/熨斗豆/手工图纸/马赛克图
- 询问拼豆颜色清单 / 买多少豆 / 怎么把图转成拼豆

Do not use when:
- 用户想要的是普通马赛克艺术（不是拼豆手工）→ 用普通图像处理 skill
- 用户想做十字绣/钩针等其他工艺 → 走对应工艺 skill
- 用户只想要缩小/像素化预览，不需要珠子图纸

## Workflow

1. **确认输入**：从用户消息或附件拿到图片路径。如果用户只说"帮我转拼豆"但没提供图，反问要哪张图（优先用最近上传的附件）。
2. **确认参数**：除非用户明确指定，否则用默认（宽度 29、标准 fit 模式、不抖动、不显示编号）。如果用户提供了细节（如"做 50 颗方板"、"加上编号"），按用户说的来。
3. **调用脚本**：

   ```bash
   python <skill>/scripts/perler_converter.py <输入图> --width <N> --output <输出目录>
   ```

   脚本必须用绝对路径（基于用户的工作目录）调用。Python 解释器用隔离 venv：
   `C:/Users/lenovo/.workbuddy/binaries/python/envs/default/Scripts/python.exe`（Windows 路径，使用 Git Bash 时写作 `/c/Users/lenovo/.workbuddy/binaries/python/envs/default/Scripts/python.exe`）。

4. **检查输出**：脚本会生成 3 个文件到 `--output` 目录：
   - `<name>_pattern.html` — 可打印的彩色网格图纸 + 材料清单（**主要交付物**）
   - `<name>_preview.png` — 像素化预览图
   - 控制台输出的材料清单摘要
5. **呈现给用户**：用 `present_files` 把 HTML 和 PNG 一起呈现给用户。HTML 会自动在浏览器中打开预览。
6. **后续建议**：告诉用户如何打印、用哪号钉板、预计多少颗珠子。详见 `references/crafting_guide.md`。

## Common Parameters

| 参数 | 作用 | 默认 |
|------|------|------|
| `--width N` | 图纸宽度（珠子数） | 29 |
| `--height N` | 图纸高度（不指定则按比例） | 自动 |
| `--mode fit/cover` | 缩放：fit 整图缩放 / cover 裁剪填满 | fit |
| `--dither` | Floyd-Steinberg 抖动（颜色过渡更自然） | 关 |
| `--codes` | 在图上显示颜色编号 | 关 |
| `--no-grid` | 不显示网格线 | 显示 |
| `--cell N` | HTML/PNG 中每格像素大小 | 18 |
| `--title "..."` | 图纸标题 | "拼豆图纸" |
| `--json` | 同时输出 JSON 数据 | 否 |

参数细节参考 `--help` 或 `references/advanced.md`。

## Tunable Recommendations

根据用户意图选择参数：

- **"想做个钥匙扣"** → `--width 20`
- **"做杯垫大小"** → `--width 29`（最常用默认）
- **"做大幅挂画"** → `--width 50` 或更大
- **"颜色要鲜艳"** → 加 `--dither`
- **"我要按编号买豆"** → 加 `--codes`
- **"要填满方形板"** → 用 `--mode cover` + 同时指定 `--height`
- **"做 Logo，颜色要准"** → 不开抖动，`--mode cover`

## Bundled Resources

- `scripts/perler_converter.py` — 主转换脚本（图像加载、颜色量化、HTML/PNG 生成、JSON 输出、CLI 全套）
- `references/palette.md` — 48 色调色板完整参考、对应常见品牌、与 Artkal/Perler/Hama 色号映射
- `references/crafting_guide.md` — 选图建议、尺寸选择、买豆量、熨烫工艺、常见问题
- `references/advanced.md` — 编程式调用、批量处理、自定义调色板、JSON 数据二次开发

加载 references 的触发条件：
- 用户问"这个色用什么豆" / "对应哪个品牌" → 加载 `palette.md`
- 用户问"怎么熨" / "需要买多少" / "温度怎么调" → 加载 `crafting_guide.md`
- 用户问"能写代码 / 批量 / 改调色板" → 加载 `advanced.md`

## Dependencies

- Python 3.10+
- Pillow (`PIL`) — 脚本会 import，如果未安装会报清晰错误并提示 `pip install Pillow`

如果用户的 Python 环境没有 Pillow，**先安装再调用**。优先安装到隔离 venv：
```bash
C:/Users/lenovo/.workbuddy/binaries/python/versions/3.13.12/python.exe -m venv C:/Users/lenovo/.workbuddy/binaries/python/envs/default
C:/Users/lenovo/.workbuddy/binaries/python/envs/default/Scripts/python.exe -m pip install Pillow
```

## Output Summary

每次执行会输出：
- 1 个 HTML（彩色图纸 + 材料清单，可打印）
- 1 个 PNG（像素化预览图）
- 1 个控制台材料清单表格（按用量降序）
- （可选）1 个 JSON

**总是把 HTML 和 PNG 用 `present_files` 呈现给用户**，这是主交付物。然后用一段话告诉用户：
- 用了多少颗珠子、几种颜色
- 推荐用什么尺寸的钉板
- 是否需要调参数（如果颜色过多或图纸过小）

## Edge Cases

- **颜色用得太多（>30 种）** → 建议加大尺寸或合并颜色
- **图太暗 → 全是黑灰** → 建议用户调整原图对比度后再来
- **图很糊** → 直接做，但提醒成品可能细节丢失
- **人形/正方形构图** → 建议 `--mode cover` + 指定 `--height`，避免上下/左右多出白边
