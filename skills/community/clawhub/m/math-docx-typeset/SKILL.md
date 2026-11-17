---
name: math-docx-typeset
description: 学术文稿公式排版 → docx：把含 LaTeX 公式的论文/推导转成 Word 原生可编辑 OMML 公式 docx（主交付），可选生成图片对照版附件（由使用者自选）。当用户说“生成 docx / 论文转 Word / 公式排版 / 推导转可编辑公式 / 写论文 docx”时启用。
version: 1.2.1
---

# Math-Docx-Typeset 学术文稿公式排版（docx 路线）

> 主交付：docx 文档，公式一律为 Word 原生可编辑 OMML 对象（双击可改）。**用户本地打开 Word/WPS 核对后另存为 PDF**，矢量高清无模糊。
> 附件模式：--image-variant 生成图片对照版 docx（块公式为 PNG），由使用者**自选比对**，不替代主文档。
> 本 skill 所有 reference 文件均为相对路径引用，跨平台安装即用。

## 硬性禁止清单（最高优先级，不可违反）

- ❌ 不可以修改、简化、改写用户给出的数学符号、推导步骤
- ❌ **主文档**禁止图片格式公式（PNG/JPG/SVG）——图片公式不可双击编辑，不符合论文要求（图片仅作为对照版附件，由使用者自选）
- ❌ 禁止生成 PPT 幻灯片
- ❌ 禁止直接生成 PDF 文件
- ❌ 不可擅自删减上下限、算子、矩阵元素

## 技术转换链路（强制，不可绕过）

```
输入文稿文本
  → GB/T 15834 引号预处理（仅"含汉字的引号"转弯引号）
  → 识别行内公式 $...$ / 块居中公式 $$...$$
  → LaTeX 语法校验（大括号成对、上下标边界、算子命令拼写）
  → LaTeX → MathML → OMML（含质量校验，拦截未知命令被静默当文本）
  → 将 OMML 原生公式对象写入 docx 文档
```

实现脚本：`scripts/latex2docx.py`（沙箱已全链路实测：行内公式、块公式居中、矩阵、数域、cases、align 多行、`\tag` 编号、降级预案、引号修正、图片对照版附件均通过）。

## 数学公式书写规范（生成 LaTeX 时必须严格遵守）

完整规范：读取 `references/formula-rules.md`。要点：

1. **数域符号**：实数域 `\mathbb{R}`、复数域 `\mathbb{C}`、自然数 `\mathbb{N}`
2. **算子符号**：偏导 `\partial`、梯度 `\nabla`、拉普拉斯 `\Delta`、无穷 `\infty`；不等号学术论文标准写法用 `\le`、`\ge`，不用 `<=`、`>=`
3. **积分求和**：定积分 `\int_{a}^{b}`、多重积分 `\iint` / `\iiint`；求和 `\sum_{i=1}^{n}`、乘积 `\prod_{i=1}^n`
4. **向量矩阵**：向量粗体 `\boldsymbol{x}`、矩阵大写粗体 `\boldsymbol{A}`；矩阵优先方括号 `\begin{bmatrix} ... \end{bmatrix}`
5. **多行推导**：统一用 `\begin{align} ... \end{align}`，`&` 作对齐标记（脚本会自动拆行逐行居中）
6. **公式编号**：用户需要编号的块公式，右侧添加 `\tag{数字}`

## 字体显示方案（重要）

OMML 路线天然免疫大部分"方块"问题（公式由 Cambria Math 渲染）。完整方案：读取 `references/font-strategy.md`。要点：

- **正文**：中文宋体（SimSun）、西文 Times New Roman
- **公式**：Cambria Math（Office 2007+ 自带；WPS 兼容）
- **正文 Unicode 字符方块**（如 ℝ、⁰）：改字符字体为 Cambria Math / STIX Two Text，或把字符收进公式（LaTeX 化转 OMML）
- **图片对照版边界**：matplotlib mathtext 不含 CJK 字形（公式内中文出 dummy）、不支持 `\begin{}` 环境（矩阵 / cases）——不可用时标注"图片对照不可用"
- **PDF 嵌入**：另存 PDF 时勾选"嵌入所用字体"

## 输入处理（四通道）

