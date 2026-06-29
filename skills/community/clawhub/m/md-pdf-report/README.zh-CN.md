# md-pdf-report · Markdown 双产物报告

> **English** | **[简体中文](./README.md)** (You are here)

一份 Markdown 源文件，两个交付物：可编辑的 `.md` + 可分享的 `.pdf`。原生支持中文（CJK）字体。专为 Hermes Agent / Claude Code / OpenClaw 优化。

---

## 为什么需要这个 Skill

AI Agent 写长文分析（调研 / 事实核查 / 方案 / 对比）的标准流程总是这样结束：

1. Agent 写出一份长 Markdown 报告
2. 用户想要 **PDF** 版本（方便查看 / 分享 / 打印）
3. 用户在**另一台设备**（手机飞书 / 另一台电脑的微信）上，访问不到本机文件
4. Agent 只能用很 hack 的方法：把 PDF 用 base64 贴在聊天里 / 转成图片 / 告诉用户"文件在 `/tmp/xxx.pdf`"（但用户打不开）

**md-pdf-report** 一次解决三个问题：

- **Markdown 是单一事实源**——可编辑、可分发给其他 Agent、可结构化解析
- **PDF 从 Markdown 生成**——一条命令，MD 和 PDF 永远不会内容漂移
- **两个文件都通过 `MEDIA:` 协议发到聊天**——用户在任意设备都能下载

---

## 它能做什么

| 输入 | 输出 | 适用场景 |
|------|------|---------|
| `report.md` | `report.pdf` + 自动发到对话 | 调研报告、事实核查、方案、投资分析 |
| 多章节 Markdown | 带 callout/表格/代码块的样式化 PDF | 长文分析（> 1 页 A4） |
| 中文 / 中英混排 | 原生 CJK 渲染，无方块乱码 | 双语分析内容 |

**不适用场景**（用其他 skill）：
- PPT/slides/deck → `kami` skill
- 简历/白皮书/作品集/一页纸 → `kami` skill
- PNG/图片导出 → 图像生成工具
- 短消息/通知 → 直接发文字

---

## 设计思路

### 为什么选 weasyprint，不用 reportlab 或 pandoc？

| 引擎 | 代码复杂度 | 中文 | 安装难度 | 输出大小 | 样式灵活度 |
|------|----------|------|---------|---------|-----------|
| **weasyprint** ⭐ | 低（HTML+CSS） | ✅ | 需 `brew install pango` | 2-3 MB/页 | ⭐⭐⭐⭐⭐ |
| reportlab | 中（Python API） | ✅ | 纯 pip | 0.3 MB/页 | ⭐⭐⭐ |
| pandoc + LaTeX | 最低（纯 MD） | ✅ | MacTeX 5GB+ | 1-2 MB/页 | ⭐⭐⭐⭐ |

选 weasyprint 的理由：
- **CSS 比 reportlab 的 `ParagraphStyle` API 好读 10 倍**
- **不用装 5GB 的 LaTeX**（用户是 Mac，不是 build server）
- **MD → HTML → PDF 是干净的流水线**——好调试、好扩展
- **2-3 MB/页的成本可接受**——飞书/Telegram 都能直接发

完整对比见 `references/pdf-engine-comparison.md`。

### 为什么 "Markdown 作为事实源"？

因为同一份内容要服务三类受众：

1. **用户，看最终报告** → 想要 PDF
2. **用户，以后要编辑** → 想要 MD
3. **其他 Agent，要解析内容** → 想要 MD（可解析、有结构）

如果 PDF 是源文件，编辑性和可解析性就丢了。如果两个文件从模板各自生成，一定会漂移。**所以 MD 是规范，PDF 是衍生品。**

### 为什么用 `MEDIA:` 自动发到对话？

因为用户通常在另一台设备。本机路径在跨设备场景下完全没用。**`MEDIA:` 前缀是 Hermes / 飞书 / Telegram 中唯一可靠的跨设备文件投递机制。** 这个规则被强制写入 skill 顶部的"必做最后一步"。

---

## 安装

### 一键安装（推荐）

```bash
# 一条命令——装到默认 skills 目录
npx clawhub@latest install 0xcjl/md-pdf-report

# 或者用 clawhub CLI
clawhub install md-pdf-report
```

### 手动安装

```bash
# 1. 克隆仓库
git clone https://github.com/0xcjl/md-pdf-report.git

# 2. 软链到 agent 的 skills 目录
# OpenClaw:
ln -sf $(pwd)/md-pdf-report ~/.openclaw/skills/md-pdf-report

# Hermes Agent:
ln -sf $(pwd)/md-pdf-report ~/.hermes/skills/md-pdf-report

# Claude Code:
ln -sf $(pwd)/md-pdf-report ~/.claude/skills/md-pdf-report

# 3. 装 Python 依赖
pip install weasyprint markdown
```

### 一次性系统配置（macOS）

weasyprint 需要 pango / cairo / gobject C 库。macOS 默认不带：

```bash
brew install pango
```

`md2pdf.py` 模块导入时会自动 bootstrap 库路径（设置 `DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib`），不需要手动设环境变量。

**验证安装：**

