# thuthesis 论文排版格式指南

本文档整理了清华大学硕士/博士学位论文（thuthesis 模板）排版中的常见需求和最佳实践，
适用于 thuthesis v7.x 系列。

---

## 1. 黑白打印图表生成规范

学位论文最终提交版通常需要黑白打印。所有图表必须在无颜色的情况下仍可清晰区分数据系列。

### 1.1 核心原则：figsize 与 textwidth 的 1:1 对应

**关键公式：** matplotlib `figsize` 的宽度必须等于 LaTeX 中实际显示宽度，这样字号才能 1:1 保持。

```python
# thuthesis 默认 textwidth ≈ 150mm ≈ 5.91 inches
DISPLAY_W = 5.91  # inches — 对应 LaTeX 中 \textwidth

# LaTeX 端使用：
# \includegraphics[width=1\textwidth]{myfigure/xxx.png}
# 这样 matplotlib 中设置的字号 = PDF 中实际显示的字号
```

**错误示范：** `figsize=(10, 6)` + `\includegraphics[width=0.8\textwidth]` → 字号会被缩小约 50%

### 1.2 字号标准

```python
FS       = 10   # 正文字号（图标题、轴标签、图例、注释）
FS_TICK  = 8    # 刻度标签字号（坐标轴数字）
FS_SMALL = 8    # 最小允许字号（论文中不应出现小于 8pt 的文字）
```

**铁律：论文图表中所有文字不得小于 8 号字（约 8pt）。**

### 1.3 黑白区分手段

在无颜色的情况下区分数据系列，使用以下方法：

#### 折线图
```python
LINE_STYLES = ['-', '--', '-.', ':']
MARKERS     = ['o', 's', '^', 'D', 'v', 'p', 'h']
GRAY_SHADES = ['#000000', '#444444', '#888888', '#BBBBBB']
```

#### 柱状图
```python
HATCHES = ['//', '\\\\', '..', 'xx', '++', '||', '--', 'oo']
# 搭配浅灰填充色
BAR_COLORS = ['#FFFFFF', '#CCCCCC', '#888888', '#444444']
```

#### 雷达图/散点图
```python
# 使用不同 marker + 线型组合
# 填充 vs 空心 marker 也可用于区分
```

### 1.4 完整模板

```python
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# === 全局参数 ===
DISPLAY_W = 5.91  # inches = thuthesis \textwidth
FS       = 10
FS_TICK  = 8
FS_SMALL = 8
DPI      = 300

plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Songti SC', 'STSong', 'SimSun', 'Times New Roman'],
    'font.size': FS,
    'axes.unicode_minus': False,
    'axes.labelsize': FS,
    'axes.titlesize': FS,
    'xtick.labelsize': FS_TICK,
    'ytick.labelsize': FS_TICK,
    'legend.fontsize': FS_SMALL,
    'figure.dpi': DPI,
})

def create_figure(height_ratio=0.618):
    """创建标准尺寸图表"""
    W = DISPLAY_W
    H = W * height_ratio
    fig, ax = plt.subplots(figsize=(W, H))
    return fig, ax

def save_figure(fig, filename, output_dir='myfigure'):
    """保存图表"""
    import os
    path = os.path.join(output_dir, filename)
    fig.savefig(path, dpi=DPI, bbox_inches='tight', pad_inches=0.02)
    plt.close(fig)
    print(f"Saved: {path}")
```

### 1.5 常见问题与解决

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| 图中文字太小 | figsize 过大导致缩放 | 确保 figsize 宽度 = DISPLAY_W |
| 坐标轴标签重叠 | 数据点太密或图太窄 | 旋转标签 / 增大子图比例 / `gridspec_kw` 调宽 |
| 图例遮挡数据 | 图例位置不当 | `loc='best'` 或手动指定 `bbox_to_anchor` |
| 中文乱码 | 字体未正确配置 | macOS: `Songti SC`, Windows: `SimSun`, Linux: `WenQuanYi` |
| 注释文字重叠 | 同一位置多个标注 | 上方系列 `va='bottom'`，下方系列 `va='top'` |

---

## 2. 表格格式规范

### 2.1 threeparttable 表格脚注

当表格需要脚注时，必须使用 `threeparttable` 环境：

```latex
\begin{table}[htbp]
  \centering
  \caption{表格标题}
  \label{tab:example}
  \begin{threeparttable}
    \begin{tabular}{llll}
      \toprule
      列1 & 列2 & 列3 & 列4 \\
      \midrule
      数据\tnote{①} & 数据 & 数据 & 数据 \\
      数据 & 数据\tnote{②} & 数据 & 数据 \\
      \bottomrule
    \end{tabular}
    \begin{tablenotes}[flushleft]
      \small
      \item[①] 脚注内容一
      \item[②] 脚注内容二
    \end{tablenotes}
  \end{threeparttable}
\end{table}
```

**注意：** thuthesis 已包含 `threeparttable` 宏包，无需额外加载。

### 2.2 长表格

跨页表格使用 `longtable` 环境，thuthesis 已预置支持。

---

