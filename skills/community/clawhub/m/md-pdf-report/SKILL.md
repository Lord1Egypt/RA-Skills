---
name: md-pdf-report
description: 'Convert Markdown research reports / fact-checks / scheme proposals into styled PDFs with native CJK (Chinese) font support. Markdown is the single source of truth; PDF is generated FROM the Markdown. Triggers on "做个 PDF 报告", "转成 PDF", "调研报告", "fact-check 报告", "方案 PDF", "scheme 报告", "给我 PDF", "PDF 版本", or any long-form analytical content that needs to be both editable (MD) and viewable/shareable (PDF).'
---

# md-pdf-report · Markdown 双产物报告（PDF + MD）

**MD 是事实源，PDF 是交付物。** 同一份内容，两个产物：

- `.md` — 可二次编辑、可分发给其他 Agent
- `.pdf` — 打开即看、可分享给他人

（详见下一节"🚨 必做最后一步"）

**核心用户偏好（Jialin）：** 调研类内容要同时产出 PDF（方便看/分享）和 MD（方便二次编辑或分发给其他 Agent）。MD 是单一事实源，不要写两份。

---

## 何时使用

| 触发 | 用法 |
|------|------|
| "做个 PDF 报告" / "转成 PDF" / "给我 PDF 版本" | → 本 skill |
| "调研报告"、"fact-check 报告"、"方案 PDF" | → 本 skill |
| 长文分析（> 1 页 A4）需要可编辑源文件 | → 本 skill |
| 用户说"以后经常用" 类长文输出 | → 本 skill |

**不适用：**
- 简历、一页纸、产品白皮书、品牌文档 → 用 `kami`
- PPT/slides → 用 `kami` 的 slides 路径
- 简短消息/通知 → 直接发文字
- 不需要 PDF，只要 MD → 直接写 .md，不调用本 skill

---

## 快速开始

```bash
# 1. 选模板（首次使用）
cp ~/.hermes/skills/md-pdf-report/templates/research-report.md ~/my-report.md
# 或 fact-check.md, scheme.md

# 2. 编辑内容（用任何 MD 编辑器）

# 3. 生成 PDF
python3 -m md2pdf ~/my-report.md

# 4. 交付（飞书/Telegram）
# 在对话中：MEDIA:/Users/you/my-report.pdf
```

**Python 用法：**
```python
from md2pdf import md_to_pdf
md_to_pdf("report.md")                    # 同名 .pdf
md_to_pdf("report.md", "out.pdf")         # 自定义输出
md_to_pdf("report.md", keep_html=True)    # 保留 .html（调试用）
```

---

## 工作流

### Step 1 — 写 Markdown（事实源）

用标准 GitHub-flavored Markdown 写。支持的语法：

- 标题（`#`, `##`, `###`）、列表、表格
- **加粗**、*斜体*、`行内代码`、代码块
- 链接 `[文字](url)`
- 引用 `>`、分隔线 `---`

**特殊区块**（用 `<div>` 实现，已在 CSS 中预定义）：

| Class | 用途 | 样式 |
|-------|------|------|
| `<div class="callout">` | 重要提示、警示、关键结论 | 红色边框 + 浅红背景 |
| `<div class="note">` | 注释、补充信息、免责声明 | 灰色边框 + 浅灰背景 |
| `<div class="warn">` | 警告 | 黄色边框 + 浅黄背景 |

示例：
```markdown
<div class="callout">

**重要：** 这是一段红色 callout 文字。Testing mixed CJK + English.

</div>
```

**模板起点：** `templates/research-report.md`、`templates/fact-check.md`、`templates/scheme.md`

### Step 2 — 转换为 PDF

```bash
python3 -m md2pdf /path/to/report.md            # 基本用法
python3 -m md2pdf report.md -o final.pdf         # 自定义输出
python3 -m md2pdf report.md --keep-html          # 保留中间 HTML（调试）
```

### Step 3 — 交付

飞书/Telegram 对话框中，PDF 通过 `MEDIA:` 前缀上传：

```
MEDIA:/absolute/path/to/report.pdf
```

飞书/Telegram 会自动作为附件投递。

---

## 关键技术细节

### ⚠️ Pitfall #1: macOS .ttc 字体不可用

苹果系统 .ttc 字体文件（PingFang.ttc、STHeiti Medium.ttc）用 PostScript outlines，
**reportlab 和 weasyprint 都无法加载**。

**解决：** 用 `.ttf` 字体文件：

