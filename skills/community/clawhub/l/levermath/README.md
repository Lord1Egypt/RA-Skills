# LeverMaTH
> 注：本 skill 由 AI 重度协助生成。请在使用前仔细阅读，确保理解其中的工作流程、注意事项和许可要求。

**面向中国数学教师、由 AI 协助制作的可交互 HTML 幻灯片模板。** 源码按帧、引擎、主题和图形拆分，放映时构建为一个离线可打开的 HTML 文件。

"Lever"取撬动教学之意；**L**ever**M**a**TH** 是将 **HTML** 倒序藏入名称的文字趣味。它不是 PowerPoint 编辑器，也不自动生成教学内容：课堂目标、例题与讲授节奏仍由教师决定。

> **Agent 使用或开发前**：先读 [SKILL.md](SKILL.md)、[AGENTS.md](AGENTS.md) 以及 [`docs/`](docs/) 下相关文档。先设计完整课件，再决定哪些信息分步出现。Agent 不应把已安装的技能目录当作工作区直接修改，更不应未经许可提交、发布或上传。

## Why this?

- **画面是一组状态，不只是死页。** 同名 `data-k` 元素可跨帧平滑移动；左侧保留竖向帧总览，演示时可全屏。
- **节奏由教师控制。** `data-enter`、`data-step` 配合 PgDn 展示下一步；PgUp 回上一帧时补齐内容（意味着可以配合翻页笔），交互动图默认静止。
- **数学内容可交互。** KaTeX 渲染变量与公式；JSXGraph 展示可拖动点、几何构造与实时读数；静态几何图可以先用 TikZ 画成 SVG。
- **电脑之间好传。** Vite 构建时把脚本、样式、许可说明、示例字集与图片装进单个 HTML。离线播放不用 TeX Live 和本地开发环境；较旧的浏览器可能不支持，建议用 Chrome 或 Edge 放映。

## 交给 AI 的用法

把仓库作为 Agent Skill 安装后，例如这样描述任务：

> 用 LeverMaTH 做一份《椭圆及其标准方程》的高中数学课件。先确认一课时的教学目标，提出帧的内容与交互顺序，再制作；公式用 KaTeX，折纸过程可拖动，淡入由 PgDn 分步触发。最后交付可离线播放的 HTML。

根目录 [`SKILL.md`](SKILL.md) 是 skill 入口；本仓库本身即供 AI 阅读的模板仓库。兼容 `SKILL.md` 的 Agent 可以从仓库中读取技能，也可将仓库复制到该 Agent 的技能目录。**不要在公开仓库里写本机用户名、工作区路径或私人偏好文件路径。** 如需单独维护工作区列表，只写进被 `.gitignore` 忽略的 `USAGES.local.md`。

## 本地开发

先安装 [Bun](https://bun.sh/)，在项目目录执行：

```bash
bun install
bun run dev
```

构建模板及两个示例：

```bash
bun run build
bun run build:ellipse
bun run build:norm
```

| 命令 | 输出 |
| --- | --- |
| `bun run build` | `dist/index.html`，基础模板 |
| `bun run build:ellipse` | `dist/examples/origami-ellipse/index.html`，椭圆折纸示例 |
| `bun run build:norm` | `dist/examples/vector-p-norm/index.html`，p-范数示例 |
| `bun run dev:ellipse` | 本地预览椭圆示例 |
| `bun run dev:norm` | 本地预览范数示例 |

构建示例时会尝试重做各自的字体子集，要求本地有 `uv`、`fonttools`、`brotli`，以及可读取的 Noto Serif SC 和 Latin Modern 原字体文件。缺少字体时，用脚本参数或 `LEVERMATH_NOTO_FONT`、`LEVERMATH_LATIN_FONT` 指定来源，见 [字体文档](docs/fonts-and-licenses.md)。仓库已有示例子集，但改字后必须重裁；不得用默认子集冒充覆盖整套课件的字体。

开发源码与发布的 HTML 是两种用途：发布物只发送对应的 `index.html`，不要求接收者安装 Bun。发布源码或公开示例时，还需要考虑 [第三方声明](THIRD_PARTY_NOTICES.md)。

## 目录

```text
levermath/
├─ SKILL.md                    AI 工作流程入口
├─ AGENTS.md                   仓库自身的使用与权限边界
├─ README.md                   当前文档
├─ LICENSE                    项目代码的 MIT 许可
├─ THIRD_PARTY_NOTICES.md     依赖与字体的来源及许可
├─ templates/basic/            四帧基础模板，含帧内平移预设与示例字体子集
├─ src/engine/                 帧、翻页、动画、公式和交互图的公共实现
├─ src/styles/                 通用舞台与侧栏样式
├─ src/themes/                 可选主题（纸白·朱砂仅为示例）
├─ examples/origami-ellipse/   折纸与椭圆示例
├─ examples/vector-p-norm/    向量 p-范数示例
├─ scripts/                    构建与字体辅助脚本
├─ docs/                       设计、交互与字体说明
└─ licenses/                   第三方许可文本
```

## 制作新课件时的标记

```html
<h1 data-k="title">椭圆的定义</h1>
<p data-enter="up" data-step="2">按 PgDn 后呈现这一条</p>
<span data-tex="|MF_1|+|MF_2|=2a"></span>
<div data-interactive="ellipse"></div>
```

- `data-k="title"`：跨帧相同身份的元素会进行变形过渡；别把同一个元素同时交给 `data-enter`。
- `data-enter="up"` + `data-step="2"`：教师按键后才揭示，默认**不自动连播**。
- `data-tex`：数学变量、关系、下标与公式全部交给 KaTeX，避免 Unicode 拼接。
- `data-interactive`：对应 `registerInteractive()` 中注册的 JSXGraph 图形；图形默认不自动播放。
- `data-move-step="2"`、`data-move-x="240"`、`data-move-y="0"`：当前帧中已显示的元素按 PgDn 后平移，先加速再减速，始终可见；参见 [帧内平移](docs/intra-frame-motion.md)。

舞台为 1280×720。正式授课须检查标题、正文与图内标签是否足够大，切勿靠不断缩字容纳过多内容；具体步骤见 [帧内动画](docs/enter-animation.md) 与 [交互式几何](docs/interactive-geometry.md)。

## 示例

[椭圆及其标准方程](examples/origami-ellipse/README.md)：折纸引入 → 折痕包络 → 交点轨迹 → 数学定义；同时保留 GeoGebra 文件和 TikZ 源用于查证构造。[向量范数示例](examples/vector-p-norm/README.md)：定义 → 数值计算 → 可拖动的单位圆。

## 已知限制

单文件播放应使用现代 Chrome 或 Edge。360 浏览器如落入 IE 兼容模式，可能不执行 ES module，页面交互会失效；即使进入“极速模式”，内核过旧也可能缺少所需浏览器 API。请在**正式授课的电脑上**提前断网试播。项目不承诺固定的最低 Chrome 版本；具体浏览器兼容性应以实际试播为准。

## LICENSE

项目代码采用 [MIT License](LICENSE)。

各字体各自保留许可证，详见 [第三方声明](THIRD_PARTY_NOTICES.md)。

