# 组件规范 (Component Specification)

## 组件文件命名

- **格式**: `<component-name>.tex`
- **规则**:
  - 小写字母 + 连字符（`-`）分隔
  - 不包含空格、中文、特殊字符
  - 文件名与组件键（`manifest.json` 中的 `key`）对应

**示例**:

| 组件键 | 文件名 |
|---------|--------|
| `preamble/class-settings` | `scripts/components/preamble/class-settings.txt` |
| `environments/mylist` | `scripts/components/environments/mylist.txt` |
| `commands/title-commands` | `scripts/components/commands/title-commands.txt` |
| `styles/section-style` | `scripts/components/styles/section-style.txt` |
| `tables/table-style` | `scripts/components/tables/table-style.txt` |
| `graphics/figure-insert` | `scripts/components/graphics/figure-insert.txt` |

---

## 组件文件内容规范

### 1. 导言区组件（`preamble/*.tex`）

**要求**:
- 只包含一个功能模块的 LaTeX 代码
- 不使用 `\begin{document}` 或 `\end{document}`
- 宏包引入使用 `\usepackage[<options>]{<package>}` 格式
- 多个宏包可以合并到一个文件（如 `scripts/components/preamble/packages.txt`）

**示例** (`scripts/components/preamble/class-settings.txt`):

```latex
% --- 文档类配置 ---
\documentclass[12pt,a4paper,oneside,UTF8,fontset=none,titlepage]{ctexart}
\linespread{1.5}
```

**示例** (`scripts/components/preamble/packages.txt`):

```latex
% --- 颜色支持 ---
\usepackage{xcolor}

% --- 作图支持 ---
\usepackage{pgfplots,tikz,siunitx,fontspec,pgfplotstable}
\usetikzlibrary{matrix, positioning}
\pgfplotsset{
    myplot/.style={
        width=0.8\textwidth,
        tick label style={font=\small},
        label style={font=\small},
        legend style={font=\footnotesize},
        every axis plot/.append style={line width=1pt}
    }
}

% --- 字体系统 ---
\usepackage{fontspec}
\setmainfont{Times New Roman}
\setCJKmainfont{SimSun}[
  BoldFont = SimHei,
  ItalicFont = KaiTi,
  AutoFakeBold = 3,
  AutoFakeSlant = 0.2
]
\ctexset{fontset=none}
```

---

### 2. 自定义环境组件（`environments/*.tex`）

**要求**:
- 使用 `\newenvironment` 或 `\NewDocumentEnvironment` 定义
- 环境名使用小写字母 + 连字符（`-`）分隔
- 明确环境参数（如果有）

**示例** (`scripts/components/environments/mylist.txt`):

```latex
% --- 列表系统 ---
\usepackage{enumitem,newunicodechar}

% 定义层级基准缩进
\newlength{\titleindent}
\setlength{\titleindent}{2em}

% 智能列表环境定义
\NewDocumentEnvironment{mylist}{}{%
  \ifnum\value{listlevel}>2
    \begin{enumerate}[label=\alph*、, % 使用Unicode中文顿号
                     leftmargin=\dimexpr\titleindent*(\value{listlevel}+ 2-\value{listlevel})\relax,
                     labelindent=0pt,
                     labelwidth=1.5em,
                     labelsep*=0.5em,
                     align=left]
  \else
    \begin{enumerate}[label=(\arabic*),
                     leftmargin=\dimexpr\titleindent*(\value{listlevel} + 2-\value{listlevel})\relax,
                     labelindent=0pt,
                     labelwidth=1.5em,
                     labelsep*=0.5em,
                     align=left]
  \fi
}{%
  \end{enumerate}
}

% 层级跟踪系统（保持不变）
\newcounter{listlevel}
\pretocmd{\section}{\setcounter{listlevel}{0}}{}{}
\pretocmd{\subsection}{\setcounter{listlevel}{1}}{}{}
\pretocmd{\subsubsection}{\setcounter{listlevel}{2}}{}{}
\pretocmd{\paragraph}{\setcounter{listlevel}{3}}{}{}
\pretocmd{\subparagraph}{\setcounter{listlevel}{4}}{}{}
```

---

### 3. 自定义命令组件（`commands/*.tex`）

