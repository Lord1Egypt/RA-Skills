# LaTeX 论文排版参考模板

供 SKILL.md 引用的完整可编译模板与 GB/T 7714—2025 文献条目示例。

## 完整中文毕业论文模板（xelatex + ctex）

```latex
\documentclass[a4paper,12pt]{ctexart}

% ===== 页面 =====
\usepackage[a4paper,left=2.5cm,right=2.5cm,top=2.5cm,bottom=2.5cm]{geometry}

% ===== 字体与行距 =====
\linespread{1.5}\selectfont
\setlength{\parindent}{2em}
\setlength{\parskip}{0pt}

% ===== 标题层级 =====
\ctexset{
  section = { format = \Large\bfseries, beforeskip = 1ex, afterskip = 1ex,
              number = \arabic{section} },
  subsection = { format = \large\bfseries, beforeskip = 0.8ex, afterskip = 0.8ex,
                 number = \arabic{section}.\arabic{subsection} },
  subsubsection = { format = \normalsize\bfseries, beforeskip = 0.6ex, afterskip = 0.6ex,
                    number = \arabic{section}.\arabic{subsection}.\arabic{subsubsection} }
}

% ===== 页眉页脚 =====
\usepackage{fancyhdr}
\pagestyle{fancy}
\fancyhf{}
\fancyhead[C]{论文标题简写}
\fancyfoot[C]{\thepage}
\fancypagestyle{plain}{\fancyhf{}\fancyhead[C]{论文标题简写}\fancyfoot[C]{\thepage}}

% ===== 图表 =====
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{float}

% ===== 参考文献 GB/T 7714—2025 =====
\usepackage[backend=biber, style=gb7714-2025, citestyle=numeric]{biblatex}
\addbibresource{refs.bib}

% ===== 超链接（可选）=====
\usepackage{hyperref}
\hypersetup{colorlinks=true, linkcolor=black, citecolor=black, urlcolor=blue}

\begin{document}
\begin{titlepage}
  \thispagestyle{empty}
  \centering
  {\zihao{2}\bfseries 论文标题\par}
  \vfill
  姓名：\underline{\hspace{8em}}\par
  专业：\underline{\hspace{8em}}\par
  学校：\underline{\hspace{8em}}\par
  指导教师：\underline{\hspace{8em}}\par
  \vfill
  \number\year\ 年 \number\month\ 月 \number\day\ 日
\end{titlepage}

% ===== 摘要 =====
\clearpage
\pagenumbering{Roman}
\begin{abstract}
摘要内容。
\end{abstract}

% ===== 目录与索引 =====
\clearpage
\tableofcontents
\clearpage
\pagenumbering{arabic}
\setcounter{page}{1}
% \listoffigures   % 如需
% \listoftables    % 如需

% ===== 正文 =====
\section{引言}
正文内容，引用示例\cite{key2023}。

\subsection{研究背景}
\subsubsection{细分标题}

% ===== 参考文献 =====
\printbibliography

\end{document}
```

编译命令：

```bash
xelatex main.tex && biber main && xelatex main.tex && xelatex main.tex
# 或
latexmk -xelatex main.tex
```

## GB/T 7714—2025 文献条目示例（refs.bib）

```bibtex
% 期刊论文 [J]
@article{key2023,
  author  = {张三 and 李四},
  title   = {基于深度学习的图像识别方法},
  journal = {计算机学报},
  year    = {2023},
  volume  = {46},
  number  = {3},
  pages   = {512--525},
}

% 图书 [M]
@book{book2022,
  author    = {王五},
  title     = {机器学习导论},
  publisher = {清华大学出版社},
  year      = {2022},
  address   = {北京},
}

% 学位论文 [D]
@phdthesis{thesis2021,
  author = {赵六},
  title  = {面向XXX的研究},
  school = {某某大学},
  year   = {2021},
}

% 会议论文 [C]
@inproceedings{conf2023,
  author    = {Smith, J. and Doe, A.},
  title     = {A Novel Approach to XXX},
  booktitle = {Proc. of ICML},
  year      = {2023},
  pages     = {100--108},
}

% 网络资源 [EB/OL]
@online{web2024,
  author = {某机构},
  title  = {某某报告},
  year   = {2024},
  url    = {https://example.com/report},
  urldate = {2024-06-01},
}

% 数据集 [DS/OL]
@dataset{dataset2025,
  author  = {某研究团队},
  title   = {某研究数据集},
  year    = {2025},
  url     = {https://doi.org/10.0000/example},
  urldate = {2025-08-01},
}

% 预印本 [PP/OL]
@online{preprint2025,
  author  = {Smith, J.},
  title   = {A Preprint Study},
  year    = {2025},
  eprint  = {2501.00001},
  eprinttype = {arxiv},
  url     = {https://arxiv.org/abs/2501.00001},
  urldate = {2025-08-01},
}
```

## 文献类型标识对照

| 类型 | 标识 | biblatex 字段 |
|------|------|---------------|
| 期刊论文 | [J] | @article |
| 图书 | [M] | @book |
| 学位论文 | [D] | @phdthesis / @mastersthesis |
| 会议论文 | [C] | @inproceedings |
| 专著章节 | [M] | @incollection |
| 标准 | [S] | @misc + note |
| 专利 | [P] | @misc + note |
| 电子资源 | [EB/OL] | @online |
| 报告 | [R] | @techreport |
| 数据集 | [DS] / [DS/OL] | @dataset |
| 预印本 | [PP] / [PP/OL] | @online + eprint |

## 常见原稿问题修正对照

| 原稿问题 | 修正方式 |
|----------|----------|
| `\begin{thebibliography}` 手动编号 | 转 .bib，用 `\printbibliography` |
| 正文引用写成 `[1]` 而非 `\cite` | 替换为 `\cite{key}`，key 按文献顺序命名 |
| 文献条目顺序与正文引用顺序不一致 | bibtex/biber 自动按引用顺序排序，无需手动调整 |
| 标题用 `\textbf{\Large 一、引言}` | 改为 `\section{引言}` |
| 图无 `\caption` | 补 `\caption{图名}\label{fig:xxx}` |
| 公式无编号 | 重要公式用 `\begin{equation}` 含编号 |
| 中文未设字体 | 加 `\usepackage{ctex}` 或 `\usepackage{xeCJK}` |
| `\usepackage{CJK}` 旧式中文 | 改用 ctex / xeCJK |
