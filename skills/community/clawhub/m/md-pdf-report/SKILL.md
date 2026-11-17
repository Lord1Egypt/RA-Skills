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
# 0. 首次使用：安装 Python 依赖（macOS 系统 Python 缺这两个模块）
pip3 install --user markdown weasyprint
# 注意：pip3 install 的脚本会装到 ~/Library/Python/3.9/bin（不在 PATH）
# 这是正常的；不影响 python3 -m 形式调用

# 1. 选模板（首次使用）
cp ~/.hermes/skills/md-pdf-report/templates/research-report.md ~/my-report.md
# 或 fact-check.md, scheme.md

# 2. 编辑内容（用任何 MD 编辑器）

# 3. 生成 PDF（用绝对路径调用，最稳）
python3 ~/.hermes/skills/md-pdf-report/md2pdf.py ~/my-report.md
# 等价但更短（前提：依赖已装）：
#   python3 -m md2pdf ~/my-report.md

# 4. 交付（飞书/Telegram）
# 在对话中：MEDIA:/Users/you/my-report.pdf
```

> ⚠️ **macOS 真实调用姿势**：本 skill 的 `md2pdf.py` 实际位于 skill 根目录（不是 `scripts/` 子目录，SKILL.md 旧版本写错了）。系统 Python (`/usr/bin/python3`) **不预装** `markdown` 和 `weasyprint` 两个包，必须先 `pip3 install --user`。验证命令：`python3 -c "import markdown, weasyprint"` —— 两者都 OK 才能跑成功。

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

**模板起点：**

| 模板 | 用途 |
|---|---|
| `templates/research-report.md` | 自己的研究输出（调研 / 链上分析 / 对比研究） |
| `templates/research-digest.md` | **消化别人的研究**（提案 / 论文 / 博客 / 论坛帖）— 必出批判性分析 + 社区讨论 + 一句话总结，含 Jialin 调研硬性格式要求 |
| `templates/fact-check.md` | 第三方主张核实 |
| `templates/scheme.md` | 方案 / 计划 / 实施路径 |

### Step 2 — 转换为 PDF

```bash
python3 -m md2pdf /path/to/report.md            # 基本用法
python3 -m md2pdf report.md -o final.pdf         # 自定义输出
python3 -m md2pdf report.md --keep-html          # 保留中间 HTML（调试）
```

### Step 3 — 交付（按平台分两种姿势）

**重要：飞书 DM 场景下必须用 `send_message` 工具，不能只在 assistant 自然回复里写 `MEDIA:` 路径。** 详见下方 Pitfall #6。

#### 姿势 A：跨平台通用 — `send_message` 工具（推荐，最稳）

```python
# 飞书 DM（用 home channel，gateway 自动路由到当前对话）
send_message(
    action="send",
    target="feishu",
    message="📄 报告标题（简短说明）\n\nMEDIA:/absolute/path/to/report.pdf"
)
# 返回值含 message_id 才算投递成功
# {"success": true, "platform": "feishu", "chat_id": "...", "message_id": "om_xxx"}
```

**其他平台 target 格式**：
- Telegram: `telegram` / `telegram:chat_id:thread_id`
- Discord: `discord:#channel-name` / `discord:chat_id:thread_id`
- 多平台 fan-out: `target="all"`

#### 姿势 B：只在 assistant 自然回复里嵌 `MEDIA:` 路径

```
MEDIA:/absolute/path/to/report.pdf
```

- ✅ Telegram / Discord 等平台：**可能**会自动作为附件投递（取决于 gateway 实现）
- ❌ **飞书 DM：不可靠**——2026-06-11 和 2026-06-11 两次 session 重蹈覆辙，用户都反馈"必须发到对话框"

> ⚠️ 经验反例（2026-06-11 + 2026-06-11 两次复现）：首次发布时只给了 `/tmp/xxx.pdf` 路径或只把 `MEDIA:` 路径嵌在 assistant 消息里就当作完成，用户立刻反馈"必须发到对话框"。**完成定义 = 本地有文件 AND 对话框能看到附件（通过 `send_message` 工具投递并拿到 message_id 确认），二者缺一不可。**

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

### ⚠️ Pitfall #5: macOS 系统 Python 缺 markdown + weasyprint（首次必踩）

**症状**：`python3 -m md2pdf file.md` 直接报 `ModuleNotFoundError: No module named 'markdown'` 或 `No module named 'weasyprint'`。