**要求**:
- 使用 `\newcommand` 或 `\NewDocumentCommand` 定义
- 命令名使用小写字母 + 连字符（`-`）分隔（如果有多单词）
- 明确命令参数（如果有）

**示例** (`scripts/components/commands/title-commands.txt`):

```latex
% --- 字体指令 ---
\usepackage{ctex,amssymb}

\newCJKfontfamily\timucn{SimSun}[AutoFakeBold=3] % 启用伪粗体
\newCJKfontfamily\yijitimucn{SimHei}
\newCJKfontfamily\erjitimucn{KaiTi}
\newCJKfontfamily\sanjitimucn{FangSong}
\newCJKfontfamily\zzcn{FangSong}
\newCJKfontfamily\dwcn{FangSong}
\newCJKfontfamily\zdcn{FangSong}[
  AutoFakeSlant = 0.2,  % 倾斜角度（0.2≈11.3度）
  ItalicFeatures = {FakeSlant=0.2}  % 确保斜体命令继承此配置
]

\newcommand{\timu}[1]{{\timucn #1}}
\newcommand{\yijitimu}[1]{{\yijitimucn #1}}
\newcommand{\erjitimu}[1]{{\erjitimucn #1}}
\newcommand{\sanjitimu}[1]{{\sanjitimucn #1}}
\newcommand{\zz}[1]{{\zzcn #1}}
\newcommand{\dw}[1]{{\dwcn #1}}
\newcommand{\seeref}[1]{%
  % 确保段落开始，继承全局 \parindent=2em
  \par 
  % 符号与缩进对齐（通过负间距微调位置）
  \hspace*{1em}\raisebox{-0.2ex}{\fontspec{Segoe UI Symbol}▶}%
  % 符号与文字间距
  \hspace{0.5em}%
  % 正文样式
  {\zdcn\zihao{-4}\itshape #1}%
  % 防止后续段落继承格式
  \par\noindent\ignorespaces
}
```

---

### 4. 样式配置组件（`styles/*.tex`）

**要求**:
- 使用 `\usepackage` + 配置命令
- 或使用 `\ctexset`、`\tikzset` 等全局配置命令
- 明确样式参数（如颜色、字体、间距）

**示例** (`scripts/components/styles/section-style.txt`):

```latex
% --- 章节样式 ---
\usepackage{needspace}

\ctexset{
    section={  % 一级标题
        format = \zihao{-4}\raggedright\yijitimu,
        numbering = true,
        number = \chinese{section},
        name = {},
        aftername = {、},
        afterindent = true % 顶格不缩进
    },
    subsection={  % 二级标题
        format = {\zihao{-4}\raggedright\erjitimu},
        numbering = true,
        number = \chinese{subsection},
        name = {（},
        aftername = {）},
        afterindent = true
    },
    subsubsection={  % 三级标题
        format = {\zihao{-4}\raggedright\sanjitimu},
        numbering = true,
        number = \arabic{subsubsection},
        name = {},
        aftername = {、},
        indent = 2em, % 固定缩进2字符
        afterindent = true
    },
    paragraph={  % 四级标题
        format = \normalfont\dwcn,
        numbering = true,
        number = \arabic{paragraph},
        name = {（},
        aftername = {）},
        indent = 2em, % 固定缩进2字符
        afterindent = true,
        runin = false, 
    },
    subparagraph={  % 五级标题
        format = \normalfont\dwcn,
        numbering = true,
        number = \alph{subparagraph},
        name = {},
        aftername = {、},
        indent = 2em, % 固定缩进2字符
        afterindent = true,
        runin = false, 
    },    
}

% 配置正文缩进（匹配标题缩进）
\setlength{\parindent}{2em}
\setcounter{secnumdepth}{5}  % 允许编号到五级标题
```

---

### 5. 表格模板组件（`tables/*.tex`）

**要求**:
- 使用 `\usepackage{tabularx,booktabs,multirow,float,subcaption,makecell,longtable,array}`
- 提供表格样式配置（如 `\newlength{\tablegap}`）
- 可以包含示例表格代码（注释掉）

**示例** (`scripts/components/tables/table-style.txt`):

```latex
% --- 表格系统 ---
\usepackage{varwidth, tabularx,booktabs,multirow,float,subcaption,makecell,longtable,array}

\newlength{\tablegap}
\setlength{\tablegap}{10em}
```

