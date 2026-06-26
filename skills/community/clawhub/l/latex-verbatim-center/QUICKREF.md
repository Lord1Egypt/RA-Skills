# LaTeX Verbatim 居中 - 快速参考卡

## 问题现象
- [ ] 代码块/图表偏左
- [ ] center 环境无效
- [ ] 数学公式正常但 verbatim 不居中

## 一键解决

### 步骤 1: 添加宏包
```latex
\usepackage{varwidth}
```

### 步骤 2: 重定义 verbatim
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

### 步骤 3: 编译两次
```bash
xelatex document.tex
xelatex document.tex
```

## 验证清单
- [ ] 代码块居中
- [ ] ASCII 图表居中
- [ ] 数学公式正常
- [ ] 表格对齐正常

## 常见错误
- ❌ 忘记添加 `varwidth` 包
- ❌ 只编译一次（需编译两次）
- ❌ 使用 `minipage` 而非 `varwidth`
- ❌ 设置 `xleftmargin=0.5\linewidth`（会导致偏右）

## 文员专用命令
```bash
# 检查是否已安装 varwidth
tlmgr list | grep varwidth

# 如未安装，执行
tlmgr install varwidth
```

## 成功案例
- 文件：`PIM-SSMoE_Research_Report.tex`
- 版本：`fixed42.pdf`
- 日期：2026-04-03

## 联系支持
如问题未解决，提供：
1. LaTeX 错误日志
2. 当前使用的宏包列表
3. verbatim 环境前后代码
