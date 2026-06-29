# 常见问题解答 (FAQ)

## 排错

### Q1: 编译时报 `Undefined control sequence` 怎么解决？

**A**: 这是命令未定义错误。按以下步骤排查：

1. 检查命令是否拼写正确（区分大小写）
2. 检查是否遗漏 `\usepackage{宏包名}`
3. 检查自定义命令（如 `\timu`）所在组件是否已被 `\input` 引入
4. 运行 `python scripts/validate.py file.tex --fix` 尝试自动修复

---

### Q2: 中文显示乱码或编译报错 `Unicode character not set up` 怎么办？

**A**: 编码问题。确保：

1. 使用 **lualatex** 或 **xelatex** 引擎（不推荐 pdflatex）
2. 文档类使用 `ctexart` 并传入 `UTF8` 选项：
   ```latex
   \documentclass[12pt,a4paper,UTF8]{ctexart}
   ```
3. 确保 .tex 文件保存为 **UTF-8 无 BOM** 编码
4. 如果是特殊字符，使用 `\usepackage{newunicodechar}` 定义

---

### Q3: 编译超时（>120秒）是什么原因？

**A**: 可能原因：

1. **文档过大**（>100页）— 增加超时时间：`validate.py --timeout 300`
2. **死循环** — 检查是否有错误的宏定义或递归命令
3. **字体加载慢** — 系统字体缓存问题，尝试换用 `\setmainfont{SimSun}` 等系统自带字体
4. **图片过大** — 压缩图片或使用 `\includegraphics[width=...]{...}` 限制大小

---

### Q4: 如何调试「缺少 `$` inserted」错误？

**A**: 数学公式未正确包裹。排查：

1. 检查所有数学符号（`^`, `_`, `\alpha` 等）是否在 `$...$` 内
2. 检查是否有遗漏的 `$` 闭合
3. 使用 `\usepackage{mathtools}` 获得更好的错误提示
4. 将文档分段注释，定位出错位置

---

### Q5: `\begin{document}` 和 `\end{document}` 不匹配怎么办？

**A**: 环境不匹配。检查：

1. 所有自定义环境（如 `mylist`、`mycolumns`）是否在导言区用 `\newenvironment` 定义
2. 环境是否配对（`\begin{mylist}` ↔ `\end{mylist}`）
3. 运行 `python scripts/validate.py file.tex` 查看具体错误行号
4. 使用编辑器括号匹配功能检查

---

## 自定义规则

### Q6: 如何添加自己的 LaTeX 组件？

**A**: 使用 `component_manager.py`：

```bash
python scripts/component_manager.py add my_package.tex \
  --dir scripts/components/ \
  --category preamble \
  --name my-package \
  --desc "我的宏包配置"
```

或直接手动创建 `scripts/components/preamble/my_package.txt`，然后编辑 `manifest.json` 添加条目。

---

### Q7: 如何更新组件加载顺序？

**A**: 更新 `scripts/compose.py` 中的 `category_order` 列表：

```python
category_order = ["preamble", "environments", "commands", "styles", "tables", "graphics"]
```

LaTeX 要求：宏包 → 自定义命令 → 自定义环境 → 样式配置。

---

### Q8: 如何添加新的宏包到排序列表？

**A**: 更新 `scripts/compose.py` 中的 `PACKAGE_ORDER` 列表，在正确位置插入宏包名：

```python
PACKAGE_ORDER = [
    "ctex", "fontspec",
    "my-new-package",  # 在这里添加
    "geometry", ...
]
```

---

## CI 集成

### Q9: 如何在 CI/CD 中自动验证 LaTeX 文档？

**A**: 在 CI 配置中添加：

```yaml
# .github/workflows/latex.yml
name: LaTeX Build
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Install TeX Live
        run: sudo apt-get install -y texlive-lualatex
      - name: Build LaTeX
        run: |
          python scripts/extract.py input.tex --output-dir scripts/components/
          python scripts/compose.py --manifest scripts/components/manifest.json --output output.tex --validate
      - name: Upload PDF
        uses: actions/upload-artifact@v3
        with:
          name: output-pdf
          path: output.pdf
```

---

### Q10: 如何批量验证多个 .tex 文件？