**根因**：
- macOS 自带 `/usr/bin/python3` 不带任何第三方包
- `pip3 install` 默认装到 `~/Library/Python/3.9/site-packages`（用户级），不影响系统 Python
- 装完后 `markdown_py` / `weasyprint` 脚本在 `~/Library/Python/3.9/bin`（**不在 PATH**）

**修复**（一次性）：

```bash
pip3 install --user markdown weasyprint
python3 -c "import markdown, weasyprint"  # 必须两个都 OK
```

**依赖装好后两种调用方式都 work**：
```bash
# 方式 1：绝对路径（最稳，永远 work）
python3 ~/.hermes/skills/md-pdf-report/md2pdf.py file.md

# 方式 2：模块形式（依赖已装时才 work）
python3 -m md2pdf file.md

# 方式 3：软链到 PATH 后（同样依赖要先装）
ln -s ~/.hermes/skills/md-pdf-report/md2pdf.py ~/.local/bin/md2pdf
md2pdf file.md
```

**反模式（不要做）**：
- ❌ 用 `sudo python3 -m pip install` 改系统 Python —— 污染 macOS 系统文件
- ❌ 不装依赖就跑任何 md2pdf 调用 —— 必失败
- ❌ 把 `~/Library/Python/3.9/bin` 加到 PATH ——会和其他工具的同名脚本冲突

**验证清单**（必做）：
```bash
python3 -c "import markdown; print('markdown', markdown.__version__)"
python3 -c "import weasyprint; print('weasyprint', weasyprint.__version__)"
```

---

### ⚠️ Pitfall #6: 飞书 DM 场景下"MEDIA: 路径" ≠ 附件投递（2026-06-11 复现）

**症状**：PDF 已经在本地生成（`ls -lh file.pdf` 有 2.4MB），assistant 自然回复里也写了 `MEDIA:/Users/.../file.pdf`，但用户立刻反馈"把 PDF 发到对话框"——**飞书对话框里看不到附件**。

**根因**：
- assistant 消息里的 `MEDIA:` 前缀在 **Telegram / Discord** 等平台大概率被 gateway 处理为附件投递
- 但在 **飞书 DM 场景**，feishu plugin 的消息解析**不识别**纯文本里的 `MEDIA:` 路径（不是合法 markdown，也不是 send_message 的 file attachment API）
- 结果：飞书只渲染文本消息，**不**上传文件 → 用户看不到附件

**修复（飞书 DM 场景必做）**：

```python
# ❌ 错误姿势：assistant 自然回复里写路径
print("MEDIA:/Users/.../file.pdf")  # 飞书不会上传！

# ✅ 正确姿势：用 send_message 工具
send_message(
    action="send",
    target="feishu",
    message="📄 报告标题\n\nMEDIA:/Users/.../file.pdf"
)
# 返回 message_id 才算成功
```

**判断用哪种姿势**：
| 平台 | 推荐姿势 | 备选 |
|------|---------|------|
| 飞书 DM | `send_message` 工具（必须） | 不可降级 |
| Telegram DM/群 | `send_message` 工具 | 自然消息里 `MEDIA:` 大概率也行 |
| Discord | `send_message` 工具 | 自然消息里 `MEDIA:` 大概率也行 |
| 飞书群/多平台 fan-out | `send_message` 工具，`target="all"` | — |

**完成定义（VBC）**：
1. `ls -lh file.pdf` — 本地有文件 ✓
2. `pdfinfo file.pdf | grep Pages` — 验证渲染 ✓
3. `send_message` 返回值含 `message_id` — 对话框收到附件 ✓
**三步全 OK 才能告诉用户"PDF 已交付"**

**send_message 投递大文件可能 timeout（2026-06-11 复现）**：

- **症状**：`send_message(target="telegram", message="...MEDIA:/path/to/big.pdf")` 返回 `success: true` + `message_id`，但 `warnings: ["Failed to send media ...pdf: Timed out"]` —— **消息文本发出去了，附件没上传**
- **触发条件**：通常是大文件（> 1.5MB，PDF 字体嵌入后常见）+ Telegram。飞书反而更稳
- **修复姿势**：
  1. **先验证 send_message 返回的 `warnings` 字段** —— `success: true` ≠ 附件成功
  2. **第一次失败后重试一次**（多数情况 2-3 次内成功）
  3. **重试前可以考虑复制到 `/tmp/`** 改用短 ASCII 文件名（避开中文文件名 + 长路径可能引发的 edge case）
  4. **3 次仍失败** → 降级方案：把 PDF 路径 + 关键摘要用纯文本发，告诉用户"附件上传超时，请到本地路径查看"

