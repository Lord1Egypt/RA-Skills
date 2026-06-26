# kai-html-export

[English](README.md) | 简体中文

> 将任意 HTML 文件导出为 PPTX、PNG，或发布为公网链接——适用于 kai-slide-creator、kai-report-creator 或任何独立 HTML 文件。

一个 Claude Code 技能，通过无头浏览器将 HTML 文件转换为便携格式。PPTX / PNG 导出无需 Node.js，直接使用你已安装的系统 Chrome；可选的 URL 发布 helper 默认使用 Cloudflare Pages，并保留 Vercel 作为回退方案。

**v1.2.0** — 新增统一分享入口 `share-html.py`，默认发布到 Cloudflare Pages，保留 Vercel 回退，并在托管云沙箱里禁用自动分享，改为输出手动分享指引。**v1.1.7** — 修复两处 native 模式图片丢失问题：（1）被 CSS 动画 wrapper（如 `kd-reveal`、淡入容器）包裹的图片会被装饰性 blob 过滤器误判为装饰元素而整棵跳过——修复方式：跳过前先检查是否含子级光栅元素；（2）`object-fit: contain` 和 `fill` 图片会回退到 Playwright 截图路径（静默失败）——修复方式：在 `_download_img_direct` 中直接读取原图文件嵌入，不做裁剪。这两个问题均会导致使用 CSS 动画 wrapper 包裹 `<img>` 的幻灯片在 native 导出时内容图片全部消失。**v1.1.6** — 导出后预览网格；PPTX 结构验证；浏览器启动沙箱适配；QA 流程说明。

---

## 安装

### Claude Code

```bash
git clone https://github.com/kaisersong/kai-html-export ~/.claude/skills/kai-html-export
pip install playwright python-pptx beautifulsoup4 lxml
```

### OpenClaw / ClawHub

```bash
clawhub install kai-html-export
```

> ClawHub 页面：https://clawhub.ai/skills/kai-html-export

OpenClaw 首次使用时会自动安装所有依赖。

---

## 使用方法

```
/kai-html-export [file.html]                    # PPTX（图片模式，默认）
/kai-html-export --pptx [file.html]             # 明确指定 PPTX 导出
/kai-html-export --pptx --mode native [file]    # 可编辑 PPTX（native 模式）
/kai-html-export --png [file.html]              # 全页截图保存为 PNG
/kai-html-export --png --scale 2                # 2× 高清 PNG
python scripts/share-html.py [file.html|folder]     # 可选：发布为分享链接（默认 Cloudflare）
python scripts/share-html.py --provider vercel [file.html|folder]
```

未指定文件时，默认使用当前目录中最近修改的 `.html` 文件。

---

## 导出模式

### 图片模式（默认）

将每张幻灯片截图后合成为 PowerPoint 文件，与浏览器显示效果像素级一致。文字为图片，不可编辑。

```bash
/kai-html-export presentation.html
# → presentation.pptx（16:9，1440×900）
```

| | 图片模式 |
|--|--|
| 视觉还原度 | ⭐⭐⭐⭐⭐ 像素级一致 |
| 文字可编辑 | ❌ 已光栅化 |
| 适用场景 | 分享、归档最终版演示文稿 |

---

### Native 模式——可编辑 PPTX

将每张幻灯片还原为真实的 PowerPoint 形状、文本框和表格，文字在 Keynote 和 PowerPoint 中完全可编辑。

```bash
/kai-html-export --pptx --mode native presentation.html
# → presentation.pptx（文字、形状、表格均可编辑）
```

| | Native 模式 |
|--|--|
| 视觉还原度 | ⭐⭐⭐ 简化渲染 |
| 文字可编辑 | ✅ 完整文字编辑 |
| 适用场景 | 修改内容、翻译、复用幻灯片 |

#### Native 模式支持的元素

| 元素 | 支持情况 |
|------|---------|
| 标题、段落、列表 | ✅ 字号、颜色、加粗、对齐 |
| 行内文字样式 | ✅ 加粗、斜体、删除线、颜色 |
| 行内背景高亮 | ✅ `<span style="background:…">` → 文字底部彩色色块 |
| 纯色背景形状（带背景色的 div） | ✅ 矩形填充 |
| 表格 | ✅ 可编辑单元格和边框 |
| 图片（`<img>`、`canvas`、CSS `background-image`） | ✅ 作为光栅层嵌入 |
| SVG 图形 | ✅ 光栅化为 PNG 后嵌入 |
| 网格 / 圆点 / 噪点背景 | ✅ 自动检测并渲染 |
| `position:fixed` 导航点和进度条 | ✅ 按幻灯片序号计算每页状态；如需隐藏两者，在 `<body>` 上设置 `data-export-progress="false"` |

#### Native 模式的简化或跳过项

