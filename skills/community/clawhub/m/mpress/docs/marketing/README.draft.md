> **归档存根**：此文件为 v1 草稿，已归档；正式 README 见仓库根目录 [`README.md`](../../README.md)。
> 本草稿中涉及的仓库名与安装命令均已同步校正为 `mpress`，避免误读或误抄。最新完整功能与实测数据请参阅根目录 README。

# mpress (v1 草稿归档)

<!-- badge：渠道上线后取消注释，把 shxuk 换成你的 GitHub handle -->
<!-- [![skills.sh](https://skills.sh/b/shxuk/mpress)](https://skills.sh/shxuk/mpress) -->
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE)
[![Node](https://img.shields.io/badge/node-%3E%3D18-green.svg)](package.json)
[![Dependencies](https://img.shields.io/badge/deps-2-brightgreen.svg)](package.json)

> **把 Markdown 一句话排成微信公众号图文，连同封面一起推进草稿箱。**
>
> mpress 是一个开源的 **Agent Skill + 命令行工具**：吃 Markdown 或纯文本，吐微信公众号能直接用的内联 HTML（公众号会剥离外链 CSS，所以样式必须全部内联），生成 1800×766 封面，需要时把正文图片一起上传并写入草稿箱。可以只本地生成看效果（不联网、不需要密钥），也可以直连公众号一步到位。
>
> 适合有固定品牌规范的企业新媒体运营、做个人 IP 的自媒体、以及批量产出图文的内容团队；不适合想自动群发、或希望 AI 改写正文的人。

<div align="center">
  <img src="./assets/preview-components.png" alt="编辑部风格组件实测：刊头、结论条、指标卡、双轨对照、步骤阶梯在手机端的实际排版效果" width="460" />
</div>

---

## 30 秒上手

```bash
# 方式 A：装进 AI 助手（Claude Code / Cursor / Codex / OpenClaw 等）
npx skills add shxuk/mpress
```

装完直接对 AI 说人话：

> 把 `文章.md` 排成公众号版式，封面用深色，然后推到草稿箱。

```bash
# 方式 B：只用命令行，本地生成看效果（不联网、不需要任何密钥）
git clone https://github.com/shxuk/mpress.git
cd mpress
npm i
node scripts/wechat.mjs gen docs/样例/style-overview.md
# → 生成 body.html（可直接在浏览器打开预览）+ layout.json
```

```bash
# 方式 C：推到公众号草稿箱（需要 AppID / AppSecret + IP 白名单，见下方配置）
node scripts/wechat.mjs push 文章.md --source-url https://shxuk.cn/xxx
```

| 你想要什么 | 用哪个命令 | 需要什么 |
|---|---|---|
| 先看排版效果 | `gen` | 只要 Node ≥ 18 |
| 生成封面头图 | `gen --head` | 只要 Node ≥ 18 |
| 推进草稿箱 | `push` | 公众号 AppID / AppSecret + IP 白名单 |
| 让 AI 全自动 | `npx skills add` 后直接说需求 | 一个支持 Skill 的 AI 工具 |

---

## 它解决什么问题

写公众号最烦的从来不是写，是后面那两小时：

- **排版**：Markdown 粘进公众号后台，样式全丢；要用 135 / 秀米重新摆一遍，每次换主题还要重调字号和间距。
- **图片**：正文图要一张张另存、再一张张上传，顺序还容易乱；封面另做一张 1800×766。
- **搬运**：AI 帮你写完了稿，你还得手动复制、粘贴、传图、存草稿。
- **一致性**：团队里每个人排出来的东西都不一样，品牌规范形同虚设。

这个项目把这三件事变成一次工具调用：**样式由一份 CSS 统一控制，图片自动上传并替换成微信地址，草稿直接落到你后台。**

---

## 能做什么

### 1. 把任意 Markdown 排成杂志风图文

支持标题、列表、表格、引用、代码块、图片，并额外提供一套结构化组件（见下表）。版式的所有颜色、间距、字体都由 [`assets/theme.css`](./assets/theme.css) 控制，换品牌色只改这一份文件。

### 2. 生成公众号封面（1800×766）

内置封面模板，按标题自动排版；`gen --head` 本地出图，`push` 时自动上传。封面版式规范见 [`docs/封面模板规范.md`](./docs/封面模板规范.md)。

### 3. 一步推进草稿箱

自动完成：正文图片上传 → 图片地址替换为微信 CDN → 封面上传 → 新建或更新草稿 → 返回 `media_id`。**只写草稿，不群发。**

### 4. 原生 SVG 折叠

公众号不支持自定义 JS，折叠面板用双层半透明 SVG 渐隐实现，在微信内可原生展开收起，无弹窗、无跳转。实现见 [`components/svg-fold.mjs`](./components/svg-fold.mjs)。

---

## 版式组件

10 个卡片组件 + 4 类内建样式，全部用 `:::` 块语法书写（**这是写进文章里的语法，不是 README 的渲染语法**，所以下面用表格说明，完整示例见 [`templates/editorial.md`](./templates/editorial.md)）：

| 组件 | 用途 | 一眼看懂的例子 |
|---|---|---|
| `kicker` | 刊头导读条：系列名 + 期号 | `给决策者的 GEO 运营指南 · CH.1/7` |
| `lead` | 结论先行区，深底加粗 | 「字多不看：GEO 是 SEO 的加法」 |
| `metrics` | 大数字指标卡，等宽表格排列 | `15% / 3.2万+ / 8.4 次` |
| `versus` | 双轨对照，用 `---` 分两栏 | 行业老大 vs 挑战者 |
| `steps` | 阶梯式流程 | 被检索 → 被引用 → 被推荐 → 被定义 |
| `dossier` | 移动优先档案卡，替代挤扁的宽表 | 五大站外阵地 |
| `verdict` | 金句判词，段落收口 | 「传统搜索选整页，AI 搜索选段落」 |
| `qa` | 一问一答卡组 | 预算审批前必问两题 |
| `checklist` | 带方块编号的行动清单 | 三句底牌 |
| `follow` | 文末关注 / 引流卡 | 「关注我，或直接发消息」 |
| 数字标题 | `## 01 标题` 自动渲染成方块数字双栏标题 | — |
| 四色提示块 | `> TIP` / `> NOTE` / `> WARNING` / `> IMPORTANT` | — |
| SVG 折叠 | `::: details[标题]` 微信内可展开 | — |
| 仓库卡 | `::: githubcard owner/repo` | — |

> 组件截图在 [`assets/components/`](./assets/components)，逐张都是手机实机效果。

---

## 不能做什么

这个工具不负责：

- **自动群发**。只写草稿箱，发布必须你在公众号后台手动点。
- **改写正文**。它只做排版和发布，不动你的文字。
- **数据统计 / 留言管理 / 用户画像**。这些请用公众号后台。
- **绕过微信的限制**。没有微信支付权限的公众号，正文里的 `<a>` 外链会被微信剥离，工具会提前列出受影响的链接，但无法改变这个规则。
- **排版设计本身**。组件是固定的，想要新样式要改 CSS 或加组件。

---

## 工作原理

```text
Markdown ──▶ 解析（markdown-it）──▶ 组件渲染 + theme.css 内联（juice）
        ──▶ body.html + layout.json ──▶ [push] 图片上传 / 封面合成 / 草稿写入
```

三步：**解析 → 内联渲染 → （可选）发布**。前两步纯本地，第三步才联网。

退出码：`2` 凭证问题 · `3` IP 白名单 · `4` 图片 · `5` 结构 · `6` 网络。

---

## 和其他方案比

| | 本项目 | 135 编辑器 / 秀米 | 手工复制粘贴 |
|---|---|---|---|
| 产出 | 内联 HTML + 草稿箱条目 | 富文本，需手动同步到公众号 | 一篇排版好的图文 |
| AI 可直接调用 | ✅ Skill / CLI | ❌ 只能在浏览器里点 | ❌ |
| 版式一致性 | 一份 CSS 控制全站 | 模板多，但每人可自由改 | 每次都不一样 |
| 图片处理 | 自动上传并替换地址 | 部分支持 | 一张张手动 |
| 封面 | 自动生成 1800×766 | 需另做 | 需另做 |
| 学习成本 | 一条命令 | 低（可视化） | 零，但最慢 |
| 收费 | 开源免费（MIT） | 订阅制 | 免费但费人 |

> 135 / 秀米的可视化编辑确实更强，模板也更多。本项目的优势在**可编程、可被 AI 调用、样式可版本化**——适合把排版当成流水线而不是手工活的场景。

---

## 配置

只需两项，且只在你用 `push` 时才需要：

| 变量 | 必填 | 说明 |
|---|---|---|
| `WECHAT_APP_ID` | push 必填 | 微信开发者平台「基础信息」里的 AppID |
| `WECHAT_APP_SECRET` | push 必填 | 同一页面的 AppSecret |
| `WECHAT_WORK_DIR` | 否 | 产物与草稿状态目录，默认 `~/.wechat-article/work` |
| `WECHAT_CREDENTIALS` | 否 | 凭证文件路径；默认读技能目录下的 `.env` 或 `credentials` |
| `WECHAT_BRAND` | 否 | 封面/关注卡上的品牌名 |
| `WECHAT_COVER_TEMPLATE` | 否 | 封面模板，默认 `e` |

凭证读取顺序：环境变量 → `WECHAT_CREDENTIALS` 指定文件 → 技能目录 `.env` → 技能目录 `credentials` → `~/.config/wechat/credentials`。

**一次性的微信后台配置**（只做一次）：

1. 公众号后台 →「设置与开发」→「开发接口管理」→ 按提示跳转到**微信开发者平台**。

   <img src="./assets/wechat-dev-step1.png" alt="微信公众平台开发管理迁移通知" width="600" />

2. 在开发者平台拿到 **AppID** 与 **AppSecret**，并把当前机器的**外网出口 IP** 加进「API IP 白名单」。

   <img src="./assets/wechat-dev-step2.jpg" alt="微信开发者平台 AppID 与 IP 白名单配置" width="460" />

> ⚠️ 凭证只从环境变量或本地文件读取，仓库 `.gitignore` 已忽略 `.env` 与 `credentials`。**不要把 AppSecret 提交到任何仓库。**

---

## 常见问题

### 需要公众号的什么权限？

需要已认证公众号的开发者权限，拿到 AppID / AppSecret，并把运行机器的出口 IP 加进 IP 白名单。已认证的订阅号、服务号都可以；个人主体未认证订阅号没有草稿接口权限。

### 会不会自动群发？

不会。工具只创建或更新草稿，群发必须你在公众号后台手动确认。

### 必须联网吗？可以先看效果吗？

可以。`gen` 模式完全本地渲染，不联网、不需要密钥，产出 `body.html` 直接在浏览器打开就是手机版效果。

### AppSecret 安全吗？

工具只从环境变量或本地凭证文件读取，不写日志、不上传、不落库；仓库里没有任何用户凭据。风险点在你自己的机器，不在工具。

### 排版不满意怎么改？

改 [`assets/theme.css`](./assets/theme.css) 一处即可影响全部组件；想换封面版式改 `templates/template-*.html`。也可以把你的偏好告诉 AI，让它改 CSS。

### 正文里的链接为什么变成纯文本了？

微信会剥离没有支付权限账号的外链。工具在推送前会列出受影响的链接并提示，但无法绕过。

### 支持哪些 Markdown 语法？

标准 Markdown（标题、列表、表格、引用、代码块、图片、粗斜体）加本文档前述的 `:::` 组件语法。注意：标注为 `mermaid` 的代码围栏会被原样保留并计数，**不会**渲染成图片。

### 和 135 / 秀米是什么关系？

互补。它们是可视化编辑器，适合单人精修；本项目是流水线，适合"AI 写完 → 直接出稿 → 进草稿箱"。可以先用本项目排，再进编辑器微调。

---

## 案例

<!-- 只写真实发生过的，数字可追溯；暂时没有就删掉本节和下面两条，不要编。 -->

- **编辑部风格 2.0**：一套组件覆盖刊头、结论、指标、对照、阶梯、档案、判词、问答、清单、关注卡，用于 GEO 系列长文。样例见 [`docs/样例/geo-editorial-case.md`](./docs/样例/geo-editorial-case.md)。
- **个人博客转公众号**：Markdown 原稿 → 公众号图文，【待填：一篇 N 字文章，排版耗时从 X 分钟降到 Y 分钟】。

---

## 项目事实

| 项 | 值 |
|---|---|
| Skill 版本 | `6.0.0`（`SKILL.md`） |
| npm 包版本 | `1.1.0` |
| 许可 | MIT |
| 运行时 | Node ≥ 18 |
| 依赖 | 2 个：`markdown-it`、`juice` |
| 产出 | `body.html`、`layout.json`、（可选）封面 PNG、草稿箱条目 |
| 封面尺寸 | 1800×766 |
| 退出码 | `2` 凭证 · `3` 白名单 · `4` 图片 · `5` 结构 · `6` 网络 |
| 不做 | 群发、正文改写、数据统计 |
| 支持平台 | Windows / macOS / Linux（Node 环境） |

---

## 给 AI Agent 的速览

```text
名称：mpress
类型：Agent Skill + CLI
作用：把 Markdown/纯文本排成微信公众号内联 HTML，生成 1800×766 封面，可推送到公众号草稿箱
何时使用：用户说"公众号排版 / 微信图文 / 推文排版 / 排成公众号格式 / 生成封面图 / 推到草稿箱 / 一键发布到公众号"
何时不用：用户要改写文章内容；用户要自动群发；用户没有公众号或开发者权限
入口：SKILL.md；CLI 为 scripts/wechat.mjs（gen / push）
依赖：Node >= 18，仅 markdown-it 与 juice，无需构建
离线可用：是（gen 模式不联网、不需要密钥）
```

---

## 仓库结构

<details>
<summary>展开查看</summary>

```text
mpress/
├── SKILL.md                 # 给 AI Agent 的技能规范（目录站只读这个）
├── assets/
│   ├── theme.css            # 全部组件样式，品牌化只改这里
│   ├── default-cover.png    # 默认封面底图
│   ├── head-base.jpg        # 头图底图
│   ├── components/          # 11 张组件手机实机截图
│   └── preview-components.png
├── components/
│   ├── cards.mjs            # 卡片与结构化语法渲染
│   └── svg-fold.mjs         # 原生 SVG 折叠
├── scripts/
│   ├── wechat.mjs           # 核心 CLI：gen / push
│   └── build-preview.mjs    # 本地无头 Chrome 截图
├── templates/
│   ├── editorial.md         # 全组件真实语料范例
│   └── template-*.html      # 封面/头图合成模板
├── docs/
│   ├── 封面模板规范.md
│   ├── 规范/                # VISUAL-SYSTEM / SVG-FOLD / MATERIALS
│   └── 样例/                # 真实排版长文样例
└── package.json
```

</details>

---

## 文档

| 文档 | 内容 |
|---|---|
| [`SKILL.md`](./SKILL.md) | AI Agent 读取的技能规范与形态映射表 |
| [`docs/规范/VISUAL-SYSTEM.md`](./docs/规范/VISUAL-SYSTEM.md) | 视觉系统：字号、间距、色彩、栅格 |
| [`docs/规范/SVG-FOLD.md`](./docs/规范/SVG-FOLD.md) | SVG 折叠的实现约束 |
| [`docs/规范/MATERIALS.md`](./docs/规范/MATERIALS.md) | 素材与图片规范 |
| [`templates/editorial.md`](./templates/editorial.md) | 所有组件的完整用法 |

---

## 更新日志

- `6.0.0` 编辑部风格 2.0：10 个卡片组件、原生 SVG 折叠、封面模板。
- `1.1.0` 新增 `gen --head` 本地封面生成，`push` 支持草稿更新。

## 贡献

欢迎 issue 和 PR。最想要的反馈：**你的公众号在哪个环节卡住了**——排版、图片、封面还是草稿写入。带着文章样例来提 issue 最好。

## License

[MIT](./LICENSE)