```bash
python3 -c "from weasyprint import HTML; HTML(string='<h1>测试</h1>').write_pdf('/tmp/test.pdf'); print('OK')"
```

打印 `OK` 就 OK。如果报 `libgobject` 错误，看 `references/weasyprint-bootstrap.md`。

---

## 使用

### 作为 Skill（推荐）

在 agent 对话里说任意一句：

- "输出 PDF" / "导出 PDF" / "转成 PDF" / "做成 PDF" / "保存成 PDF"
- "给我个 PDF 版本" / "以 PDF 格式输出"
- "convert to PDF" / "save as PDF" / "export PDF"

skill 会自动触发，生成 PDF，**并把 `.md` 和 `.pdf` 两个文件都发到对话**，你在任何设备都能下载。

### 作为 CLI

```bash
# 基本用法
python3 md2pdf.py report.md

# 自定义输出路径
python3 md2pdf.py report.md -o final.pdf

# 保留中间 HTML（用于调试）
python3 md2pdf.py report.md --keep-html

# 作为模块运行
python3 -m md2pdf report.md
```

### 作为 Python API

```python
from md2pdf import md_to_pdf

# 默认：输出到同目录的 report.pdf
md_to_pdf("report.md")

# 自定义输出
md_to_pdf("report.md", "out.pdf")

# 保留中间 HTML（用于调试）
md_to_pdf("report.md", keep_html=True)

# 自定义 CSS
from md2pdf import DEFAULT_CSS
md_to_pdf("report.md", css=DEFAULT_CSS + "h1 { color: #B91C1C; }")
```

---

## 支持的 Markdown 语法

标准 GitHub-flavored Markdown 全部开箱即用：

- 标题（`#`, `##`, `###`）
- 列表（有序/无序/嵌套）
- 表格
- **加粗**、*斜体*、`行内代码`
- 链接 `[文字](url)`
- 代码块（带语言提示）
- 引用 `>`
- 分隔线 `---`

另外三个自定义 `<div>` 类用于样式化 callout：

```html
<div class="callout">
  <b>重要：</b>红色边框的 callout，用于关键结论或警示。
</div>

<div class="note">
  浅灰色注释 / 补充信息。
</div>

<div class="warn">
  黄色警告提示。
</div>
```

`templates/` 下有三个现成的脚手架：

- `fact-check.md` — claim → verification → context 结构
- `research-report.md` — 调研 / 分析结构
- `scheme.md` — 方案 / 提案 / 计划结构

---

## 架构

```
md-pdf-report/
├── SKILL.md                          # Skill 定义（中文，agent 用）
├── README.md                         # 英文 README（GitHub 主页）
├── README.zh-CN.md                   # 中文 README（本文件）
├── md2pdf.py                         # 主模块（CLI + Python API）
├── references/
│   ├── pdf-engine-comparison.md      # 为什么选 weasyprint
│   ├── macos-cjk-fonts.md            # 为什么 .ttc 不行 / 用哪些 .ttf
│   └── weasyprint-bootstrap.md       # 修复 "cannot load libgobject" 错误
├── templates/
│   ├── fact-check.md                 # 事实核查脚手架
│   ├── research-report.md            # 调研报告脚手架
│   └── scheme.md                     # 方案脚手架
└── examples/
    ├── test_report.md                # 最小功能测试
    └── Mike_Lynch_FactCheck.md       # 真实 7 页事实核查报告
```

---

## 验证过的输出

`examples/Mike_Lynch_FactCheck.md` 是一个 14 KB 的 Markdown 文件，能产出：

- **7 页 A4 PDF**，1951 个中文字符全部正确渲染
- **表格 / callout / 代码块 / 36 个来源链接**全部样式化
- **页脚**带 `1 / 7` 风格分页
- **最终 2.4 MB**（weasyprint 嵌入完整字体以保证跨平台可读）

重新生成：

```bash
python3 md2pdf.py examples/Mike_Lynch_FactCheck.md
```

---

## 自定义

### 自定义 CSS

```python
from md2pdf import md_to_pdf, DEFAULT_CSS

# 加品牌色
md_to_pdf(
    "report.md",
    css=DEFAULT_CSS + """
        h1 { color: #B91C1C; }
        .callout { background: #FEFCE8; border-color: #FACC15; }
    """
)
```

### 自定义字体

编辑 `md2pdf.py` 顶部的 `FONT_BODY` / `FONT_HEADING` / `FONT_KAITI` 变量，指向你自己的 `.ttf` 文件。macOS 路径参考 `references/macos-cjk-fonts.md`。

---

## Credits

- **构思与实现**: [0xcjl](https://github.com/0xcjl)
- **CJK 字体研究**: 从 `reportlab.pdfbase.ttfonts.TTFError` 报错出发 → 排查 `.ttc` PostScript outlines 不兼容 → 发现 `/System/Library/AssetsV2/` 下的 `.ttf`
- **触发关键词设计**: 受 `kami` skill（同为 0xcjl 出品）的"自然语言优先"哲学启发
- **真实测试案例**: Mike Lynch / 贝叶斯号事实核查报告 —— 2026-06-11 通过 Hermes DM 频道发布，作为完整 MD → PDF → 对话投递流水线的演示

---

## License

MIT