```python
# 健壮投递模板（按 attachments 是否真的上传决定要不要重试）
result = send_message(action="send", target="telegram", message=f"...\n\nMEDIA:{path}")
warnings = result.get("warnings", [])
if any("media" in w.lower() or "timed out" in w.lower() for w in warnings):
    # 附件失败 → 重试
    result = send_message(action="send", target="telegram", message=f"...\n\nMEDIA:{path}")
# 仍失败 → 降级文本说明
```

**为什么不在 Pitfall #6 主线写**：Pitfall #6 解决"压根没投递"的问题（assistant 自然消息 vs send_message 工具），这里的失败是"已经用对了工具但附件本身 timeout"，是不同的失败层次。

---

## ⚠️ Pitfall #7: weasyprint 不生成可点击 link annotation（必须后处理）

**症状**（2026-07-29 UNI 费用开关报告复现）：
- 用户要求"每条断言/数据下面附来源链接"
- MD 里的 `[文字](https://...)` 正常渲染为带下划线的蓝色文字
- **但 PDF 里链接点不开** —— 鼠标悬停不变手型，点击无反应
- macOS Preview / Chrome PDF viewer 都识别不到链接

**根因**（实测验证）：
- `weasyprint.HTML(string=html).write_pdf()` **默认不输出 PDF Link annotation**
- HTML 里 `<a href="...">` 会被渲染为带样式的可见文字，但 PDF 字节流里 `/URI` 标记数 = 0
- 实测 5 个场景（baseline / base_url / stylesheets / presentational_hints / 段落多链接）URI 全是 0
- 这是 **weasyprint 66.0 的设计行为**，不是 bug，也没有"打开开关"的 API

**为什么不能靠改 CSS / base_url 修复**：
- CSS 加 `text-decoration: underline` 能让链接视觉上像链接，但 PDF annotation 还是不生成
- 加 `base_url` 只影响相对路径解析，对绝对 URL 无影响
- `presentational_hints=True` 不存在该参数

**唯一修复方案：pikepdf 后处理**

完整流程（已实测通过，51/68 annotation 命中，macOS Preview 可点）：

```bash
python3 -m pip install --user pikepdf pdfminer.six
```

```python
from pikepdf import Pdf, Name, Dictionary, Array
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer
import re

LINK_RE = re.compile(r'\[([^\]]+)\]\((https?://[^)]+)\)')
md_links = LINK_RE.findall(md_text)  # 不去重!表格里同一 URL 多行要各算一个

# Step 1: weasyprint 渲染 PDF(写到中间文件,pikepdf 不能覆盖输入)
HTML(string=html).write_pdf('/tmp/tmp.pdf')

# Step 2: pdfminer 抽每页 LTTextContainer + bbox
layouts = list(extract_pages('/tmp/tmp.pdf'))
page_blocks = []
for layout in layouts:
    blocks = [el for el in layout if isinstance(el, LTTextContainer)]
    page_blocks.append(blocks)

# Step 3: 按 link_text 匹配 block,记录 (url, bbox, link_text)
# 关键:不去重 + used_blocks 防止同一 block 被多个链接误占
used_blocks = set()
matched_per_page = [[] for _ in layouts]

for link_text, url in md_links:
    target = link_text.lower().strip()
    fingerprint = target[:25] if len(target) > 25 else target
    found = False
    for p_idx, blocks in enumerate(page_blocks):
        for b_idx, block in enumerate(blocks):
            key = (p_idx, b_idx)
            if key in used_blocks:
                continue
            block_text = block.get_text().lower()
            if target in block_text:
                matched_per_page[p_idx].append((url, block.bbox, link_text))
                used_blocks.add(key)
                found = True
                break
        if found:
            break
    if not found:
        # fingerprint 兜底
        for p_idx, blocks in enumerate(page_blocks):
            for b_idx, block in enumerate(blocks):
                key = (p_idx, b_idx)
                if key in used_blocks:
                    continue
                block_text = block.get_text().lower()
                if fingerprint in block_text:
                    matched_per_page[p_idx].append((url, block.bbox, link_text))
                    used_blocks.add(key)
                    found = True
                    break
            if found:
                break

# Step 4: pikepdf 写入 Link annotation(注意 padding 扩大点击区)
pdf = Pdf.open('/tmp/tmp.pdf')
for i, page in enumerate(pdf.pages):
    annots = page.get('/Annots', Array([]))
    for url, (x0, y0, x1, y1), _ in matched_per_page[i]:
        # 表格 cell bbox 偏小,padding 让点击更容易命中
        width = float(x1 - x0)
        pad_h = 4 if width < 150 else 2
        rect = [float(x0)-pad_h, float(y0)-2, float(x1)+pad_h, float(y1)+2]
        annot = Dictionary(
            Type=Name('/Annot'),
            Subtype=Name('/Link'),
            Rect=Array(rect),
            Border=Array([0, 0, 0]),
            A=Dictionary(Type=Name('/Action'), S=Name('/URI'), URI=url)
        )
        annots.append(annot)
    page['/Annots'] = annots
pdf.save('/tmp/final.pdf')
```

