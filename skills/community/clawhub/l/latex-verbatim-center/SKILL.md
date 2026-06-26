# LaTeX Verbatim 居中技能

## 技能说明
**技能名称**：latex-verbatim-center  
**适用场景**：当 LaTeX 文档中的 verbatim 环境（代码块、ASCII 图表等）无法正确居中时使用  
**技能标签**：#LaTeX #排版 #居中 #verbatim #varwidth

## 问题描述
在 LaTeX 中，当尝试将 `verbatim` 环境放在 `center` 环境中时，内容往往不会真正居中，而是偏左对齐。这是因为 `verbatim` 环境会忽略外部的 `\centering` 指令。

**典型症状**：
- 第 3 页的 ASCII 图表偏左
- 代码块没有居中显示
- 使用 `center` 环境包裹 `verbatim` 无效

## 解决方案

### 核心方法
使用 `varwidth` 包包裹 `verbatim` 环境，再用 `center` 环境实现真正居中。

### 实现步骤

#### 1. 添加宏包
在文档 preamble 中添加：
```latex
\usepackage{varwidth}
```

#### 2. 重新定义 verbatim 环境
```latex
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

#### 3. 完整示例
```latex
\documentclass{article}
\usepackage{fontspec}
\usepackage{xeCJK}
\usepackage{varwidth}  % 关键宏包

\setCJKmainfont{WenQuanYi Zen Hei}

% 重新定义 verbatim
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

\begin{document}
这里是正常文本。

\begin{verbatim}
def main():
    print("Hello World")
\end{verbatim}

这里也是正常文本。
\end{document}
```

## 技术原理
- `varwidth` 环境会根据内容自动调整宽度（最大不超过 `\linewidth`）
- `center` 环境会将 `varwidth` 盒子居中
- 组合使用实现真正的居中效果

## 替代方案对比

| 方法 | 效果 | 推荐度 |
|------|------|--------|
| `center` + `varwidth` | ✅ 完美居中 | ⭐⭐⭐⭐⭐ |
| `center` + `minipage` | ❌ 仍然偏左 | ⭐⭐ |
| `xleftmargin=0.5\linewidth` | ❌ 会偏右 | ⭐ |
| `lrbox` + `center` | ⚠️ 有时有效 | ⭐⭐⭐ |

## 注意事项
1. 必须使用 `varwidth` 包，标准 `minipage` 无效
2. 需要编译两次才能看到最终效果
3. 如果文档中有多个 verbatim，只需重定义一次
4. 与 `fancyvrb` 包可能冲突，建议二选一

## 文员专用说明
**适用人员**：文档排版文员、技术文档编辑  
**使用频率**：当发现文档中代码块或 ASCII 图表未居中时使用  
**操作步骤**：
1. 检查文档是否已加载 `varwidth` 包
2. 检查是否已重定义 `verbatim` 环境
3. 如未配置，按上述步骤添加
4. 编译两次 PDF 查看效果

## 相关文件
- 技能位置：`~/.openclaw/extensions/openclaw-latex-skills/skills/latex-verbatim-center/SKILL.md`
- 示例文档：`/home/raolin/.openclaw/workspace-editor/PIM-SSMoE_Research_Report.tex`
- 最终版本：`fixed42.pdf`（使用此方案的第一个成功版本）

## 版本历史
- **v1.0** (2026-04-03): 初始版本，基于 fixed42.pdf 成功经验
- 问题解决者：AI Assistant
- 问题报告者：用户

## 参考资料
- TeX Stack Exchange: "How to center verbatim" (2013)
- LaTeX.org Forum: "center a text in verbatim" (2009)
- CTAN: varwidth package documentation
- TeX Live 2024 验证通过
