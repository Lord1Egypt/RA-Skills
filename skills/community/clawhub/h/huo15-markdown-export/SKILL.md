---
name: huo15-markdown-export
displayName: 火一五排版发布技能
description: 火一五排版发布技能 / 火一五 markdown 排版 / 火一五 PDF 导出 / 火一五出版 / 火一五发布 / huo15-markdown-export — 【青岛火一五】markdown 一键导出 PDF / Word / HTML / 长图 / 公众号 inline。**12 主题**默认 **apple-tech(苹果科技风,大字 hero + 紧字距 + 黑白蓝 + 大留白,默认主题)**,其他 11 套:typora-newsprint 报纸 / typora-night 暗色 / github / academic / 微信 / 小红书 / huo15-brand 品牌 / anthropic-doc Anthropic 文档 / editorial-magazine 杂志 / manuscript-book 书稿 / tufte-handout Tufte 边注。Node + markdown-it + Puppeteer + qrcode。与 office-doc 互补(它走公文,本 skill 走 md 视觉美学)。v0.4.2:加 apple-tech 默认 + 修 YAML frontmatter 错乱渲染 + 强化触发词。v0.4.1:反 Type 3 字体修复(PDF 浅灰看不清);v0.4.0:抽 _tokens.css + DESIGN.md 团队规范(8 大设计范式 + 反 AI Slop / Type 3 红线)。capability detection 集成 enhance:md-share/md-publish 输出 JSON,AI chain 调 enhance_share_file 拿公网 URL 发企微/钉钉/微信;无 enhance 独立可跑。触发词:火一五排版发布、火一五排版发布技能、火一五排版、火一五出版、火一五发布、火一五markdown、火一五PDF、火一五导出、排版发布、导出PDF、导出Word、md转PDF、md转Word、md2pdf、md2docx、Typora、长图、小红书、朋友圈长图、微信公众号、博客导出、复盘、changelog、版本对比、品牌报告、发到企微、发给客户、分享链接、公网链接、卡片预览、二维码、苹果科技风、Apple 风、科技风、技术博客、产品文档、品牌故事、深度长文、小说、长篇随笔、研究报告、数据分析、教学讲义、Anthropic 文档风、杂志体、书稿体、Tufte 边注。
version: 0.4.4
aliases:
  - 火一五排版发布技能
  - 火一五排版发布
  - 火一五排版
  - 火一五排版技能
  - 火一五出版技能
  - 火一五出版
  - 火一五发布技能
  - 火一五发布
  - 火一五Markdown
  - 火一五Markdown技能
  - 火一五Markdown排版发布
  - 火一五PDF导出
  - 火一五PDF导出技能
  - 火一五PDF
  - 火一五导出
  - 火一五Typora替代
  - 火一五多端发布技能
  - 火一五美化排版
  - 火一五分享文档
  - 火一五长图技能
  - 火一五二维码PDF
  - 火一五苹果科技风
  - 火一五Apple风
  - 苹果科技风排版
  - markdown 渲染
  - markdown 导出
  - md2pdf
  - md2docx
  - md2image
  - md2wechat
  - md-publish
dependencies:
  npm-packages:
    - markdown-it
    - puppeteer
    - katex
    - juice
    - highlight.js
  optional-binaries:
    - pandoc        # 仅 md2docx 必需
    - weasyprint    # 仅 --engine pandoc 走 weasyprint 路线时
---

# 火一五 Markdown 视觉渲染管线 v0.1.0

> Typora 不需要复刻——它的能力本来就是开源拼装的。这个 skill 把同一套拼装做成 AI 可调用的版本。

**愿景:** 加速企业向全场景人工智能机器人转变
**理念:** 打破信息孤岛,用一套系统驱动企业增长

---

## 〇、与 `huo15-openclaw-office-doc` 的边界(必读)

| 维度 | huo15-openclaw-office-doc | huo15-markdown-export(本 skill) |
|---|---|---|
| 输入 | 自然语言指令(写合同/写 PRD) | 已有的 markdown 文件 |
| 引擎 | python-docx + reportlab(结构化直出) | markdown-it + Puppeteer + Pandoc |
| 适用 | 合同 / PRD / 会议纪要 / 故障报告等**结构化业务公文** | 技术博客 / 复盘 / 营销文案 / 客户报告等**视觉化 markdown** |
| 主题 | 一套企业公文规范 | 7 套(报纸风/暗色/学术/公众号/小红书/品牌等) |
| 多端 | docx / PDF | docx / PDF / HTML / 长图 / 公众号 inline / live preview |

**选择规则**:用户给"目的+主题"让你**写**新文档 → office-doc;用户给一份**已有的 .md** 让你"导出/渲染/换主题/做长图" → 本 skill。

---

## 一、能干什么(7 个工具一图)