| 输入类型 | 处理 | 详见 |
|---|---|---|
| 已含 LaTeX 的文稿 | 直接进主链路 | `references/transcription.md` §4 |
| 截图 | OCR + 视觉 read 先转成 LaTeX（符号逐个查 `references/symbol-table.md`），再进主链路 | `references/transcription.md` §1 |
| 口述描述 | 自然语言映射为 LaTeX 再进主链路 | `references/transcription.md` §2 |
| 乱码文本 | 排查编码，无法恢复按截图流程重做 | `references/transcription.md` §3 |

## 完整工作执行步骤

1. 通读全部输入文稿，拆分普通正文段落、行内公式、独立居中块公式。
2. 对每一处数学内容生成 LaTeX 代码，自检：所有大括号 `{}` 成对、上下标边界正确、算子命令拼写无误、无语法错误（自检清单见 `references/transcription.md`）。
3. **GB/T 15834 引号预处理**：正文里"含汉字的引号"自动转弯引号（保护公式、代码、URL）。
4. LaTeX 转换为标准 MathML，再转换 OMML 标记片段（**含质量校验**）。
5. 新建 docx 文档；普通文字写入段落；公式位置注入 OMML 原生公式对象。
6. 论文基础排版规范：正文宋体、1.5 倍行距；块级公式居中对齐。
7. （可选）生成图片对照版附件（`--image-variant`），由使用者自选比对。
8. 生成 docx 文件交付用户。
9. 输出交付提示：

> 文件已生成 docx。请本地打开 Word/WPS 核对全部数学公式；确认无误后另存导出 PDF，即可得到矢量高清无模糊的论文 PDF。

## 脚本用法（AI 执行时调用）

```bash
# 依赖（首次）
pip install latex2mathml mathml2omml python-docx matplotlib

# 转换（默认：宋体、12pt 小四、1.5 倍行距、块公式居中、GB/T 15834 引号修正）
python scripts/latex2docx.py 输入文稿.md 输出.docx

# 自定义排版参数
python scripts/latex2docx.py 输入文稿.md 输出.docx --font 黑体 --size 10.5 --leading 1.25

# 同时生成图片对照版附件（块公式为 PNG，自选比对）
python scripts/latex2docx.py 输入文稿.md 输出.docx --image-variant
# 产出：输出.docx（主，OMML 原生公式）+ 输出-图片对照版.docx（附件，PNG 公式对照）
```

脚本自动完成：GB/T 15834 引号修正 → 块公式 / 行内公式识别 → LaTeX→MathML→OMML（含质量校验）→ docx 写入 → 转换报告（成功数 / 降级数 / 降级清单）。

## 降级故障预案（转换失败时强制执行）

当 LaTeX-OMML 转换链路执行失败（含**未知命令被静默当文本**的质量校验失败），**主文档**处理：

1. 在文档对应位置保留完整正确的原始 LaTeX 代码；
2. 代码后标注文字【公式转换失败，复制本段 LaTeX 粘贴进 Word 公式编辑器即可生成】（黄色高亮）；
3. 正常输出 docx 文档，任务不可中断。

**图片对照版**对应处理：matplotlib 渲染失败（含 CJK 或不支持的 `\begin{}` 环境）时，标注【图片对照不可用（含中文或暂不支持的命令），请以主文档公式为准】，保留 LaTeX 原文。

## 实测能力边界（重要）

- ✅ 已验证支持：分式、上下标、根号、求和/积分及上下限、希腊字母、`\hbar`、矩阵（bmatrix）、cases 分段、align 多行（自动拆行）、`\tag` 编号、`\mathbb` 数域、`\boldsymbol` 粗体、`\text{中文}`
- ❌ 不支持（触发降级）：未知命令（如 `\fraz`）、裸 `& ... \\` 多行语法（必须包在 align 环境内）、physics 等扩展包命令
- 未知命令**不会报错**而是被静默当文本写入公式（排版变乱）——脚本已内置 OMML 质量校验拦截此情况
- 图片对照版额外限制：公式内中文（`\text{且}`）和 `\begin{bmatrix}/cases` 等环境（mathtext 不支持）→ 标注"图片对照不可用"

## 与其他 skill 的衔接

- **feynman-research**（调研）：其报告中的公式可经本 skill 落地为 docx 原生公式
- **math-pdf-typeset**（用户已有，Markdown→PDF 链路）：附件《math-pdf-typeset 符号还原完整方案》四层防线的方法（字体双轨 + 符号映射 + 占位符保护法 + 缺字扫描）适用于 reportlab PDF 场景，与本 skill 的 docx/OMML 路线互为补充；本 skill 的 `references/font-strategy.md` §二做了三类场景对照