## 3. 签名插入

### 3.1 授权声明页签名

在 `thuthesis.cls` 中找到 `\thu@authorization@mk` 定义，修改签名行：

```latex
作者签名：\hspace{4bp}\thu@underline[7em]{%
  \includegraphics[height=3.6em]{myfigure/sig-author.jpg}%
}\hspace{47bp}%
导师签名：\hspace{4bp}\thu@underline[7em]{%
  \includegraphics[height=1.8em]{myfigure/sig-advisor.jpg}%
}\par
\vskip 6bp%
日\hspace{2em}期：\hspace{4bp}\thu@underline[7em]{2026年X月X日}\hspace{47bp}%
日\hspace{2em}期：\hspace{4bp}\thu@underline[7em]{2026年X月X日}\par
```

### 3.2 声明页签名

在 `thuthesis.cls` 中找到声明页的签名部分：

```latex
\thu@signature\thu@underline[76bp]{%
  \includegraphics[height=3.6em]{myfigure/sig-author.jpg}%
}\hspace{-3bp}%
\thu@backdate\thu@underline[105bp]{2026年X月X日}\par
```

### 3.3 签名图片要求

- 格式：JPG 或 PNG（白底黑字扫描件）
- 建议：去除白色背景或使用高对比度扫描
- `height` 参数调整签名大小，不同签名可能需要不同值
- 作者签名一般 `height=3.0em~4.0em`，导师签名可能不同

---

## 4. 页面样式控制

### 4.1 声明页页眉/页脚

thuthesis 的 `\statement` 命令接受 `page-style` 参数：

```latex
% 在 my-thesis.tex 中：
\statement[page-style=plain]   % 有页眉（显示"声明"）和页脚（页码）
\statement[page-style=empty]   % 无页眉页脚（默认）
```

**注意：** 对于 graduate 模式，`plain` 样式自带 headrule + `\leftmark` header + 页码 footer。

### 4.2 pagestyle 覆盖规则

LaTeX 中 `\thispagestyle` 遵循"最后调用者胜出"原则：
- `\chapter*` 内部调用 `\CTEX@setthispagestyle{chapter}` → 使用 `\ps@chapter`（空样式）
- 如果 `\statement` 的 `page-style=plain`，它会在 `\chapter*` 之后再调用 `\thispagestyle{plain}`
- 确保在 `my-thesis.tex` 中正确设置参数，而不是去修改 `.cls` 文件

---

## 5. 送审/答辩版本特殊处理

### 5.1 指导教师评语页（只留标题）

```latex
% mydata/comments.tex
\begin{comments}

\end{comments}
```

`comments` 环境会自动生成"指导教师/指导小组学术评语"标题。空的环境体 = 只有标题。

### 5.2 答辩委员会决议书页（只留标题）

```latex
% mydata/resolution.tex
\begin{resolution}

\end{resolution}
```

`resolution` 环境会自动生成"答辩委员会决议书"标题。空的环境体 = 只有标题。

### 5.3 综合论文训练记录表

如果不需要，在 `my-thesis.tex` 中注释掉 `\record{...}` 即可。

---

## 6. 编译环境配置

### 6.1 编译命令

```bash
# macOS (MacTeX)
export PATH="/Library/TeX/texbin:/usr/bin:/bin:/usr/sbin:/sbin:$PATH"
cd <thesis-root>
latexmk -xelatex my-thesis.tex

# 清除缓存后重新编译（解决某些编译错误）
latexmk -C && latexmk -xelatex my-thesis.tex
```

### 6.2 字体选择

```latex
\documentclass[degree=master,fontset=fandol]{thuthesis}
% fontset 选项：
%   windows — Windows 系统字体（宋体、黑体等）
%   mac     — macOS 系统字体
%   fandol  — Fandol 开源字体（跨平台，推荐开发阶段使用）
%   ubuntu  — Linux 系统字体
% 建议：开发阶段用 fandol，终版用 windows 编译
```

### 6.3 参考文献

```latex
\bibliography{myref/refs}  % BibTeX 方式（推荐）
% 编译链：xelatex → bibtex → xelatex → xelatex
% latexmk 会自动处理多次编译
```

---

## 7. 常用 thuthesis 文件结构

```
thesis-root/
├── my-thesis.tex          # 主文件
├── thusetup.tex           # 论文元信息（标题、作者、导师等）
├── thuthesis.cls          # 模板类文件（谨慎修改）
├── mydata/
│   ├── abstract.tex       # 摘要
│   ├── chap01.tex ~ chap05.tex  # 各章节
│   ├── acknowledgements.tex     # 致谢
│   ├── resume.tex         # 个人简历
│   ├── comments.tex       # 指导教师评语
│   ├── resolution.tex     # 答辩委员会决议书
│   ├── committee.tex      # 委员会名单
│   └── denotation.tex     # 符号对照表
├── myfigure/
│   ├── *.py               # 图表生成脚本
│   ├── *.png              # 生成的图片
│   └── sig-*.jpg          # 签名图片
└── myref/
    └── refs.bib           # 参考文献库
```