```
input.md ──┬──► md2pdf.sh        ──► input.pdf      Chromium 打印,7 主题
           │     └─ md2pdf-puppet.js  (推荐)
           │     └─ pandoc engine     (可选,需 weasyprint/xelatex)
           │
           ├──► md2docx.sh       ──► input.docx     Pandoc + reference.docx 模板
           │
           ├──► md2html.js       ──► input.html     单文件自包含,可邮件可离线
           │
           ├──► md2image.js      ──► input.png      1080px 长图(小红书/朋友圈)
           │
           ├──► md2wechat.js     ──► input.wechat.html  juice 内联,粘到公众号编辑器
           │
           ├──► md-preview.js    ──► http://localhost  改文件自动 reload + 主题热切换
           │
           └──► md-diff.sh <from> <to>  ──► changelog.pdf   git ref 之间的变更报告
```

---

## 二、最小可用流程

```bash
# 1. 第一次用先装依赖
bash scripts/install-deps.sh

# 2. 用样例文件试一发
node scripts/md2pdf-puppet.js examples/sample.md             # → examples/sample.pdf
node scripts/md2html.js       examples/sample.md             # → examples/sample.html
node scripts/md2image.js      examples/sample.md             # → examples/sample.png(小红书)
node scripts/md2wechat.js     examples/sample.md             # → examples/sample.wechat.html

# 3. 实时预览
node scripts/md-preview.js    examples/sample.md             # 浏览器开 http://127.0.0.1:7777
```

---

## 三、主题选择决策树(给 AI 用)

> v0.4.0 起 11 套主题分两大流派阵营:**信息密集**(给信息读者)/ **视觉沉浸**(给阅读者)。
> 设计规范完整版见 [`themes/DESIGN.md`](themes/DESIGN.md)。

### 默认 / 通用首选

| 用户场景关键词 | 选哪个 | 用什么脚本 |
|---|---|---|
| "苹果风 / 科技风 / 产品发布稿 / 默认就行" | **`apple-tech`** ⭐ v0.4.2 默认 | `md2pdf` 或 `md2html` |

### 信息密集类(短段落 + 列表 + 代码)

| 用户场景关键词 | 选哪个 | 用什么脚本 |
|---|---|---|
| "技术博客 / 长文随笔 / 个人复盘 / 报纸感" | `typora-newsprint` | `md2pdf` 或 `md2html` |
| "技术博客 / **产品文档 / Anthropic 风 / Stripe 风** / 行业标杆审美" | **`anthropic-doc`** ⭐ v0.4.0 | `md2html` 或 `md2pdf` |
| "GitHub / 开源 / API 文档" | `github` | `md2pdf` |
| "夜间阅读 / 投影 / 暗色" | `typora-night` | `md2html` |
| "学术论文 / IEEE / 投稿初稿" | `academic` | `md2pdf` |
| "公司报告 / 客户提案 / 内部周报 / 带页眉页脚" | `huo15-brand` | `md2pdf` |
| "changelog / release notes / 版本对比" | `huo15-brand` | `md-diff` |

### 视觉沉浸类(长段落 + 节奏 + 留白)

| 用户场景关键词 | 选哪个 | 用什么脚本 |
|---|---|---|
| "**品牌故事 / 商业杂志 / 深度长文 / 访谈**" | **`editorial-magazine`** ⭐ v0.4.0 | `md2pdf` 或 `md2html` |
| "**小说 / 长篇随笔 / 思考长文 / 沉浸阅读**" | **`manuscript-book`** ⭐ v0.4.0 | `md2pdf` |
| "**研究报告 / 数据分析 / 教学讲义 / 论证型长文**" | **`tufte-handout`** ⭐ v0.4.0 | `md2html`(右挂边注需 ≥1100px 宽屏) |

### 多端发布类(目标编辑器特殊)

| 用户场景关键词 | 选哪个 | 用什么脚本 |
|---|---|---|
| "微信公众号 / 推文" | `wechat` | `md2wechat`(juice 内联化) |
| "小红书 / 朋友圈 / 长图文" | `xiaohongshu` | `md2image`(1080px PNG) |

**用户没说就默认** `apple-tech`(苹果科技风,通用 + 极简 + 黑白蓝 + 大留白,适合 90% 场景)。
**做技术文档无脑选** `anthropic-doc`(2026 年行业主流审美)。

---

## 四、关键参数速查

### `md2pdf-puppet.js`
```bash
node scripts/md2pdf-puppet.js <input.md> [output.pdf] \
  --theme typora-newsprint     # 11 选 1(见 §三 决策树)
  --paper A4                   # A4 / Letter / A3 / A5
  --margin 18                  # 四边等距 mm(默认 18)
  --header "我的文档"          # 自定义页眉(huo15-brand 主题已内置)
  --footer "{pageNumber} / {totalPages}"
  --print-urls                 # 链接后追加 (URL) 文本
  --no-mermaid                 # 跳过 mermaid 等待加速
```