---

### 6. 图片模板组件（`graphics/*.tex`）

**要求**:
- 使用 `\usepackage{graphicx,eso-pic,float}`
- 提供图片插入命令（如 `\newcommand{\coverbackground}[1]{...}`）
- 明确图片路径格式（推荐使用正斜杠 `/`）

**示例** (`scripts/components/graphics/figure-insert.txt`):

```latex
% --- 图形支持 ---
\usepackage{graphicx}
\usepackage{eso-pic}
\usepackage{float}

% --- 背景命令 ---
\newcommand{\coverbackground}[1]{
  \AddToShipoutPicture*{
    \AtPageLowerLeft{
      \includegraphics[width=\paperwidth,height=\paperheight]{#1}
    }
  }
}
```

---

## manifest.json 格式规范

```json
{
  "version": "1.0.0",
  "generated_at": "2026-05-27T19:06:17",
  "components": {
    "preamble/class-settings": {
      "file": scripts/components/preamble/class-settings.txt",
      "desc": "文档类声明",
      "dependencies": []
    },
    "preamble/packages": {
      "file": scripts/components/preamble/packages.txt",
      "desc": "宏包引入",
      "dependencies": []
    },
    "preamble/colors": {
      "file": "preamble/colors.tex",
      "desc": "颜色定义",
      "dependencies": ["xcolor"]
    "preamble/fonts": {
      "file": "preamble/fonts.tex",
      "desc": "字体配置",
      "dependencies": ["fontspec", "ctex"]
    },
    "environments/mylist": {
      "file": scripts/components/environments/mylist.txt",
      "desc": "自定义列表环境",
      "dependencies": ["enumitem", "newunicodechar"]
    },
    "commands/title-commands": {
      "file": scripts/components/commands/title-commands.txt",
      "desc": "标题命令",
      "dependencies": ["ctex", "amssymb"]
    },
    "styles/section-style": {
      "file": scripts/components/styles/section-style.txt",
      "desc": "章节样式（ctexset）",
      "dependencies": ["ctex"]
    },
    "styles/toc-style": {
      "file": scripts/components/styles/toc-style.txt",
      "desc": "目录样式",
      "dependencies": ["tocloft"]
    },
    "styles/header-footer": {
      "file": scripts/components/styles/header-footer.txt",
      "desc": "页眉页脚",
      "dependencies": ["fancyhdr", "lastpage"]
    },
    "tables/table-style": {
      "file": scripts/components/tables/table-style.txt",
      "desc": "表格样式",
      "dependencies": ["tabularx", "booktabs", "multirow", "float", "subcaption", "makecell", "longtable", "array"]
    },
    "graphics/figure-insert": {
      "file": scripts/components/graphics/figure-insert.txt",
      "desc": "图片插入",
      "dependencies": ["graphicx"]
    },
    "graphics/background": {
      "file": scripts/components/commands/background.txt",
      "desc": "背景图片",
      "dependencies": ["eso-pic"]
    }
  },
  "body_file": "body.tex"
}
```

---

## 组件依赖声明

组件文件中如果使用其他宏包，必须在 `manifest.json` 的 `dependencies` 字段声明。

**示例**:

如果 `scripts/components/commands/title-commands.txt` 中使用了 `\newcommand` 和 `\newCJKfontfamily`，则需要声明：

```json
"commands/title-commands": {
  "file": scripts/components/commands/title-commands.txt",
  "desc": "标题命令",
  "dependencies": ["ctex", "amssymb"]
}
```

`compose.py` 会根据 `dependencies` 自动排序宏包引入顺序。

---

## 禁止事项

1. **禁止在组件文件中使用 `\begin{document}` 或 `\end{document}`** — 这些属于主文档，不在组件中
2. **禁止在组件文件中使用 `\input{}` 或 `\include{}` 引入其他组件文件** — 主文档负责引入所有组件
3. **禁止在组件文件中使用中文注释（如果宏包不支持 UTF-8）** — 使用英文注释或确保宏包支持 UTF-8
4. **禁止在组件文件名中使用空格、中文、特殊字符** — 只允许小写字母 + 连字符（`-`）
5. **禁止在组件文件中使用绝对路径** — 使用相对路径或让用户在主文档中配置
