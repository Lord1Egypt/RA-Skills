# Math-Docx-Typeset 使用指南

> 名称：`math-docx-typeset`｜版本：1.2
> 一句话：把含数学公式的学术文稿转成 **docx，公式为 Word 原生可编辑 OMML 对象**（双击可改，不是图片）。可选生成图片对照版附件，自选比对。
> 安装：解压后把 `math-docx-typeset` 文件夹放入 skills 目录（Mac：`~/.workbuddy/skills/`，Windows：`C:\Users\<用户名>\.workbuddy\skills\`），相对路径引用，跨平台通用。

## 一、它能做什么 / 不能做什么

| 能 | 不能（硬性禁止） |
|---|---|
| 论文正文 + 数学推导 → docx，公式为原生 OMML（双击可编辑） | ❌ 主文档公式渲染成 PNG/JPG/SVG 图片嵌入（图片公式不可双击编辑） |
| 识别 `$...$` 行内公式、`$$...$$` 块居中公式 | ❌ 生成 PPT |
| 矩阵、cases 分段、align 多行拆行、`\tag` 编号 | ❌ 直接生成 PDF（由你本地 Word/WPS 另存 PDF，矢量高清） |
| 正文宋体 + Times New Roman、1.5 倍行距、块公式居中（可参数化） | ❌ 修改 / 简化 / 删减你的数学符号与推导步骤 |
| GB/T 15834 引号自动修正（中文内容直引号转弯引号，保护代码 / URL）| ❌ 用图片公式兜底转换失败 |
| 转换失败自动降级：保留 LaTeX 原文 + 黄色高亮标注，任务不中断 |  |
| **图片对照版附件**（`--image-variant`，块公式为 PNG，**使用者自选**）|  |

## 二、调用提示词（直接复制用）

**完整版指令**：

```
启动 math-docx-typeset。将下面这份学术推导 / 论文正文生成 docx 文档，
所有数学内容生成 Word 原生可编辑公式，不要图片公式，我后续本地导出 PDF。
【粘贴你的论文 / 推导文本】
```

**极简版指令**：

```
math-docx-typeset，生成 docx，原生可编辑公式，文稿内容：【粘贴内容】
```

**带公式的截图输入**：

```
启动 math-docx-typeset。把下面截图里的推导转成 LaTeX（OCR + 视觉 read，
符号查 references/symbol-table.md，不确定的列"已假设"清单），然后生成 docx 原生公式文档。
【附截图】
```

**同时要图片对照版**：

```
math-docx-typeset，生成 docx，附图片对照版（块公式 PNG 形式），自选比对，文稿内容：【粘贴内容】
```

**自定义排版**：

```
math-docx-typeset，生成 docx，正文字体用黑体、字号五号、行距 1.25，文稿内容：【粘贴内容】
```

## 三、脚本直接用法（命令行）

```bash
# 首次装依赖（纯 Python，无需 TeX 环境）
pip install latex2mathml mathml2omml python-docx matplotlib

# 主文档（默认：宋体 / 12pt 小四 / 1.5 倍行距 / 块公式居中 / GB/T 15834 引号修正）
python scripts/latex2docx.py 输入文稿.md 输出.docx

# 自定义排版
python scripts/latex2docx.py 输入文稿.md 输出.docx --font 黑体 --size 10.5 --leading 1.25

# 同时生成图片对照版附件
python scripts/latex2docx.py 输入文稿.md 输出.docx --image-variant
# 产出：输出.docx（主，OMML 原生公式）+ 输出-图片对照版.docx（附件，PNG 公式对照）
```

输入文稿格式：`.md` / `.txt`，公式用 `$...$`（行内）和 `$$...$$`（块居中）标记；`#` `##` `###` 转为 Word 标题。

运行后输出转换报告：主文档成功 / 降级 / 降级清单；图片对照版渲染 / 不可用 / 不可用清单。

## 四、文稿里的公式怎么写（速记）

