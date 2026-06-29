# latex-modular 架构说明

## 模块划分

```
latex-modular/
├── SKILL.md                     # 技能入口（≤230行）
├── scripts/                     # Python 脚本
│   ├── safe_write.py           # 原子写入工具（tmp + os.replace）
│   ├── extract.py              # 从 LaTeX 源文件提取组件
│   ├── compose.py              # 模块组合引擎
│   ├── validate.py             # 编译验证器
│   ├── refactor.py            # 重构引擎
│   ├── component_manager.py    # 组件库管理
│   └── update_frontmatter.py  # 更新 SKILL.md frontmatter
├── scripts/components/                 # 组件库（auto-generated）
│   ├── manifest.json          # 组件索引
│   ├── preamble/              # 导言区组件
│   ├── environments/          # 自定义环境
│   ├── commands/              # 自定义命令
│   ├── styles/               # 样式配置
│   ├── tables/               # 表格模板
│   └── graphics/             # 图片模板
└── references/                # 渐进式加载参考文档
    ├── guide.md                # 完整使用指南
    ├── architecture.md         # 本文件
    ├── antipatterns.md         # 反模式手册
    ├── faq.md                 # 常见问题
    ├── changelog.md          # 版本更新记录
    └── component-spec.md     # 组件规范
```

## 核心模块说明

### 1. safe_write.py（原子写入工具）

**功能**：所有文件写入操作必须通过此模块，确保 UTF-8 中文编码不损坏。

**核心函数**：
- `safe_write(filepath, content, encoding="utf-8")` — 原子写入
- `safe_patch_by_line(filepath, line_num, new_line)` — 按行号精确替换
- `safe_patch_regex(filepath, pattern, replacement)` — 正则替换
- `safe_insert_after(filepath, after_pattern, insert_text)` — 在匹配行后插入

**写入流程**：
```
tmp_fd = tempfile.mkstemp()
with os.fdopen(fd, "w", encoding="utf-8") as f:
    f.write(content)
os.replace(tmp_path, target_path)
```

### 2. extract.py（组件提取器）

**功能**：从已有 LaTeX 源文件提取组件到模块化库。

**提取规则**（`CLASSIFY_RULES`）：
按正则模式匹配，将导言区内容分类到不同组件文件。

**输出**：
- `scripts/components/manifest.json` — 组件索引（JSON）
- `scripts/components/<category>/<name>.txt` — 各组件文件

### 3. compose.py（组合引擎）

**功能**：按依赖顺序组合组件，生成完整可编译的 .tex 文件。

**组合顺序**（硬编码在 `compose.py`）：
1. 文档类声明（`\documentclass`）
2. 宏包引入（自动去重 + 按 `PACKAGE_ORDER` 排序）
3. 颜色定义（`xcolor`）
4. 字体配置（`fontspec`、`ctex`）
5. 页面配置（`geometry`）
6. 作图支持（`pgfplots`、`tikz`）
7. 自定义环境（`\NewDocumentEnvironment`）
8. 自定义命令（`\newcommand`）
10. 章节样式（`\ctexset`）
11. 目录样式（`tocloft`）
12. 页眉页脚（`fancyhdr`）
13. 正文内容（`\begin{document}` ... `\end{document}`）

**宏包排序**（`PACKAGE_ORDER`）：
字体相关（`ctex`、`fontspec`）→ 版式相关（`geometry`、`fancyhdr`）→ 颜色/图形（`xcolor`、`graphicx`）→ 作图（`pgfplots`、`tikz`）→ 列表/分栏（`enumitem`、`multicol`）→ 表格（`tabularx`、`booktabs`）→ 其他（`pifont`、`etoolbox`）

### 4. validate.py（编译验证器）

**功能**：使用系统 `lualatex` 编译 .tex 文件，解析错误并给出修复建议。

**验证流程**：
1. 查找引擎路径（`find_engine()`）
2. 执行编译（`compile_tex()`，超时 120 秒）
3. 解析错误和警告（`parse_errors_and_warnings()`）
4. 尝试自动修复（`attempt_auto_fix()`，可选）
5. 打印报告（`print_report()`）

**错误解析规则**（`ERROR_PATTERNS`、`WARNING_PATTERNS`）：
使用正则匹配编译输出，提取错误描述、上下文、行号。

**自动修复规则**（`attempt_auto_fix()`）：
- 未定义颜色 → 添加 `\usepackage{xcolor}`
- 未定义命令（如 `\mathbb`）→ 添加 `\usepackage{amssymb}`
- 环境未定义（如 `figure`、`table`）→ 添加 `\usepackage{float}`

### 5. refactor.py（重构引擎）

**功能**：将原始 LaTeX 代码重构进模块化体系，保留原文语义。

**重构流程**：
1. 读取源文件（`read_source()`）
2. 分割文档为导言区和正文区（`split_document()`）
3. 分类导言区内容到模块（`classify_preamble()`）
4. 保存模块到 `scripts/components/`（`save_components()`）
5. 生成模块化主文档（`generate_modular_document()`，使用 `\input{}` 引入组件）
6. 编译验证（`validate_refactored()`，调用 `validate.py`）

**模块分类规则**（`MODULE_RULES`）：
与 `extract.py` 的 `CLASSIFY_RULES` 类似，但增加了依赖宏包字段。

### 6. component_manager.py（组件库管理）

**功能**：管理组件库的增删改查，维护 `manifest.json`。

**子命令**：
- `list` — 列出所有组件（按 category 分组）
- `add` — 添加组件（自动提取依赖宏包）
- `remove` — 删除组件（删除文件 + 更新 manifest）
- `show` — 显示组件内容
- `validate` — 验证所有组件（检查 `{}` 配对、环境标签、编码）

## 数据流

### extract 模式

```
source.tex → extract.py → scripts/components/*.txt + manifest.json
```

### compose 模式

```
manifest.json + body.tex → compose.py → output.tex → lualatex → output.pdf
```

### refactor 模式

```
source.tex → refactor.py → scripts/components/*.txt + manifest.json + output_modular.tex
```

## 依赖查找顺序

### Python 解释器

```
<managed_python>  (优先)
<system_python>  (后备)
```

### LaTeX 引擎

```
/c/Program Files/MiKTeX/miktex/bin/x64/lualatex  (已安装)
/usr/bin/lualatex
系统 PATH 中查找
```

## 编码规范

- 所有 `.md` 文件：UTF-8（必须用 `safe_write.py` 写入，禁止直接用 Write/Edit 工具）
- 所有 `.tex` 文件：UTF-8（LaTeX 侧用 `\usepackage[UTF8]{ctex}` 或 `fontspec`）
- 所有 `.py` 文件：UTF-8（Python 侧用 `encoding="utf-8"` 打开文件）