**A**: 写一个简单的 bash 脚本：

```bash
#!/bin/bash
for f in *.tex; do
  echo "Validating $f ..."
  python scripts/validate.py "$f" --engine lualatex
  if [ $? -ne 0 ]; then
    echo "FAILED: $f"
    exit 1
  fi
done
echo "All files passed!"
```

---

## 其他

### Q11: 支持哪些 LaTeX 引擎？

**A**: 目前支持：

| 引擎 | 推荐度 | 说明 |
|------|--------|------|
| **lualatex** | ⭐⭐⭐⭐⭐ | 推荐，原生支持 UTF-8，字体支持好 |
| **xelatex** | ⭐⭐⭐⭐ | 也可用，但某些宏包兼容性略差 |
| **pdflatex** | ⭐⭐ | 不推荐，UTF-8 支持需额外配置 |

通过 `--engine` 参数切换：`python scripts/compose.py ... --engine xelatex`

---

### Q12: 生成的 PDF 字体不正确怎么办？

**A**: 检查：

1. 系统中是否安装了该字体（如 `SimSun`、`SimHei`）
2. 字体名是否拼写正确（区分大小写）
3. 使用 `\setmainfont{字体名}[BoldFont = ..., ItalicFont = ...]` 明确指定
4. 运行 `fc-list :lang=zh` 查看系统可用的中文字体

---

### Q13: 如何贡献新功能或报告 Bug？

**A**: 在 `workbuddy-skills` 仓库提交 Issue 或 Pull Request。

### Q14: 这个技能支持哪些 LaTeX 引擎？能切换吗？

**A**: 技能默认使用 **LuaLaTeX**，组件库基于 LuaLaTeX 语法。引擎策略如下：

| 引擎 | 状态 | 说明 |
|------|------|------|
| **LuaLaTeX** | ✅ 默认 | 组件库原生语法，推荐使用 |
| **XeLaTeX** | ✅ 一键切换 | `--engine xelatex`，组件库完全兼容（无 LuaLaTeX 独占功能） |
| **pdfLaTeX** | 🔧 动态转换 | inject 时自动将组件转为 pdfLaTeX 语法；convert 模式支持整篇转换 p→l |

LuaLaTeX ↔ XeLaTeX 互转无需额外配置，编译结果一致。
pdfLaTeX → LuaLaTeX 需要用 convert 模式。inject 模式会自动检测目标文档引擎。

如果尚未安装 LaTeX 环境：

| 发行版 | 下载 | 国内镜像 |
|--------|------|---------|
| **MiKTeX**（推荐，轻量） | https://miktex.org/download | 清华: https://mirrors.tuna.tsinghua.edu.cn/CTAN/systems/texlive/tlnet/<br>阿里: https://mirrors.aliyun.com/CTAN/systems/texlive/tlnet/ |
| **TeX Live**（完整版） | https://tug.org/texlive/ | 同上 |

切换方式：
```bash
python scripts/compose.py --manifest scripts/components/manifest.json --output output.tex --engine xelatex --validate
python scripts/template.py --type article --engine xelatex --output-mode pdf
```

不建议使用 pdflatex（不推荐，UTF-8 和字体支持需要额外配置）。

---

### Q15: 首次编译时宏包自动安装失败怎么办？

**A**: MiKTeX 默认会在首次编译时自动下载缺失的宏包。如果自动安装失败：

1. **检查网络**：确保电脑可以访问宏包镜像
2. **手动安装**：
   ```bash
   # 以管理员身份运行
   mpm --install=pgfplots
   mpm --install=ctex
   mpm --install=fontspec
   ```
3. **切换镜像源**（如果下载慢）：
   ```bash
   mpm --set-repository=https://mirrors.tuna.tsinghua.edu.cn/CTAN/systems/win32/miktex/tm/packages/
   ```
4. **检查字体**：SimSun（宋体）、SimHei（黑体）、KaiTi（楷体）、FangSong（仿宋）是 Windows 系统自带字体，其他平台可能需要安装中文字体包：
   - macOS: `brew install --cask font-noto-sans-cjk`
   - Linux: `apt install fonts-noto-cjk`
5. **首次编译较慢**：因为要生成字体缓存（luaotfload），后续编译会快很多。