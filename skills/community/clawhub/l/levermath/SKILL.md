---
name: levermath
description: 面向中国数学教师的可交互 HTML 数学幻灯片模板。用户提到制作高中数学课件、伪 PPT、几何图形演示、KaTeX 公式、JSXGraph 动点、分步淡入、关键帧或单文件离线放映时使用；帮助 AI 从教学目标出发制作、构建并验证 LeverMaTH 课件。
---

# LeverMaTH：数学教师的 HTML 幻灯片

此仓库同时是可复用的源码模板和 AI 使用说明。先阅读仓库根 `AGENTS.md` 与 `docs/` 中的相关文档，再制作课件。不要把技能安装目录当作工作区直接改动：复制模板到用户指定的工作区，在副本中创作。

## 开始之前

1. 确认年级、教材章节、课时目标、学生已有知识与课堂时长；内容和交互服务于教学，而非追求动画数量。
2. 先设计所有帧的内容、尺寸和讲解顺序，再安排 `data-k` 跨帧变形与 `data-step` 入场。
3. 确认主题与照片来源。如果需要真实课堂照片，AI 无法自己拍摄，须由用户提供且确认公开使用权限；不要用网上图片或示意图无声替代。
4. 确认目标工作区已经存在且不会被覆盖，再复制 `templates/basic/` 与引擎所需源码过去。保留用户手动编辑的成果。

## 课件机制

- `src/engine/deck.ts`：左侧缩略图、全屏和 PgUp/PgDn；`stage.ts`：1280×720 舞台与帧状态；`morph.ts`：`data-k` 同名元素间过渡；`enter.ts`：`data-enter` + `data-step` 按教师按键逐项展示；`interactive.ts`：按 `data-interactive` 注册 JSXGraph；`math.ts`：按 `data-tex` 渲染 KaTeX。
- 数学变量、表达式和下标全部使用 KaTeX，例如 `<span data-tex="F_1"></span>`；不要用 Unicode 下标、普通文本斜体凑公式。
- 帧内淡入默认不自动串联：初始展示第一步，PgDn 展示下一步，全部放完才翻页；PgUp 回上一帧时展示上一帧的全部步骤。交互图默认静止，拖动或点击按钮才动。同一帧里已显示元素需要平移，使用 [`data-move-step`](docs/intra-frame-motion.md)，不是 `data-enter`。
- 静态图可用 TikZ 生成 SVG；需要拖动点、轨迹和实时读数时，用 JSXGraph 的 SVG renderer。做图前读 [`docs/interactive-geometry.md`](docs/interactive-geometry.md)。

## 制作与构建

参考 `templates/basic/frames/*.html` 创建新的帧，并从独立的 `main.ts` 加载。可从两个示例学习：

- `examples/origami-ellipse/`：折纸生成椭圆，包含作品照片、可拖动几何图、GeoGebra 和 TikZ 源。
- `examples/vector-p-norm/`：p-范数公式、数值比较、滑块控制单位圆。

使用 Bun 安装依赖，在课件目录完成后通过 Vite 生成自包含 `index.html`。需要联网只发生在**第一次安装依赖**；构建后的课件单文件可离线播放。每套课件的字体子集须按最终用字重新制作：操作见 [`docs/fonts-and-licenses.md`](docs/fonts-and-licenses.md)，不要复用其他课件的中文字集。

仓库自带的构建命令与示例输出见 [README](README.md)。对于正式课堂课件，至少验证以下场景：

1. 缩略图导航与全屏；PgDn 先逐步揭示，再切帧；PgUp 回看时内容完整。
2. KaTeX 字形和数学上下标；JSXGraph 拖动、按钮和读数；两种动画不会在切帧时自动运行。
3. 全部图形、字体与照片均位于生成的 HTML 中，断网和换一台电脑后仍可加载；演示电脑优先用现代版 Chrome/Edge，旧浏览器兼容模式不受支持。
4. 如需发布源码或示例，先读 `THIRD_PARTY_NOTICES.md`。单文件的“开源许可与字体声明”也须保留。

## 交付边界

把改动、验证结果、缺字或依赖问题告诉用户。不要擅自修改私人偏好文件、上传课件或将内容提交到 Git：提交、发布、上传均需分别获得明确授权。
