# LaTeX Verbatim 居中技能

> **技能编号**: latex-verbatim-center  
> **适用版本**: TeX Live 2024+  
> **文员专用**: 是  
> **最后更新**: 2026-04-03

## 技能概述

本技能解决 LaTeX 中 `verbatim` 环境无法正确居中的问题。通过使用 `varwidth` 包，可以实现代码块、ASCII 图表等内容的完美居中。

## 问题背景

在 LaTeX 文档排版中，当尝试将 `verbatim` 环境放在 `center` 环境中时，内容往往不会真正居中，而是保持左对齐。这是因为 `verbatim` 环境会忽略外部的格式化指令。

**典型症状**：
- 第 3 页的 ASCII 图表偏左
- 代码块没有居中显示
- 使用 `center` 环境包裹 `verbatim` 无效

## 解决方案

使用 `varwidth` 包包裹 `verbatim` 环境，再用 `center` 环境实现真正居中。

### 核心代码
```latex
\usepackage{varwidth}

\let\originalverbatim\verbatim
\let\endoriginalverbatim\endverbatim

\renewenvironment{verbatim}{%
  \par
  \begin{center}
  \begin{varwidth}{\linewidth}
  \originalverbatim
  \footnotesize
}{%
  \endoriginalverbatim
  \end{varwidth}
  \end{center}
  \par
}
```

## 文件结构

```
latex-verbatim-center/
├── SKILL.md              # 完整技能文档
├── QUICKREF.md           # 快速参考卡片
├── config-example.tex    # 配置示例
├── test-template.tex     # 测试模板
└── README.md             # 本文件
```

## 使用步骤

### 1. 安装依赖
```bash
# 检查是否已安装 varwidth
tlmgr list | grep varwidth

# 如未安装，执行
tlmgr install varwidth
```

### 2. 添加配置
将 `config-example.tex` 中的代码添加到文档 preamble 中。

### 3. 测试验证
使用 `test-template.tex` 测试配置是否正确。

### 4. 编译文档
```bash
xelatex document.tex
xelatex document.tex  # 需要编译两次
```

## 成功案例

**项目**: PIM-SSMoE 研究报告排版  
**问题**: 第 3 页 ASCII 图表偏左，第 7、8、10 页表格表头不对齐  
**解决**: 使用本技能方案  
**版本**: fixed42.pdf  
**日期**: 2026-04-03

## 技术细节

### 为什么使用 varwidth？
- `minipage` 会强制指定宽度，导致居中计算错误
- `varwidth` 根据内容自动调整宽度（最大不超过 `\linewidth`）
- 配合 `center` 环境实现真正居中

### 为什么需要编译两次？
LaTeX 需要第一次编译收集宽度信息，第二次编译才能正确应用居中设置。

## 常见问题

### Q: 与 fancyvrb 包冲突吗？
A: 是的，建议二选一。如果已使用 fancyvrb，请使用其内置的居中选项。

### Q: 可以只居中特定的 verbatim 吗？
A: 可以，不要重定义环境，而是创建新环境：
```latex
\newenvironment{centerverbatim}{%
  \begin{center}
  \begin{varwidth}{\linewidth}
  \verbatim
}{%
  \endverbatim
  \end{varwidth}
  \end{center}
}
```

### Q: 影响性能吗？
A: 轻微影响，但现代计算机上可忽略不计。

## 参考资料
- TeX Stack Exchange: "How to center verbatim"
- CTAN: varwidth package documentation
- LaTeX.org Forum: "center a text in verbatim"

## 维护者
- 创建日期：2026-04-03
- 创建者：AI Assistant
- 适用人员：文档排版文员

## 版本历史
- v1.0 (2026-04-03): 初始版本，基于 fixed42.pdf 成功经验