| 字体 | 用途 | 路径 |
|------|------|------|
| STXIHEI | 正文 | `…/10e7a462a671950b802274fad767b566ff8457d1…/STXIHEI.ttf` |
| STHEITI | 标题 | `…/53fe5be564086fefc7523ccd0a31200acf92e0e5…/STHEITI.ttf` |
| Kai | 注释/引用 | `…/6331c5916c361af1b83fb8b8b76ef2eece20c8eb…/Kai.ttf` |

**完整路径、验证脚本、失败模式**见 `references/macos-cjk-fonts.md`

### ⚠️ Pitfall #2: weasyprint 缺 C 库

```bash
brew install pango
export DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib
```

`md2pdf.py` 的 `bootstrap_macos()` 在导入时自动设置。设 `MD2PDF_NO_BOOTSTRAP=1` 可关闭。

**详细步骤、验证方法、Linux 替代**见 `references/weasyprint-bootstrap.md`

### ⚠️ Pitfall #3: HTML 标签在 reportlab 表格里需要 Paragraph 包裹

如果混用 reportlab 路径（罕见，本 skill 默认 weasyprint），`<b>` `<br/>` 在
`Table` 单元格中**不会自动渲染**，必须把字符串用 `Paragraph()` 包一层。

### ⚠️ Pitfall #4: PDF 文件大小

weasyprint 默认嵌入全字体（2-3MB/页）。研究类报告 < 15 页通常无需优化。
超过 15 页或需要邮件发送时，参考 `references/pdf-engine-comparison.md` 的优化章节。

---

## 引擎选择

`md2pdf.py` 默认使用 **weasyprint**（最佳平衡点）。三种引擎详细对比、迁移路径见 `references/pdf-engine-comparison.md`。

简要决策：

| 场景 | 推荐引擎 |
|------|---------|
| 研究报告、fact-check、方案 | **weasyprint**（默认） |
| 程序化生成、极致文件大小 | reportlab |
| 学术级排版、纯 MD + 公式 | pandoc + tectonic |

---

## 文件结构

```
~/.hermes/skills/md-pdf-report/
├── SKILL.md                    # 本文件
├── scripts/
│   └── md2pdf.py              # 主转换模块（也可作 CLI: python3 -m md2pdf）
├── templates/
│   ├── research-report.md     # 调研报告模板
│   ├── fact-check.md          # 事实核查模板
│   └── scheme.md              # 方案/计划模板
├── references/
│   ├── macos-cjk-fonts.md     # 中文字体路径与陷阱
│   ├── weasyprint-bootstrap.md # C 库安装与环境变量
│   └── pdf-engine-comparison.md # weasyprint vs reportlab vs pandoc
└── examples/
    ├── Mike_Lynch_FactCheck.md  # 真实案例（7页 PDF）
    └── test_report.md           # 最小测试用例
```

**软链到 PATH（可选）：**
```bash
ln -s ~/.hermes/skills/md-pdf-report/md2pdf.py ~/.local/bin/md2pdf
chmod +x ~/.local/bin/md2pdf
# 然后直接用: md2pdf report.md
```

---

## 自定义 CSS

```python
from md2pdf import md_to_pdf, DEFAULT_CSS

# 追加自定义规则
custom_css = DEFAULT_CSS + """
h1 { color: #B91C1C; }  /* 改标题为红 */
table th { background: #0F172A; }  /* 表头更深 */
"""

md_to_pdf("report.md", css=custom_css)
```

---

## 验证清单（生成 PDF 后必做）

- [ ] 中文渲染正常（不是方块、不是问号）
- [ ] 表格不被截断
- [ ] 代码块/引用样式正确
- [ ] callout/note/warn 区块显示正确
- [ ] 页码/页脚正常
- [ ] 链接可点击（导出后 hover 试一下）
- [ ] 文件大小 < 5MB

**快速验证命令：**
```bash
pdfinfo report.pdf | grep Pages           # 检查页数
pdftotext report.pdf - | head -50         # 检查中文渲染
```

---

## 维护

- **macOS 系统升级后字体路径可能变** → `find /System/Library/AssetsV2 -name "STXIHEI.ttf"` 重新确认
- **PDF 突然乱码** → 90% 是字体路径失效，重新 `find`
- **导出报 `cannot load library 'libgobject'`** → pango 没装好或 `DYLD_FALLBACK_LIBRARY_PATH` 没设
- **weasyprint 版本更新** → 关注 changelog