### `md2docx.sh`(需先装 pandoc)
```bash
bash scripts/md2docx.sh <input.md> [output.docx] \
  --no-toc                              # 不要目录
  --reference templates/reference.docx  # 自定义模板
```

### `md2image.js`
```bash
node scripts/md2image.js <input.md> [output.png] \
  --theme xiaohongshu          # 默认 xiaohongshu
  --width 1080                 # 画幅宽度
  --scale 2                    # 倍清(2 = retina)
```

### `md-diff.sh`
```bash
bash scripts/md-diff.sh <from-ref> <to-ref> [output.pdf] \
  --theme huo15-brand          # 默认 huo15-brand
  --repo /path/to/git/repo     # 默认当前目录
```

---

## 五、AI 调用模式(集成到对话流)

### 模式 A:一步导出
> 用户:"把这份分析报告导成 PDF 给我"
> AI:Bash → `bash scripts/md2pdf.sh /tmp/report.md /tmp/report.pdf --theme huo15-brand`

### 模式 B:导出 + 转发(联动 huo15-wecom)
> 用户:"复盘报告导成 PDF 发到运营群"
> 1. AI 写 `report.md` 到 `/tmp`
> 2. AI 调本 skill 导 PDF → `/tmp/report.pdf`
> 3. AI 调 `huo15-wecom` 发文件到目标群

### 模式 C:多端并行(一份 md 多种产出)
> 用户:"这篇文章我要发公众号 + 小红书 + 个人博客"
> AI 并行:
> - `md2wechat.js article.md` → 公众号粘贴版
> - `md2image.js article.md --theme xiaohongshu` → 小红书长图
> - `md2html.js article.md --theme typora-newsprint` → 博客 HTML

### 模式 D:AI 改主题
> 用户:"主题再暖一点,标题大一点"
> AI 用 Edit 工具直接改 `themes/typora-newsprint.css` 的 `--accent` 与 `h1 font-size`,**不需要写新脚本**——这是本 skill 的元能力。

### 模式 E:版本对比 PDF
> 用户:"v1.2 到 v1.3 都改了什么,出个 PDF 给客户"
> AI:`bash scripts/md-diff.sh v1.2.0 v1.3.0 release-notes.pdf --theme huo15-brand`

### 模式 F:企微/钉钉/微信对话渲染送达(harness 思维,**最常用**)
> 用户(在企微对话框):"把这份复盘渲染成 PDF 发给我"
> 1. AI 调 `bash scripts/md-share.sh report.md --mode pdf --label "Q1 复盘报告"`(默认 `--prefer file`)
> 2. AI 拿到 stdout 的 JSON,看到 `files[0].path = /tmp/.../report-20260505.pdf` + 3 个 `next_actions`
> 3. **priority=1 send_file_to_channel**:AI 看当前会话有哪个 `*_send_file` / `*_upload_file` 工具(`wecom_send_file` / `wechat_send_file` / `dingtalk_send_file` 等),**直接发文件到对话框**——用户在企微/钉钉/微信里看到的是带预览的文件消息,点开下载
> 4. **priority=2 share_via_public_url(fallback)**:send_file 类工具都不可见 / 文件 > 25MB / 用户明确说"给我链接" → 才调 `enhance_share_file` 拿公网 URL。**收到 URL 后检查 host**:含 `localhost:18789` 就不要发(用户看 404 — 见 §八踩坑 §14),降级 priority=3
> 5. **priority=3 local_path(降级)**:把 `file.path` 告诉用户(终端 / SSH 场景)
> **用户明确要链接**:加 `--prefer link` 反转顺序,先拿 URL 再降级到发文件

### 模式 F 变体:用户明确要分享链接
> 用户:"给我个公网链接发给客户,链接形式"
> AI:`bash scripts/md-share.sh report.md --mode pdf --label "..." --prefer link`
> → JSON.next_actions 的 priority=1 变成 `share_via_public_url`,AI 调 `enhance_share_file` 拿 URL 发出

### 模式 G:发布 + 多端 + 自动归档(v0.3.0,**复盘场景首选**)
> 用户:"把 Q1 复盘**发布**出去,我可能要发企微 + 朋友圈 + 邮件"
> AI:`bash scripts/md-publish.sh report.md --slug q1-summary --label "Q1 复盘"`(默认 mode=all)
> → 一次渲染 4 端产物 + 写归档 `~/knowledge/huo15/<日期>-<slug>.md` + JSON.post_share_actions
> → 4 个 file 各调一次 `enhance_share_file` 拿 URL → AI 用 Edit 把 URL 回写到 KB 归档 frontmatter `share_urls:`
> → 组装"多版本菜单"消息回当前会话(PDF / 长图 / HTML / 公众号 inline)— **用户自己**决定转发哪个,不替用户广播
> 加 `--with-qr` 触发"二阶段二维码":AI 用 PDF URL 二刷 `md2pdf-puppet --qr-url <url>` 出打印版

