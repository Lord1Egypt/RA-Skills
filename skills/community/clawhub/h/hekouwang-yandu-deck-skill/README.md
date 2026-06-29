# hekouwang-yandu-deck-skill · 演读 DECK

**中文** · [English](README.en.md)

> GitHub: [https://github.com/huiyonghkw/hekouwang-yandu-deck-skill](https://github.com/huiyonghkw/hekouwang-yandu-deck-skill)

会勇禾口王的AI笔记 ·「演读 DECK」沉浸式演示产线与发布 Skill。

把一篇文章/选题做成**一屏一镜、可翻页、能自动播放**的 keynote 演示版网页（**暖黑** / **米白** 两套主色），自托管字体（思源黑/宋子集化 + Anthropic 打包、零 CDN、preload 治 FOUT），并一键发布到 Cloudflare Pages。

线上样例：**https://hekouwang.pages.dev**

## 示例动画版本 / Demo

最快的体验方式 —— 双击打开 **[`examples/demo.html`](examples/demo.html)**：一个**自包含、零依赖、系统字体**的最小示例，直接 `file://` 打开就能看引擎怎么动（翻页 / 自动播放 / 柱子生长 / 数字滚动 / 折线描线 / 卡片错峰）。

| 封面（数字滚动 + 标题渐变） | 流程屏（节点淡入 + 箭头描线 + stat 弹入） |
|---|---|
| ![cover](docs/demo-cover.png) | ![flow](docs/demo-flow.png) |

- **在线完整版（可翻页/自动播放）**：
  - 首页：<https://hekouwang.pages.dev>
  - 暖黑系列：<https://hekouwang.pages.dev/suanli/ep01>（`#3` 直达第 3 屏）
  - 米白系列：<https://hekouwang.pages.dev/toushi/ep01>
- `assets/templates/deck-engine-暖黑.html` / `deck-engine-米白.html` 是两套**完整引擎模板**（需起本地服务器看字体：`python3 -m http.server`）。

## 依赖

| 依赖 | 关系 | 说明 |
|---|---|---|
| **`hekouwang-content-factory`** ⭐ | **内容来源（强依赖）** | 本 Skill 是「**把内容做成翻页演示 + 发布**」的一半；**另一半（生成文章 HTML、视觉规范 V1/V2/V3、去 AI 味、合规红线）在 `hekouwang-content-factory`**。演示版的源 HTML、配色 token、字体方案都源自它。**⚠️ `hekouwang-content-factory` 是付费 Skill**（GitHub 上为 **PRIVATE 私有仓库，非授权无法 clone / 获取**；需向作者 @huiyonghkw 获取授权），本仓库不含其内容。 |
| Python 3 + `fonttools`+`brotli` | 字体子集化 | 仅发布时需要（`tools/fenv` venv，见 `SKILL.md`）。没有则回退用 `fonts/cache/` 已切好的子集。 |
| `wrangler`（Cloudflare） | 部署 | `publish.py` 调它发到 CF Pages；首次需 `wrangler login`。 |
| Anthropic Sans/Mono woff2 | 拉丁/代码字体 | 来自 `hekouwang-content-factory`（自用/演示授权）。缺失则拉丁字自动回退系统字。 |

> 只想用**引擎**（不要内容产线）：直接拷 `assets/templates/deck-engine-*.html` 当模板填内容即可，那部分零依赖、可独立使用。

## 这是什么

这是一个 [Claude Code](https://claude.com/claude-code) **Skill**，按官方 `anthropics/skills` 约定分目录组织。`SKILL.md` 是给 Agent 读的方法说明；`scripts/` `assets/` `references/` `examples/` 是可直接拷用的脚本、模板、文档与示例。

```
SKILL.md                              # 方法 + 触发词 + 防踩坑（Agent 入口）
scripts/
└── publish.py                       # 构建 dist/ → 部署 CF Pages（零三方依赖）
assets/templates/
├── deck-engine-暖黑.html             # 演示版引擎模板（数据/财经/科普暗调）
├── deck-engine-米白.html             # 演示版引擎模板（人文/方法论亮调）
└── home.html                        # 首页模板
references/
└── 系统说明.md                       # 系统说明文档
examples/
└── demo.html                        # 零依赖最小示例（双击即看）
```

> 落地铁律：`scripts/publish.py` 与 `assets/templates/home.html` 拷进项目时必须放进同一个 `演读DECK/`（publish.py 用 `SELF/home.html` 找首页源）。

## 安装

把本仓库放进 `~/.claude/skills/hekouwang-yandu-deck-skill/`：

```bash
git clone git@github.com:huiyonghkw/hekouwang-yandu-deck-skill.git ~/.claude/skills/hekouwang-yandu-deck-skill
```

之后在 Claude Code 里说「把这篇做成演示版 / 加一期演读 / 发 hekouwang」等即会自动加载。

## 核心能力

- **演示版引擎**（零依赖 CSS+JS）：全屏一屏一镜、←/→/空格/点击/触屏翻页、自动播放、进场动画（卡片错峰 / 柱子生长 / SVG 描线 / 数字滚动 / 幽灵章节号）、`fit()` 自适应、`#N` 深链、`prefers-reduced-motion` 友好。
- **两套主色**：暖黑（数据控制台）/ 米白（编辑人文），引擎 JS 主题无关。
- **字体自托管**：思源黑 4 字重 + 宋按用字子集化（各 ~180KB），Anthropic Sans/Mono 打包，全站零外链；preload + 强缓存消除首屏字重跳变。
- **一键发布**：`python3 publish.py`，MANIFEST 加一行即加一期，CF Pages 干净 URL。

> 配套图文/视频产线见 `hekouwang-content-factory`。

## License

本仓库代码（演示版引擎模板、`publish.py`、`demo.html`、`home.html`、`SKILL.md` 等）以 **MIT** 开源，见 [LICENSE](LICENSE)。注意：

- **`hekouwang-content-factory` 是独立的付费 Skill，其内容不在本仓库**，不受本许可覆盖。
- 思源黑体/思源宋体（Noto Sans/Serif SC）为 SIL OFL 开源字体，本仓库**不含字体文件**，自行获取时遵循其 OFL。
- Anthropic Sans/Mono 为专有字体，本仓库不含，使用前自行确认授权。
