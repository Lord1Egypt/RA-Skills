# 反模式手册

## 常见错误 + 正确做法

### ❌ 反模式 1: 直接用 Write/Edit 工具更新 .md 文件

**错误代码**：
```python
# AI 直接调用 Write 工具写 SKILL.md
Write(file_path="SKILL.md", content="...")
```

**后果**：UTF-8 中文编码损坏，文件变成乱码。

**正确做法**：
```python
# 使用 safe_write.py 原子写入
python scripts/safe_write.py write SKILL.md "<content>"
```

或使用 Python 直接调用 `safe_write()` 函数。

---

### ❌ 反模式 2: 宏包重复引入

**错误代码**（生成的 .tex）：
```latex
\usepackage{xcolor}
\usepackage{graphicx}
\usepackage{xcolor}  % 重复！
```

**后果**：编译警告，可能冲突。

**正确做法**：
`compose.py` 的 `collect_packages()` 使用 `seen` 集合去重。

---

### ❌ 反模式 3: 宏包顺序错误

**错误代码**：
```latex
\usepackage{fontspec}
\usepackage{ctex}  % 错误！ctex 应在 fontspec 之前（如果使用 xelatex）
```

**正确做法**：
`compose.py` 的 `PACKAGE_ORDER` 列表定义了正确顺序，依赖此列表排序。

---

### ❌ 反模式 4: 忘记配对 \begin 和 \end

**错误代码**：
```latex
\begin{mylist}
  \item 项目1
  \item 项目2
% 缺少 \end{mylist}！
```

**后果**：编译错误 `Missing \end\{mylist\}`。

**正确做法**：
`validate.py` 会检测 `\begin` 和 `\end` 数量不匹配，并给出警告。

---

### ❌ 反模式 5: 路径使用反斜杠（Windows）

**错误代码**：
```latex
\includegraphics[width=0.5\textwidth]{D:\Users\username\OneDrive\Desktop\xxx.png}
```

**后果**：LaTeX 将 `\U` `\O` 等解释为命令，编译失败。

**正确做法**：
使用正斜杠：
```latex
\includegraphics[width=0.5\textwidth]{D:/Users/username/OneDrive/Desktop/xxx.png}
```

---

### ❌ 反模式 6: 中英文之间无空格

**错误代码**：
```latex
这是English和中文混排。
```

**后果**：排版不美观，可能触发 `R-20` 规则报警。

**正确做法**：
```latex
这是 English 和中文混排。
```

---

### ❌ 反模式 7: 使用 \usepackage[UTF8]{inputenc}（已过时）

**错误代码**：
```latex
\usepackage[UTF8]{inputenc}  % pdflatex 专用
```

**后果**：lualatex 下可能报错或无效。

**正确做法**：
```latex
% lualatex 直接使用
\documentclass[UTF8]{ctexart}  % ctex 自动处理编码
```

---

### ❌ 反模式 8: 忘记加载宏包就使用命令

**错误代码**：
```latex
\timu{标题文本}  % 需要 \newcommand{\timu} 定义
```

**后果**：`Undefined control sequence` 错误。

**正确做法**：
确保 `scripts/components/commands/title-commands.txt` 组件已被 `\input` 引入。

---

### ❌ 反模式 9: 表格列格式用错了 p{} 宽度

**错误代码**：
```latex
\begin{tabularx}{\linewidth}{|>{\raggedright\arraybackslash}p{2cm}|>{\raggedright\arraybackslash}X|}
```

**后果**：`p{}` 和 `tabularx` 的 `X` 列可能冲突。

**正确做法**：
```latex
\begin{tabularx}{\linewidth}{|>{\raggedright\arraybackslash}p{2cm}|>{\raggedright\arraybackslash}X|}
% 确保加载了 tabularx 宏包
\usepackage{tabularx}
```

---

### ❌ 反模式 10: 编译验证时忘记检查 PDF 是否生成

**错误代码**（简化版 `validate.py`）：
```python
proc = subprocess.run([engine, tex_file], ...)
if proc.returncode == 0:
    print("Success")
```

**后果**：某些情况下 LaTeX 返回 0 但 PDF 未生成（如文件被占用）。

**正确做法**：
```python
pdf_path = Path(tex_path).with_suffix(".pdf")
if pdf_path.exists() and pdf_path.stat().st_size > 0:
    result["success"] = True
```

---

## 检查清单

生成 LaTeX 文档后，检查：

- [ ] 宏包无重复
- [ ] 宏包顺序正确（`ctex` → `fontspec` → `geometry` → ...）
- [ ] 所有自定义命令已定义（在 `commands/*.tex` 中）
- [ ] 所有自定义环境已定义（在 `environments/*.tex` 中）
- [ ] `\begin` 和 `\end` 配对
- [ ] 文件路径使用正斜杠
- [ ] 编码为 UTF-8（无 BOM）
- [ ] 编译生成了 PDF（文件大小 > 0）
- [ ] 无 `Undefined control sequence` 错误
- [ ] 无 `Missing $ inserted` 错误（数学公式用 `$...$` 包裹）

### ❌ 反模式 11: 假设 pdflatex 也能编译

**错误代码**：
```bash
python scripts/compose.py --manifest ... --engine pdflatex
```

**后果**：`fontspec` 和 `ctex` 对 pdflatex 支持有限，中文编译可能报错。

**正确做法**：始终使用 lualatex 或 xelatex。

---

### ❌ 反模式 12: 忽略首次编译的宏包安装过程

**错误做法**：第一次编译报错就以为是代码有问题。

**正确做法**：MiKTeX 首次编译会自动安装宏包，可能需要几十秒到几分钟。
如果超时，先手动安装：
```bash
mpm --install=fontspec,ctex,pgfplots,tikz,etoolbox,enumitem,booktabs,multirow,tabularx
```