### 模式 H:卡片预览(v0.3.0)
> 用户:"发个链接给同事,要在企微对话框里直接看到标题+摘要预览"
> AI:`md2html.js` 生成 HTML(默认从 markdown 抽 H1 + 首段作 OG title/description)→ `enhance_share_file` → 发企微
> 同事看到带卡片预览的链接(微信/企微/Slack/Twitter 都支持 OG)

### 模式 I:线下纸质 ↔ 线上文档(v0.3.0)
> 用户:"客户提案打印 50 份发线下,客户能扫码看在线版"
> 两阶段:① `md-publish.sh proposal.md --mode pdf --with-qr` 拿 PDF URL ② `md2pdf-puppet --qr-url <PDF URL> --qr-label "扫码看完整在线版"` 二维码进每页页脚
> 用户打印 → 客户扫码 → 跳 enhance 公网链接看高保真 PDF

---

## 六、自定义主题(给 AI 的)

用户说"我要 X 风格" → AI 直接改 CSS,**不要重写脚本**:

1. **先读** [`themes/DESIGN.md`](themes/DESIGN.md)(8 大设计范式 + 红线清单 + 命名规范)
2. 复制最相近的主题到新文件:`cp themes/typora-newsprint.css themes/<my-theme>.css`
3. 改 `:root` 中的 **token override**(差异化变量,如 `--font-body` / `--color-accent` / `--measure` / `--leading`)— **不要复制 _tokens.css 的内容**,render.js 自动 prepend
4. 写本主题独有的"特征"(双线 / drop cap / 边注 / 居中标题等)
5. 在 [`scripts/lib/render.js`](scripts/lib/render.js) 的 `AVAILABLE_THEMES` 数组加新名字
6. 在本 SKILL.md 第三节决策树加一行
7. 立刻可用:`--theme <my-theme>`

**主题文件不允许**:
- 塞 `<script>` / 远程 `@import` 字体(打印会卡)/ JS
- 用 Inter / Roboto 默认字体(反 AI Slop 红线 — 见 DESIGN.md §1.7)
- h2/h3 加左竖条装饰(同上,2023 ChatGPT 卡片风泛滥)
- 渐变背景 / 大 box-shadow 红紫光晕(同上)

---

## 七、依赖说明

| 依赖 | 必需性 | 装法 |
|---|---|---|
| Node ≥ 18 | 必装 | https://nodejs.org/ 或 `brew install node` |
| `npm install`(本目录) | 必装 | `bash scripts/install-deps.sh` |
| Pandoc | `md2docx` 必需 | `brew install pandoc` / `apt install pandoc` |
| WeasyPrint | `md2pdf --engine pandoc` 路线可选 | `pip install weasyprint` |
| **huo15-openclaw-enhance** | **可选** — 装了启用"企微对话拿公网 URL"模式 F | `openclaw plugins install @huo15/huo15-openclaw-enhance` |

**默认路线(puppeteer)只需 npm install,不依赖 pandoc;企微集成所需的 enhance 也是可选,无 enhance 仍能用本机渲染**。

---

## 八、踩坑提示(给 AI 的预防针)

1. **微信公众号粘贴丢样式**:必须用 `md2wechat.js`(已 juice 内联),**不能**直接用 `md2html.js` 的输出粘
2. **mermaid 渲染需要联网**:`md2pdf-puppet.js` 默认从 jsdelivr CDN 加载 mermaid 运行时,离线环境加 `--no-mermaid`
3. **小红书长图过长会被压缩**:超过 5000px 时拆成两张,先用 markdown 二级标题分段后分别导
4. **学术 PDF 中文断行**:`academic` 主题用衬线英文优先,中文长段落建议手动加空格断词,或改用 `huo15-brand` 主题
5. **品牌页眉页脚只在 huo15-brand 主题生效**:其他主题想要页眉用 `--header` 参数手动加
6. **reference.docx 不存在不报错**:Pandoc 自动用内置默认。想要品牌 Word → 见 `templates/README.md`
7. **严禁手写 enhance-share URL**:配合 enhance 时,必须从 `enhance_share_file` 工具的 `structuredContent.url` 取真实链接。**不能**手写、拼接、猜测、回忆类似 `http://localhost:18789/<file>`、`/plugins/enhance-share/<filename>`(缺 token)等任何形式——它们都不是真实链接,用户点了只会 404。这条与 enhance v5.7.24+ 的规则一致

