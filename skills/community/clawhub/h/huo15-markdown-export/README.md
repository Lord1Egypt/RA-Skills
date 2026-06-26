# 火一五 Markdown 视觉渲染管线

---

<div align="center">

<img src="https://tools.huo15.com/uploads/images/system/logo-colours.png" alt="火一五Logo" style="width: 120px; height: auto; display: inline; margin: 0;" />

</div>

<div align="center">

<h3>打破信息孤岛,用一套系统驱动企业增长</h3>
<h3>加速企业用户向全场景人工智能机器人转变</h3>


</div>
<div align="center">

| 🏫 教学机构 | 👨‍🏫 讲师 | 📧 联系方式         | 💬 QQ群      | 📺 配套视频                         |
|:-----------:|:--------:|:------------------:|:-----------:|:-----------------------------------:|
| 逸寻智库 | Job | support@huo15.com | 1093992108  | [📺 B站视频](https://space.bilibili.com/400418085) |

</div>

---

## 这是什么

**`huo15-markdown-export`** 是火一五 OpenClaw 生态的 markdown 视觉渲染管线。任何 `.md` 文件,一行命令就能导出 PDF / Word / 单文件 HTML / 小红书长图 / 微信公众号 inline / live preview / git changelog PDF——7 种产出,7 套主题,零 AI 也能跑,接进 Claude 后 AI 直接调用。

把 Typora 的"渲染美学 + 多格式导出"剥离出来,做成 AI 可编排的工具——**编辑器交给 VSCode / Obsidian / Cursor,渲染交给本 skill**。

---

## 与 huo15-openclaw-office-doc 的关系

| 场景 | 用哪个 |
|---|---|
| 让 AI **写**一份合同/PRD/会议纪要 | `huo15-openclaw-office-doc`(结构化公文,reportlab 直出) |
| 我有一份 .md,想**导出**成 PDF/Word/长图 | `huo15-markdown-export`(本 skill) |

**两者互补,不重叠**。

---

## 快速开始

```bash
# 1. 进 skill 目录
cd ~/workspace/projects/openclaw/huo15-skills/huo15-markdown-export

# 2. 装依赖(node + 可选 pandoc)
bash scripts/install-deps.sh

# 3. 试一发
node scripts/md2pdf-puppet.js examples/sample.md
node scripts/md2image.js      examples/sample.md --theme xiaohongshu
node scripts/md-preview.js    examples/sample.md
# 浏览器打开 http://127.0.0.1:7777
```

---

## 9 个工具

| 脚本 | 输入 → 输出 | 用途 |
|---|---|---|
| `md2pdf-puppet.js` | md → PDF | Chromium 打印(Typora 同款),7 主题;**v0.3.0 加 `--qr-url` 嵌二维码** |
| `md2docx.sh` | md → docx | Pandoc + 火一五 reference.docx 模板 |
| `md2html.js` | md → 单文件 html | **v0.3.0 自动加 OG 卡片**(企微/微信粘贴显示标题摘要) |
| `md2image.js` | md → png | 1080px 小红书长图,也可 huo15-brand 沉稳风 |
| `md2wechat.js` | md → inline html | juice 内联,粘到微信公众号 |
| `md-preview.js` | md → http server | 本机 127.0.0.1(企微看不见,本机调试用) |
| `md-diff.sh` | git ref × 2 → PDF | 版本对比 / changelog |
| **`md-share.sh`** ⭐ v0.2.0 | md → 多产物 + JSON | **企微对话渲染送达**,对接 enhance 拿公网 URL |
| **`md-publish.sh`** ⭐⭐ v0.3.0 | md → 多端 + JSON + KB 归档 | **发布场景首选**:多端 + 归档 `~/knowledge/huo15/` + 二阶段 QR PDF;人在回路转发 |

---

## 7 套主题

| 主题 | 适用 |
|---|---|
| `typora-newsprint` | 报纸风衬线,个人博客 / 长文随笔 |
| `typora-night` | 暗色护眼,夜间 / 投影 |
| `github` | GitHub README 风,开源文档 |
| `academic` | 学术论文,IEEE/ACM 风格初稿 |
| `wechat` | 微信公众号(已剥离 grid/flex/var) |
| `xiaohongshu` | 小红书长图,1080px 暖色大字号 |
| `huo15-brand` | 火一五品牌,客户报告 / 内部周报(自带页眉页脚) |

切主题:`--theme <name>`。AI 想做新主题:复制最相近的 CSS 改即可。

---

## 集成到 OpenClaw / Claude

**自然语言示例**(AI 自动调用):

> "把这份分析报告**发给客户**" → AI 调 `md-share.sh --mode pdf` → chain 调 `enhance_share_file` 拿公网 URL → 发企微对话
> "这份 Q1 复盘**发布**出去 + 留档" → AI 调 `md-publish.sh --slug q1-summary` → 多端发布 + 归档 KB + 4 个 URL 让用户挑转发
> "客户提案打印 50 份,要让客户能扫码看在线版" → AI 调 `md-publish.sh --with-qr` → 二阶段拿到 URL → 二刷 PDF 嵌二维码
> "这篇文章发链接给同事,要在企微显示标题摘要预览" → AI 调 `md2html.js`(v0.3.0 自动 OG)→ enhance share → 发链接,自动卡片
> "v1.2 到 v1.3 改了什么,出个 PDF" → AI 调 `md-diff.sh`
> "主题再暖一点" → AI 用 Edit 工具改 themes/*.css(不写新脚本)

---

## 企微 / 钉钉 / 微信对话渲染送达(v0.2.0 新增)

**问题**:OpenClaw 部署在内网穿透后(`https://<bot_base_url>` → `localhost:18789`),企微用户无法访问 `127.0.0.1` 起的预览 server。

**方案**:`md-share.sh` + `huo15-openclaw-enhance`(可选)的 `enhance_share_file` 工具 = 渲染产物自动暴露成 `https://<bot_base_url>/plugins/enhance-share/<token>-<file>` 公网 URL。

```
企微用户:"把复盘渲染成长图发我"
     ↓
AI:bash md-share.sh report.md --mode image --label "Q1 复盘"
     ↓
拿到 stdout JSON.files[0].path
     ↓
AI:enhance_share_file({filePath, label, expireHours: 24})    ← enhance 工具
     ↓
url = https://keepermac.huo15.com/plugins/enhance-share/abc-Q1.png
     ↓
AI 把 url 发回企微对话,用户点链接看图
```

**capability detection 设计**:本 skill **不强依赖 enhance**——

- 装了 enhance:走上面的优雅链路(priority=1)
- 没装 enhance:`md-share.sh` 输出的 JSON 仍然给本地路径(priority=2 fallback),AI 把路径告诉用户(降级,不报错)
- 跨 OpenClaw 部署自适应:`bot_base_url` 不同的实例,enhance 自动从 host header 检测,无需配 env

详细 chain 调用模式见 [SKILL.md §九](SKILL.md)。

---

## 发布 + 归档(v0.3.0 新增)

`md-publish.sh` 把"发出去给人看"和"给自己留档"做成同一个动作:

```bash
bash scripts/md-publish.sh report.md --slug q1-summary --label "Q1 复盘报告"
```

一次完成:
1. **多端渲染** — PDF + 长图 + HTML(带 OG 卡片)+ 公众号 inline,共 4 个产物
2. **KB 归档** — 自动写 `~/knowledge/huo15/2026-05-06-q1-summary.md`,带 frontmatter(title / slug / published_at / source / summary / render_outputs / share_urls 占位 / tags)
3. **share-ready JSON** — AI 拿到后逐个调 `enhance_share_file` 拿 4 个 URL
4. **回写 KB** — AI 用 Edit 工具把 4 个 URL 写回 KB frontmatter `share_urls:` 列表(未来翻档案能直接拿到当时的公网链接)
5. **多版本菜单** — AI 把 4 个 URL 组装成消息发回当前会话,**用户自己**决定转发哪个版本到哪个群(人在回路,严守 §6.5 "禁广播")

`--with-qr` 启用二阶段:AI 拿到 PDF URL 后,自动用 `md2pdf-puppet --qr-url <url>` 二刷一份带二维码页脚的打印版 PDF。**线下客户提案 / 海报 / 名片背面 / 印刷品**专用——扫码直达在线版。

---

## OG 卡片(v0.3.0 新增)

`md2html.js` 默认从 markdown 抽 H1 + 首段作为 `og:title` / `og:description`。HTML 通过 enhance 暴露成公网 URL 后,粘到企微/微信/Slack 对话框**自动显示标题+摘要的卡片预览**(不是冷链接)。

```bash
# 自动模式(零配置)
node scripts/md2html.js article.md

# 显式覆盖 + 加封面图
node scripts/md2html.js article.md article.html \
  --og-title "AI 时代的 Markdown 工具链" \
  --og-description "把 Typora 拆成 OpenClaw skill 的设计思考" \
  --og-image https://tools.huo15.com/uploads/cover.png
```

---

## 依赖

| 工具 | 必需性 | 装法 |
|---|---|---|
| Node ≥ 18 | 必装 | `brew install node` |
| npm install | 必装 | `bash scripts/install-deps.sh` |
| Pandoc | 仅 `md2docx` | `brew install pandoc` |
| **huo15-openclaw-enhance** | 仅企微对话送达模式(可选) | `openclaw plugins install @huo15/huo15-openclaw-enhance` |

默认 puppeteer 路线只需 Node,不依赖 pandoc;企微集成所需的 enhance 也是可选——**装不装本 skill 都能跑**。

---

## 详细文档

- 完整能力 + AI 调用模式 → [SKILL.md](SKILL.md)
- 主题选择决策树 + reference.docx 自定义 → [templates/README.md](templates/README.md)
- 跑一遍 → [examples/sample.md](examples/sample.md)

---

## 协议

MIT — 见 [LICENSE](LICENSE)。

---

<div align="center">

**公司名称:** 青岛火一五信息科技有限公司

**联系邮箱:** postmaster@huo15.com | **QQ群:** 1093992108

---

**关注逸寻智库公众号,获取更多资讯**

<img src="https://tools.huo15.com/uploads/images/system/qrcode_yxzk.jpg" alt="逸寻智库公众号二维码" style="width: 200px; height: auto; margin: 10px 0;" />

</div>

---