| 场景 | 写法 |
|---|---|
| 行内 | `$E = \hbar^2 k^2 / 2m$` |
| 块居中 | `$$ \int_{-\infty}^{\infty} e^{-x^2}\,dx = \sqrt{\pi} $$` |
| 带编号 | `$$ \rho(x) = |\psi(x)|^2 \tag{3.7} $$` |
| 矩阵 | `\begin{bmatrix} a & b \\ c & d \end{bmatrix}` |
| 多行推导 | 包在 `\begin{align} ... \end{align}` 里，`&` 对齐，`\\` 换行 |
| 向量 / 数域 | `\boldsymbol{x}`、`x \in \mathbb{R}` |
| 不等号 | `\le` `\ge`（不用 `<=` `>=`） |
| 公式内含少量中文 | `\text{且}`（主文档 OMML 正常，图片对照版不可用会标注） |

**禁用扩展包命令**：`\pdv` `\dv` `\braket`（physics 包）、`\cancel`、`\bm`——链路不支持，会触发降级。替代写法：`\frac{\partial f}{\partial x}`、`\langle \phi | \psi \rangle`、`\boldsymbol{v}`。完整边界见 `references/formula-rules.md` §八。

## 五、降级预案说明

**主文档**：转换失败的公式在原位保留**完整 LaTeX 代码** + 黄色高亮【公式转换失败，复制本段 LaTeX 粘贴进 Word 公式编辑器即可生成】。处理：打开 docx，找到黄色高亮处，复制那段 LaTeX，在 Word 里按 `Alt + =` 进入公式编辑器粘贴，回车即得原生公式。任务不中断。

**图片对照版附件**：渲染失败（含 CJK、矩阵等 `\begin{}` 环境）的公式同样保留 LaTeX 原文 + 黄高亮【图片对照不可用，请以主文档公式为准】。

## 六、字体显示方案（避免方块）

本 skill 的 OMML 路线天然免疫大部分"方块"问题（公式由 Cambria Math 渲染）。三类排版场景完整策略：读取 `references/font-strategy.md`。

| 场景 | 风险 | 解决 |
|---|---|---|
| docx OMML 公式 | 低 | 装 Cambria Math（Office 自带） |
| docx 正文 Unicode 字符（ℝ、⁰）| 中：宋体覆盖不全 | 改字符字体为 Cambria Math / STIX Two Text，或把字符收进公式 |
| docx 另存 PDF 后方块 | 中 | 勾选"嵌入所用字体" |
| 图片对照版（matplotlib）| 高：无 CJK、不支持 `\begin{}` | 标注"图片对照不可用" |
| Markdown→PDF（reportlab）| 见 `references/font-strategy.md` §二对照 | 与本 skill 互为补充 |

**专业学术论文字体方案速选**：

- **国内学位论文（OMML 路线）**：宋体（中文）+ Times New Roman（西文）+ Cambria Math（公式）
- **LaTeX 期刊系**：newtxmath（Times 系） / stix2（STI Pub 标准，Unicode 数学覆盖最全）/ libertinus（开源现代）
- **通用 Unicode 数学字体**（独立字符级设置）：Cambria Math / STIX Two Math / Noto Sans Math / Latin Modern Math

字体覆盖检查命令（fontTools cmap，附件方法对 docx 同样适用）见 `references/font-strategy.md` §五。

## 七、与其他 skill 的关系

- **feynman-research**（调研）：其报告含公式时交本 skill 落地 docx
- **math-pdf-typeset**（你已有，Markdown→PDF 链路）：附件《math-pdf-typeset 符号还原完整方案》四层防线（字体双轨 + 符号映射 + 占位符保护法 + 缺字扫描）适用于 reportlab PDF 场景；本 skill 专注 docx/OMML 路线；`references/font-strategy.md` §二做了三类场景对照
- **math-formula**（之前版本，单条公式轻量排版）：已被本 skill 取代；本 skill 入口拆为"主文档（OMML）"+"图片对照版附件（PNG，自选）"

## 八、第三方依赖与许可证

本 skill 全部自有代码均为原创。运行所需的第三方依赖（`latex2mathml` / `mathml2omml` / `python-docx` / `matplotlib`）均为 MIT 或 BSD 风格宽松许可证，无 GPL 类传染性义务；本 skill **不打包这些库的源码**，由 `pip install` 安装，各包 LICENSE 随 PyPI 分发。完整声明（含 attribution 要求与上游思路说明）见 **`THIRD_PARTY.md`**。