14. **任何内网 URL 都不要发给企微/钉钉外网用户**(v0.4.3 起,v0.4.4 扩到 LAN IP):enhance 默认 `bot_base_url=http://localhost:18789`,OpenClaw gateway 默认端口 18999(可能绑 LAN IP)。如果用户的 OpenClaw 没配公网 `bot_base_url`,任何 share/preview 工具返回的 URL 可能是 **localhost** 或 **LAN IP**(`http://192.168.1.x:18999/...` / `http://10.0.0.x:18789/...`),企微/钉钉外网用户机器**根本访问不到**这些地址,点开就 404。**AI 拿到 URL 后必须跑 unsafe_host_check**:
    - **host 在**:`localhost` / `127.0.0.1` / `0.0.0.0` / `::1` → 不发
    - **host 以**:`192.168.` / `10.` / `169.254.` / `172.16.`-`172.31.` 开头 → 不发(RFC 1918 私网地址)
    - 触发任一条 → 降级:`priority=3`(本地路径) 或 `priority=$P_SEND`(发文件),并提示用户"enhance/gateway 未配公网 bot_base_url,本次走文件路径"
    - **跨 skill 适用**:不只是本 skill 的 `enhance_share_file`,任何来自 enhance_preview / gateway static / agent 自写 HTML 等第三方工具的 URL 都按这条把关
    - v0.4.3 起 skill 默认 `--prefer file` 直接绕过这个坑——发文件不依赖公网 URL。`md-share.sh` / `md-publish.sh` JSON `next_actions[].unsafe_host_check` 字段明文列了所有 unsafe host pattern,AI 必看必跑