**VBC 验证清单（用户交付前必过）**：
1. `pdfinfo final.pdf | grep Pages` — 页数 OK
2. 统计 annotation 数:应接近 MD 里链接数（不去重 50–70% 命中率，去重 100%）
3. macOS Preview 打开 hover 链接 → 手型 + 点击跳转
4. 表格列里**每个 cell 链接都点得开**（不是只有第一个）

**已知陷阱**：
- **表格 cell 链接**：`LTTextContainer.bbox` 是整 cell 的 bbox，不是精确链接文字 bbox。必须给 Rect 加 padding（横向 4pt、纵向 2pt），否则用户点 cell 边缘会落空
- **同 URL 多行出现**：**不能去重**！表格里 CoinGecko 出现 4 次 = 要 4 个独立 annotation，各指各的 cell。`set(md_links)` 会丢 3 个
- **pikepdf 不允许覆盖输入文件**：先 weasyprint 写到 `/tmp/tmp.pdf`，pikepdf 打开后再 `save('/tmp/final.pdf')`
- **简写引用未匹配是正常的**：`[Blockworks]`（6 字符）+ fingerprint 25 字符兜底，文本完全一致但被前面的 `[Blockworks — Uniswap finally turns the fee switch]` 先占了 block，命中率为 0。可接受（不影响核心可点性）

**完成定义**（用户验收）：
- macOS Preview 打开 → 鼠标悬停链接变手型 ✓
- 点击跳转浏览器打开 URL ✓
- 表格里**每一行**的来源链接都能点（不是只第一个）✓
- 链接文字后不显示完整 URL（CSS 不加 `content: attr(href)`，保持视觉干净）

**参考脚本位置**：`/tmp/regen.py`（验证可用的完整流程，下次直接复用）

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
├── md2pdf.py                   # 主转换模块（绝对路径调用 / 软链 / 模块形式均可）
├── templates/
│   ├── research-report.md     # 调研报告模板（自己的研究输出）
│   ├── research-digest.md     # 研究消化模板（消化别人研究，必出批判性分析）
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

> **注意**：旧版 SKILL.md 把 `md2pdf.py` 写在 `scripts/` 子目录下，但实际位于 skill **根目录**。如果以后发现位置真的变了，先 `find ~/.hermes/skills/md-pdf-report -name "md2pdf.py"` 确认。

**软链到 PATH（可选）：**
```bash
ln -s ~/.hermes/skills/md-pdf-report/md2pdf.py ~/.local/bin/md2pdf
chmod +x ~/.hermes/skills/md-pdf-report/md2pdf.py
# 然后直接用: md2pdf report.md
# ⚠️ 前提：依赖已装（见 Pitfall #5）
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
- **首次跑报 `ModuleNotFoundError: No module named 'markdown'` 或 `'weasyprint'`** → macOS 系统 Python 缺依赖，`pip3 install --user markdown weasyprint`（详细见 Pitfall #5）
- **`python3 -m md2pdf` 找不到模块** → `md2pdf.py` 在 skill 根目录不在 `scripts/`，改用绝对路径：`python3 ~/.hermes/skills/md-pdf-report/md2pdf.py file.md`
- **飞书 DM 场景用户看不到 PDF 附件** → assistant 自然消息里的 `MEDIA:` 路径在飞书 DM 不被处理为附件投递，必须用 `send_message` 工具（详细见 Pitfall #6）