| 元素 | 处理方式 |
|------|---------|
| CSS 渐变 | → 取渐变中间色填充 |
| Box shadow | → 省略 |
| 自定义 Web 字体（Barlow、Inter 等） | → 替换为最接近的系统字体 |
| 不支持的 DOM / CSS 边界情况 | → 安全跳过，不再导致导出崩溃 |

#### CJK（中日韩）字体补偿

PingFang SC 等 CJK 字体在 Keynote/PowerPoint 中比 Chrome 宽约 15%、高约 30%。Native 模式会自动补偿：

- 含 CJK 文字的文本框宽度扩大 ×1.15
- Condensed 字体容器（Barlow Condensed 等）扩大 ×1.30
- 宽度扩展仅适用于宽度小于 3 英寸的小框（防止宽容器溢出边界）
- Windows 上优先将 CJK 字体映射为 Microsoft YaHei / 微软雅黑，避免导出的 PPT 回退到 Calibri
- 行内背景色块使用 PPTX 坐标系（而非 Chrome 坐标），确保与文字精确对齐

---

## 导出为 PNG

截取完整页面为 PNG 图片，适合将报告或单页 HTML 以图片形式分享。

```bash
/kai-html-export --png report.html
# → report.png

# 2× 分辨率，适合发送到微信 / Telegram 等 IM
/kai-html-export --png report.html --scale 2
```

---

## 发布 HTML 为分享链接

把生成好的 deck 或报告发布出去，并拿到一个可直接分享的 URL：

```bash
python scripts/share-html.py presentation.html
python scripts/share-html.py ./my-html-folder
python scripts/share-html.py --provider vercel presentation.html
```

- 支持单个 HTML 文件，或包含 `index.html` 的文件夹
- 传入单文件时，会自动复制常见相对路径资源
- 默认走 Cloudflare Pages，因为它在中国通常比 Vercel 更容易访问
- 保留 Vercel 作为可选回退方案
- 只依赖运行时 CLI，不会给仓库新增安装依赖
- 在托管云沙箱里会禁用自动分享，直接输出“请在本地手动分享”的提示，不会尝试登录或部署

本地使用 Cloudflare 时，先登录：

```bash
wrangler login
```

本地使用 Vercel 时，先登录：

```bash
npx vercel login
```

---

## 依赖要求

| 依赖 | 用途 | OpenClaw 自动安装 |
|------|------|------------------|
| Python 3 + `playwright` | 无头浏览器截图 | ✅ via uv |
| Python 3 + `python-pptx` | 合成 PPTX | ✅ via uv |
| `beautifulsoup4` + `lxml` | HTML 解析（native 模式） | ✅ via uv |
| Node.js + Wrangler / Vercel CLI | 可选：发布分享链接 | ❌ 需手动准备 |

**浏览器：** 优先使用系统已安装的 Chrome、Edge 或 Brave，无需下载 Chromium。找不到系统浏览器时才回退到 Playwright 自带的 Chromium。

**Claude Code 用户** 需手动安装：
```bash
pip install playwright python-pptx beautifulsoup4 lxml
```

如需通过 Cloudflare 发布分享链接：
```bash
wrangler login
```

如需通过 Vercel 发布分享链接：
```bash
npx vercel login
```

---

## 使用案例：品牌风格迁移

将现有 `.pptx` 迁移到自定义品牌设计系统——一套工作流同时输出像素级归档版和可编辑版。

**准备工作：** 在 `themes/your-brand/` 下创建 `reference.md`，描述颜色、字体和布局（复杂视觉系统可额外提供 `starter.html`）。

```bash
# 第一步——风格迁移：slide-creator 读取 PPTX，按品牌主题重排
/slide-creator --plan "将 company-deck.pptx 迁移到我们的品牌风格"
# 确认 PLANNING.md 后：
/slide-creator --generate
# → branded-deck.html

# 第二步——两种模式同时导出
/kai-html-export branded-deck.html
# → branded-deck.pptx（像素级，用于分享）

/kai-html-export --pptx --mode native branded-deck.html
# → branded-deck.pptx（文字可编辑，用于修改）
```

这套工作流特别适合企业已有品牌模板或 VI 规范的场景——将规范写成 `starter.html`，slide-creator 以此为底板，自动填入源 PPTX 的内容。

---

## 适配的技能

| 技能 | 输出类型 | 导出格式 |
|------|---------|---------|
| [kai-slide-creator](https://github.com/kaisersong/slide-creator) | 含 `.slide` 元素的 HTML 演示文稿 | PPTX（逐幻灯片） |
| [kai-report-creator](https://github.com/kaisersong/kai-report-creator) | 单页 HTML 报告 | PNG（全页截图） |
| 任意 HTML 文件 | 独立 HTML | PPTX 或 PNG |

---

## 兼容性

| 平台 | 版本 | 安装路径 |
|------|------|----------|
| Claude Code | 任意 | `~/.claude/skills/kai-html-export/` |
| OpenClaw | ≥ 0.9 | `~/.openclaw/skills/kai-html-export/` |

---

## 许可证

MIT