8. **md-preview.js 不要直接暴露给企微用户**:它绑 127.0.0.1,内网穿透看不见。企微场景必用 `md-share.sh` + enhance_share_file 链路
9. **md-share.sh / md-publish.sh 不调 enhance**:本 skill 输出 JSON 的 next_actions 是**指示**,不是直接调用——独立装本 skill(没装 enhance)依然能跑(降级 priority=2 输出本地路径)
10. **md-publish 不替用户广播**:即使用户说"发到所有群",也只输出 4 个 URL 让**用户自己**转发。严禁 AI 主动调 wecom 类工具广播——这是 §6.5 + memory `lesson_wecom_at_all_broadcast.md` v2.8.1 @all 事故的红线
11. **OG 卡片需要公网 URL 才显示完整**:HTML 自包含可粘到本地预览,但**只有把 HTML 通过 enhance_share_file 暴露到公网**,微信/企微/Slack 抓 OG meta 时才会渲染卡片(本机 file:// 不会触发卡片抓取)
12. **二维码两阶段不能合一**:**md2pdf-puppet --qr-url 必须传一个已存在的公网 URL**——不能在第一阶段渲染 PDF 时就嵌"未来这个 PDF 的 URL"(鸡生蛋问题)。正确流程:第一阶段 publish 拿 PDF URL → 第二阶段用该 URL 重渲染带 QR 的 PDF
13. **KB 归档 frontmatter 的 share_urls 由 AI 回写**:md-publish 写归档时 share_urls 留空数组,**AI 拿到 enhance URL 后用 Edit 工具回写**——脚本不调 enhance,所以脚本自己写不出 URL(capability detection 设计的代价)

---

## 九、企微 / 钉钉 / 微信场景:capability detection 集成 enhance

### 设计原则(与 §11.4 红线 + memory `feedback_plugins_must_be_independently_installable.md` 一致)

- ✅ 本 skill 不 import / 不依赖 enhance
- ✅ md-share.sh 仅渲染 + 输出标准 JSON
- ✅ 由调用 skill 的 AI 在运行时检测 enhance 是否在场:**enhance_share_file 工具可见 → 调它拿 URL;不可见 → 给本地路径**
- ❌ 不写跨插件 import,不写"if enhance 装了"的硬判断,不在脚本里 spawn 任何 plugin

### 工作流图

```
企微用户:"把这份分析报告导成 PDF 发我"
        │
        ▼
   OpenClaw inbound
        │
        ▼
   AI 看到 SKILL.md §九 模式 F
        │
        ▼
   bash scripts/md-share.sh report.md --mode pdf --label "..."
        │
        │ stdout: {"files":[{"path":"/tmp/.../report-TS.pdf",...}], "next_actions":[...]}
        ▼
   AI 按 next_actions priority=1 尝试:
   enhance_share_file({filePath, label, expireHours: 24})
        │
        ├─ 工具可见 ─→ 拿 structuredContent.url ─→ outbound 发链接到企微 ─→ ✓
        │
        └─ 工具不可见 / 调用失败 ─→ priority=2 fallback ─→
                                 outbound 把 file.path 告诉用户(降级)
```

### `md-share.sh` 用法速查

```bash
# 单一格式
bash scripts/md-share.sh report.md --mode pdf --label "Q1 复盘报告"
bash scripts/md-share.sh post.md   --mode image --theme xiaohongshu  # 小红书长图
bash scripts/md-share.sh news.md   --mode wechat                      # 公众号 inline

# 一份 md 多端并行(企微一次给齐 PDF + 长图 + 网页 三个链接)
bash scripts/md-share.sh report.md --mode all --label "战略分析报告"

# 长效链接(客户 30 天内可访问)
bash scripts/md-share.sh proposal.md --mode pdf --expire-hours 720 --label "客户提案 v1"
```

### `md-publish.sh` 用法速查(v0.3.0,**比 md-share 多了 KB 归档 + 多端默认**)

```bash
# 默认:mode=all,自动归档到 ~/knowledge/huo15/<日期>-<slug>.md
bash scripts/md-publish.sh report.md --slug q1-summary --label "Q1 复盘报告"

# 客户提案(打印场景):带二维码,二阶段 AI 自动二刷 PDF
bash scripts/md-publish.sh proposal.md --slug client-proposal-v1 \
  --label "客户提案 v1" --with-qr --expire-hours 720

# 不归档(纯发布,不写知识库)
bash scripts/md-publish.sh quick-note.md --no-archive

# 自定义归档目录
bash scripts/md-publish.sh internal.md --kb-dir ~/work/wiki/2026-q2

# 仅 PDF + 归档
bash scripts/md-publish.sh report.md --mode pdf --slug q1-summary
```

**md-publish vs md-share 选择**:
- 一次性"发我看看" → md-share(轻量)
- "发布出去 + 留档案" → md-publish(归档 + 多端默认 + 二维码可选)
- 复盘 / 客户提案 / 周月报 / 公司公告 → md-publish

### v0.3.0 新增能力(简表)

- **OG 卡片**:`md2html` 默认从 H1 + 首段抽 og:title/description;显式覆盖用 `--og-title/--og-description/--og-image/--og-url`。HTML 粘到企微/微信/Slack 自动渲染卡片
- **PDF 二维码**:两阶段 — ①拿 PDF URL ②`md2pdf-puppet --qr-url <URL> --qr-label "扫码看在线版"`,二维码进每页右下角页脚(huo15-brand 主题最佳)

输出 JSON(stdout)始终遵循 schema:

```json
{
  "status": "render_complete",
  "files": [{ "path": "/tmp/.../xxx.pdf", "kind": "pdf", "label": "...", "size_kb": 234, "mime": "...", "theme": "huo15-brand" }],
  "next_actions": [
    { "priority": 1, "tool": "enhance_share_file", "args_per_file": {...}, "result_field": "structuredContent.url", "warning": "严禁手写 URL" },
    { "priority": 2, "tool": null, "fallback": "把 path 告诉用户" }
  ],
  "ai_instruction": "对每个 file 优先 priority=1,失败降级 priority=2"
}
```

### AI 触发判断(给读 SKILL.md 的 AI)

用户出现以下意图就走模式 F:
- "**发**给我 / 发给客户 / 发到群里" — outbound 意图
- "**链接**给我 / 给我个链接 / 公网链接 / 分享链接" — URL 需求
- "**给我看看 / 看效果 / 预览**" + 渠道在 IM(企微/钉钉/微信)— 视觉送达
- 当前会话来自企微/钉钉/微信 inbound — 渠道天然适配 enhance

如果用户**只是**说"导出 PDF" 而**没有发送/链接**意图,走模式 A(纯本机文件输出);用户后续说"发我" 再切到模式 F。

---

## 十、文件清单

```
huo15-markdown-export/
├── SKILL.md / README.md / package.json / _meta.json / LICENSE
├── scripts/
│   ├── install-deps.sh / install-to-workspaces.sh
│   ├── md2pdf.sh + md2pdf-puppet.js   # PDF
│   ├── md2docx.sh                      # Word(Pandoc)
│   ├── md2html.js                      # HTML 自包含 + OG 卡片
│   ├── md2image.js                     # 长图 PNG
│   ├── md2wechat.js                    # 微信公众号 inline
│   ├── md-preview.js                   # 127.0.0.1 live preview
│   ├── md-share.sh / md-publish.sh    # 对接 enhance(JSON)
│   ├── md-diff.sh                      # git → changelog PDF
│   └── lib/render.js                   # 共享渲染核心
├── themes/
│   ├── DESIGN.md   ⭐ v0.4.0          # 设计规范(必读)
│   ├── _tokens.css ⭐ v0.4.0          # design tokens
│   ├── apple-tech.css ⭐ v0.4.2 默认  # 苹果科技风
│   ├── typora-newsprint / -night / github / academic / huo15-brand
│   ├── anthropic-doc / editorial-magazine / manuscript-book / tufte-handout  ⭐ v0.4.0
│   └── wechat / xiaohongshu           # hardcode(目标编辑器剥 var)
├── templates/{pdf-print.css, README.md}
└── examples/{sample.md, chart-demo.md}
```

---

## 十一、版本

- **v0.4.4**(2026-05-12):**unsafe_host_check 扩 LAN IP(192.168/10/172.16-31/169.254)+ 跨 skill 适用**
  - 用户报:某 agent 用 canvas 渲染 markdown 到 HTML 后,给出 `http://192.168.1.177:18999/nengbai_preview.html` LAN 预览链接,企微外网用户访问不到。18999 是 **OpenClaw gateway 默认端口**,LAN IP 是用户机器内网地址 — 跟 v0.4.3 修的 localhost:18789 同源
  - v0.4.3 只检测 `localhost` / `127.0.0.1`,这次**扩**:
    - host 在:`localhost` / `127.0.0.1` / `0.0.0.0` / `::1`(本机 loopback)
    - host 以下列开头:`192.168.` / `10.` / `169.254.` / `172.16.`-`172.31.`(RFC 1918 私网地址)
  - JSON `next_actions[].unsafe_host_check` 新增字段明文列检测规则;`ai_instruction` 强调**跨 skill 适用** — 不只检查 `enhance_share_file` 返回值,任何来自第三方工具(enhance_preview / gateway static / agent 自写 HTML 等)的 URL 也按此把关
  - SKILL.md §八第 14 条重写
- **v0.4.3**(2026-05-07):**默认发文件而不是发链接(harness 思维)+ 修 localhost URL 404**
  - 用户报:用 `enhance_share_file` 拿的 URL 是 `http://localhost:18789/plugins/enhance-share/...`(enhance 默认 bot_base_url 未改),企微用户点开 404
  - **harness 思维改造**(SKILL 脚本硬编码 priority 顺序,AI 只 dispatch 在场工具):
    - `md-share.sh` / `md-publish.sh` 默认 `--prefer file`,JSON `next_actions` 改 3 优先级:
      - **priority=1 send_file_to_channel** — 直接发文件到对话框(企微/钉钉/微信原生文件消息),不依赖公网 URL,不暴露 token
      - **priority=2 share_via_public_url** — 拿公网 URL 发链接(用户明确要 / 文件 > 25MB / send_file 不可用时),AI **必须检查 URL host 是否 localhost**,是则降级
      - **priority=3 local_path_only** — 告诉用户本地路径(终端/SSH 场景)
    - 加 `--prefer link` 反转优先级(用户明确要链接时用)
    - `tools_pattern` 列举:`wecom_send_file` / `wechat_send_file` / `dingtalk_send_file` / `*_send_file` / `*_upload_file`
  - SKILL.md §九 重写"模式 F",新增"模式 F 变体(明确要链接)";§八踩坑加第 14 条 localhost URL warning
- **v0.4.2**(2026-05-07):**新默认主题 apple-tech(苹果科技风)+ 修 YAML frontmatter 错乱 + 加强触发词**
  - 新增 **`apple-tech`** 主题作为默认 — Apple 官网视觉:大字 hero(h1=3rem 紧字距 -0.022em)+ 大留白(80px+ padding)+ 黑白为主(#1d1d1f 字 / #ffffff 底)+ 极少色(Apple Blue #0066cc 仅在链接,60-30-10)+ 圆角(8-12px panel)+ 零装饰(无下划线 / 无边框 / 无分隔线)
  - **字体双轨**:屏幕用 -apple-system / SF Pro / PingFang(Mac 原生视觉),`@media print` 切到 Helvetica Neue + Songti SC(反 Type 3 安全字体,PDF 嵌入 CID TrueType 正常)
  - **修 YAML frontmatter 渲染 bug**(用户截图实测):`render.js` 在 markdown-it parse 前调 `stripFrontMatter()` 剥掉 `--- title: x\nauthor: y ---`,原来被当成 `<hr>` + 段落渲染显示为大字标题段,现在剥干净 + meta.title 注入 OG title
  - **改默认主题**:`render.js` 内 `DEFAULT_THEME = 'apple-tech'`(原 `typora-newsprint`),`md2html.js` / `md2pdf-puppet.js` / `md2pdf.sh` / `md-share.sh` 默认全部同步
  - **加强触发词**:`description` 开头加"火一五排版发布技能"重复 3 次提升嵌入向量命中,`aliases` 列表前 8 位全是"火一五XXX"高频锚词,补"苹果科技风排版" / "火一五苹果风"
  - 修 `anchor permalink` 染色 bug:`markdown-it-anchor` 给 h1-h6 内嵌的 `<a>` 继承 `--color-accent` 致 h1/h2 整段变 Apple Blue,显式 `h1-h6 a { color: inherit }` 让标题保持 fg 色
- **v0.4.1**(2026-05-07):**反 Type 3 字体修复 — PDF 渲染浅灰看不清的真根因**
  - 用户报"科技风、其他风格 PDF 文字很浅看不清"。深度调研发现:macOS Headless Chromium 把字体嵌入 PDF 时,Apple 受保护字体(`-apple-system` / `system-ui` / `PingFang SC` / `SF Pro` / `Iowan Old Style`)+ OpenType CFF 字体(`Source Han Sans/Serif SC` / `Noto CJK` / `Hiragino Sans GB`)走 **Type 3 路径渲染**,WPS / Foxit / 旧 Acrobat 渲染成笔画细 + 灰阶模糊
  - 调研对照 Typora 官方 5 大主题(newsprint/github/night/gothic/pixyll)— **零用** Apple 系统字体,英文用 PT Serif / Open Sans / Merriweather / Helvetica Neue,中文 fallback 只用 STSong / Songti SC。我们对齐
  - **修法 1**:`_tokens.css` 字体栈剔除所有禁忌字体,英文用 `PT Serif/Merriweather/Open Sans/Helvetica Neue`,**中文 fallback 不论英文衬线/无衬线统一用 `Songti SC`**(macOS 预装真 TTC,嵌成 CID TrueType 正常)
  - **修法 2**:typora-night 加 `@media print` 自动反色为浅底深字 — 原本暗底浅字打印模式 1.4:1(WCAG 远不达 4.5:1)看不清,反色后 17.4:1
  - **修法 3**:`templates/pdf-print.css` 删 `body { background: #ffffff !important }` 强制白底 — 让主题自控背景(newsprint 米色 / manuscript 旧书纸 / editorial 暖白等保留)
  - **修法 4**:`themes/DESIGN.md §7.5` 新增"反 Type 3 字体硬红线"段,落禁忌字体清单 + 推荐字体 + 发版前 `pdffonts | grep "Type 3"` 自查
  - 验收:9 主题 PDF 重渲染,Type 3 字体从 178/177/177/9/194/35/14/10/9 → 5/5/5/9/5/5/9/6/5(主体字体全部 CID TrueType,5-9 个边缘 emoji / 标点 fallback 不影响视觉);9 主题打印模式 WCAG 全部 ≥ 14:1
- **v0.4.0**(2026-05-07):**主题系统重构 + 4 个新预设**
  - 抽 `themes/_tokens.css`(全局 design tokens:字体栈 / 字号阶梯 1.25 Major Third / 行高档位 / 留白 8pt grid / 容器宽 / 语义色)
  - `render.js` 自动为 9 个支持 token 的主题 prepend `_tokens.css`,wechat / xiaohongshu 因目标编辑器剥 var 保留 hardcode
  - 新增 [`themes/DESIGN.md`](themes/DESIGN.md) — 8 大设计范式 + 反 AI Slop 红线 + 主题选择决策树 + 新主题 7 步 checklist + 发版前红线 grep 自查
  - 重构 5 旧主题(newsprint / night / github / academic / brand)用 token,代码量 ~40% 收缩
  - **修 3 处 AI Slop 红线**:typora-night 字体 Inter → system-ui + 暗底 #1f2329 → #121212;huo15-brand 去 h2 左竖条 + 改 60-30-10(strong / h3 不再染主色,主色降到 ≤10%);xiaohongshu 去渐变背景 + 去 strong 渐变高亮 + 去图片红光晕
  - **新增 4 个预设**:
    - `anthropic-doc` — Anthropic / Stripe 技术文档风,衬线正文 + 灰底代码 + 极少装饰(2026 年技术文档主流审美)
    - `editorial-magazine` — 商业杂志体,Playfair Display 大字 + drop cap + 满版图 + 大留白(品牌故事 / 深度长文)
    - `manuscript-book` — 书稿 / 小说体,单一衬线 + 1.95 行高 + 章标居中 + 0 装饰 + 段首缩进(无干扰沉浸阅读)
    - `tufte-handout` — Tufte 边注体,窄主文 + 右挂边注(≥1100px)+ 三线表 + ET Book 衬线感(数据分析 / 研究报告)
  - 主题决策树拆"信息密集 / 视觉沉浸 / 多端发布"三阵营(更易选)
- **v0.3.x**(2026-05-06):`md-publish.sh` 多端发布 + KB 归档;HTML OG 卡片;PDF `--qr-url` 二维码;`install-to-workspaces.sh` 多 workspace 安装
- **v0.2.0**(2026-05-05):`md-share.sh` + capability detection 集成 enhance
- **v0.1.0**(2026-05-05):首发,7 主题 + 7 脚本 + KaTeX + mermaid + highlight.js

> 详细 changelog 见 `git log` / cnb.cool 仓库 commit history

---

**公司:** 青岛火一五信息科技有限公司 · postmaster@huo15.com · QQ群 1093992108
