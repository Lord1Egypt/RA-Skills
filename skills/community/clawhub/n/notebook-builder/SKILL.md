---
name: notebook-builder
description: 分段式 Jupyter Notebook 生成与修改工具。当用户需要创建、分段追加、修改、合并 Jupyter Notebook (.ipynb) 时使用此技能。支持的高级功能包括：(1) 分段多次生成 Notebook 内容，避免一次性生成过大导致超时或内容截断；(2) 本地图片 base64 嵌入到 Markdown cell；(3) 内置哈希判题系统（不显示明文答案）；(4) 灵活的 cell 级增删改查；(5) 合并多个 notebook 为一个；(6) 导出为纯 Python 脚本；(7) 自动生成目录；(8) Cell 标签分组与重排序。适用场景包括教学课件、编程练习、技术教程、学习笔记等 notebook 的创建与维护。
license: MIT License, complete terms in LICENSE.txt
---

# Notebook Builder

分段式创建和修改 Jupyter Notebook，支持图片嵌入与判题系统。

## ⚠️ 执行规则（必须遵守）

**所有 Python 代码必须由 agent 自己通过 terminal 工具执行，严禁让用户手动在命令行执行。**

原因：agent 通过工具执行命令时，stdout/stderr 会被自动捕获并返回，agent 可以依据输出判断操作是否成功。如果让用户手动执行，agent 无法感知执行结果，会导致工作流中断或状态不一致。

具体要求：
1. 每一段 Python 代码都必须通过 `terminal` 工具直接执行，不要输出代码让用户自己运行
2. 执行后必须检查 stdout 输出，确认操作成功（如看到 `✅` 前缀的确认信息）
3. 分段生成时，每段执行完毕后应通过 `terminal` 工具执行 `nb_info()` 或 `get_cell_summary()` 检查当前 notebook 状态，再继续下一段
4. 如遇执行错误，agent 应自行分析错误信息并修正代码后重试，无需用户介入

## 核心工作流程

```
用户请求
  │
  ├─ 创建新 notebook      → "创建流程"
  ├─ 修改现有 notebook    → "修改流程"
  ├─ 添加判题系统         → "判题流程"
  └─ 嵌入图片             → "图片流程"
```

## ❗ 关于 `<技能脚本目录>` 占位符

示例代码中的 `<技能脚本目录>` 需要替换为此技能实际的 `scripts/` 目录绝对路径。agent 应通过以下方式确定该路径：
1. 此 SKILL.md 文件所在目录的同级 `scripts/` 子目录
2. 即 SKILL.md 的父目录 + `/scripts`

例如如果此 SKILL.md 位于 `/home/user/.codebuddy/skills/notebook-builder/SKILL.md`，则 `<技能脚本目录>` 应替换为 `/home/user/.codebuddy/skills/notebook-builder/scripts`。

## 辅助脚本

此技能包含核心辅助脚本 `scripts/nb_helpers.py`，提供以下能力：

| 函数 | 作用 |
|------|------|
| `new_notebook()` | 创建空 notebook 字典 |
| `load_notebook(path)` | 从文件加载 notebook |
| `save_notebook(nb, path)` | 保存 notebook 到文件 |
| `make_markdown_cell(src)` | 构造 Markdown cell |
| `make_code_cell(src)` | 构造 Code cell |
| `append_cells(nb, cells)` | 向末尾追加 cell |
| `insert_cells(nb, idx, cells)` | 在指定位置插入 cell |
| `delete_cells(nb, start, count)` | 删除 cell |
| `replace_cell(nb, idx, cell)` | 替换 cell |
| `find_cells_by_keyword(nb, kw)` | 按关键词搜索 cell |
| `find_cells_by_id(nb, id)` | 按 id 查找 cell |
| `embed_image_in_markdown(path)` | 图片转 base64 嵌入 |
| `make_image_output(path)` | 为 code cell 创建图片输出 |
| `make_quiz_code_cell(...)` | 生成哈希判题 cell |
| `make_quiz_summary_cell(ids, total, scores)` | 生成判题汇总 cell |
| `merge_notebooks(paths, output)` | 合并多个 notebook |
| `export_to_script(nb, path)` | 导出为 Python 脚本 |
| `make_toc_cell(nb, max_level)` | 自动生成目录 cell |
| `reorder_cells(nb, new_order)` | 按索引重排 cell |
| `tag_cell(cell, tags)` | 为 cell 添加标签 |
| `find_cells_by_tag(nb, tag)` | 按标签查找 cell |
| `make_section(title, ...)` | 快速生成章节 |
| `clear_all_outputs(nb)` | 清除所有输出 |
| `set_kernel(nb, name, display)` | 修改 kernel |
| `nb_info(nb)` | notebook 统计信息 |
| `get_cell_summary(nb)` | 每个 cell 的摘要 |

## 创建流程（分段生成）

分段生成的核心思路：**不要试图一次性生成整个 notebook**。将内容拆分为多个"段"，每段包含若干 cell，逐段追加。

### 步骤

1. **初始化**：用 `new_notebook()` 创建空 notebook，根据用户需求设置 kernel
2. **规划章节**：将内容大纲拆分为 3-5 段，每段对应一个逻辑章节
3. **逐段生成**：
   - 使用 `make_section()` 或 `make_markdown_cell()` + `make_code_cell()` 构造当前段的 cell
   - 使用 `append_cells()` 追加到 notebook
   - 调用 `save_notebook()` 保存当前进度（支持中途预览）
4. **收尾**：添加总结章节，最终保存

### 分段生成示例

> **重要**：以下每一段代码都应由 agent 通过 terminal 工具分段执行，不要一次性全部执行，也不要让用户手动执行。

**第 1 次执行**（通过 terminal 工具）：初始化 + 标题段
```python
import sys
sys.path.insert(0, "<技能脚本目录>")
from nb_helpers import *

nb = new_notebook(kernel_name="python3")
append_cells(nb, [
    make_markdown_cell("# 🔥 我的教程\n---\n**目标**：xxx"),
    make_code_cell("import torch\nprint(torch.__version__)"),
])
save_notebook(nb, "my_tutorial.ipynb")
print(nb_info(nb))  # 验证状态
```

**第 2 次执行**（通过 terminal 工具）：追加第一章
```python
import sys
sys.path.insert(0, "<技能脚本目录>")
from nb_helpers import *

nb = load_notebook("my_tutorial.ipynb")
append_cells(nb, make_section(
    "1.1 基础概念",
    "这里是 Markdown 正文...",
    ["# 实验代码\nprint('hello')"],
))
save_notebook(nb, "my_tutorial.ipynb")
print(nb_info(nb))  # 验证状态
```

**第 N 次执行**（通过 terminal 工具）：追加考核 + 总结
```python
import sys
sys.path.insert(0, "<技能脚本目录>")
from nb_helpers import *

nb = load_notebook("my_tutorial.ipynb")
quiz = make_quiz_code_cell("q1", "1+1=?", 2, score=10)
append_cells(nb, [make_divider_cell(), make_markdown_cell("## 📝 考核时间"), quiz])
save_notebook(nb, "my_tutorial.ipynb")
print(nb_info(nb))  # 验证状态
```

### 关键约束

- **所有代码必须由 agent 通过 terminal 工具执行**，不要输出代码让用户手动运行
- 每次追加的 cell 数量建议不超过 10 个，避免单次操作过大
- 每次追加后都 `save_notebook()`，确保进度不丢失
- 每次执行后检查 stdout 输出，确认看到 `✅` 成功信息
- 使用 `nb_info()` 和 `get_cell_summary()` 检查当前状态
- 分段执行时，每次都需要重新 `import` 和 `load_notebook()`，因为每次 terminal 调用是独立的 Python 进程

## 修改流程

### 步骤

1. **加载**：`load_notebook(path)` 加载现有 notebook
2. **定位**：
   - `get_cell_summary()` 查看所有 cell 概览
   - `find_cells_by_keyword()` 按关键词搜索目标 cell
   - `find_cells_by_id()` 按 id 精确定位
3. **修改**：
   - `replace_cell()` 替换整个 cell
   - `insert_cells()` 在指定位置插入新 cell
   - `delete_cells()` 删除不需要的 cell
4. **保存**：`save_notebook(nb, path)`

### 修改示例

> 以下代码由 agent 通过 terminal 工具执行：

```python
import sys
sys.path.insert(0, "<技能脚本目录>")
from nb_helpers import *

nb = load_notebook("existing.ipynb")

# 查看结构
for line in get_cell_summary(nb):
    print(line)

# 在第 5 个 cell 后插入新内容
insert_cells(nb, 5, [
    make_markdown_cell("### 补充说明\n新增的内容..."),
    make_code_cell("# 新的实验代码"),
])

# 替换第 3 个 cell
replace_cell(nb, 3, make_markdown_cell("## 更新后的标题"))

save_notebook(nb, "existing.ipynb")
print(nb_info(nb))  # 验证修改结果
```

## 图片流程

两种嵌入方式：

### 方式 1：嵌入到 Markdown cell（推荐）

```python
# 基础用法
img_md = embed_image_in_markdown("diagram.png", alt_text="架构图")
cell = make_markdown_cell(f"## 系统架构\n\n{img_md}\n\n上图展示了...")

# 指定宽度
img_md = embed_image_in_markdown("photo.jpg", alt_text="示例", width=500)
```

### 方式 2：嵌入到 Code cell 输出

```python
output = make_image_output("result.png")
cell = make_code_cell("# 运行结果如下", outputs=[output])
```

### 注意事项

- 图片会被 base64 编码嵌入，无需外部依赖
- 大图片会显著增大 .ipynb 文件体积，建议压缩后再嵌入
- 支持 PNG、JPG、GIF、SVG 格式

## 判题流程

判题系统通过 SHA256 哈希存储答案，学生无法看到明文。

### 生成判题 cell

```python
# 单选/填空题
quiz1 = make_quiz_code_cell(
    question_id="q1",
    question_prompt="torch.randn(3,4,5) 的 stride 是什么？",
    answer=(20, 5, 1),      # 正确答案（不会以明文出现在 notebook 中）
    answer_type="tuple",
    hints=["stride[i] = 后面所有维度 size 的乘积"],
    score=10,
)
```

### 支持的答案类型

| 类型 | 示例 | 说明 |
|------|------|------|
| `int` | `42` | 整数 |
| `float` | `3.14` | 浮点数 |
| `str` | `"hello"` | 字符串（不区分大小写，去首尾空格） |
| `bool` | `True` | 布尔值 |
| `tuple` | `(20, 5, 1)` | 元组 |
| `list` | `[1, 2, 3]` | 列表（会被转为 tuple 比较） |

### 汇总评分

```python
summary = make_quiz_summary_cell(
    question_ids=["q1", "q2", "q3"],
    total_score=30,
    scores={"q1": 10, "q2": 10, "q3": 10},  # 可选，未指定时平均分配
)
append_cells(nb, [summary])
```

### 判题原理

1. 答案经过标准化处理（去空格/小写/统一类型表示）
2. 加盐后 SHA256 哈希，截取前 16 位存储
3. 学生运行 cell 时，对其输入做同样处理并比对哈希
4. 哈希不可逆，学生无法从中推导答案

## 完整教程生成模板

当用户要求生成完整教学 notebook 时，推荐结构：

```
1. 标题 + 目标描述 (markdown)
2. 环境准备 (code: import + version check)
3. --- 分隔线 ---
4. 章节 1: 概念讲解 (markdown) + 实验代码 (code) × N
5. --- 分隔线 ---
6. 章节 2: ...
7. --- 分隔线 ---
8. 📝 考核时间 (markdown)
9. 题目 1 (quiz code cell)
10. 题目 2 (quiz code cell)
11. ...
12. 📊 汇总评分 (quiz summary code cell)
13. --- 分隔线 ---
14. 完成总结 (markdown)
```

## 常见问题

### Q: 为什么代码必须由 agent 自己执行？
A: agent 只能通过工具调用的返回值感知执行结果。如果让用户在终端手动执行，即使输出了结果，agent 也无法检测到，会导致状态不一致。因此所有 Python 代码都必须通过 terminal 工具执行。

### Q: 分段执行时变量会丢失吗？
A: 会。每次 terminal 工具调用是一个独立的 Python 进程，上次定义的变量不会保留。因此每次执行都需要重新 `import` 并用 `load_notebook()` 加载之前保存的 notebook。

### Q: 分段生成时如何避免内容重复？
A: 每次追加前用 `get_cell_summary()` 检查当前状态，确认上一段已正确追加后再继续。

### Q: 如何修改已有 notebook 中的某个 cell？
A: 用 `find_cells_by_keyword()` 定位目标 cell 的 index，然后用 `replace_cell()` 替换。

### Q: 判题 cell 能否防止学生查看哈希？
A: 哈希值虽然可见，但不可逆。学生无法从 16 位哈希推导出原始答案。如需更高安全性，可将判题逻辑放到外部服务。

### Q: 图片嵌入后文件太大怎么办？
A: 建议在嵌入前压缩图片（如 PNG → 降低分辨率、JPG → 降低质量），或只嵌入关键图片。

## 合并 Notebook

将多个 notebook 合并为一个，适合把分散的章节/讲义合并。

```python
# 合并多个 notebook
merged = merge_notebooks(
    paths=["chapter1.ipynb", "chapter2.ipynb", "chapter3.ipynb"],
    output_path="full_course.ipynb",
    add_dividers=True,   # 在每个 notebook 之间添加分隔线
    add_titles=False,    # 不添加来源标注
)
```

## 导出为 Python 脚本

将 notebook 的 Code cell 导出为 `.py` 文件，Markdown cell 可选地转为注释。

```python
nb = load_notebook("tutorial.ipynb")
export_to_script(
    nb,
    output_path="tutorial.py",
    include_markdown=True,  # Markdown cell 作为注释写入
)
```

## 自动生成目录

扫描 notebook 中所有 Markdown 标题，生成可点击跳转的目录 cell。

```python
nb = load_notebook("long_tutorial.ipynb")
toc = make_toc_cell(nb, max_level=3, title="📑 目录")
insert_cells(nb, 0, [toc])  # 插入到 notebook 开头
save_notebook(nb, "long_tutorial.ipynb")
```

## Cell 重排序

按指定索引顺序重排 cell，可用于调整结构。

```python
nb = load_notebook("messy.ipynb")
for line in get_cell_summary(nb):
    print(line)
# 按新顺序重排
reorder_cells(nb, [0, 3, 1, 2, 4])
save_notebook(nb, "messy.ipynb")
```

## Cell 标签系统

为 cell 打标签，然后按标签筛选。标签存储在 `metadata.tags` 中，JupyterLab 可直接识别。

```python
# 打标签
cell = make_code_cell("x = 1")
tag_cell(cell, ["exercise", "easy"])

# 按标签查找
exercises = find_cells_by_tag(nb, "exercise")
for idx, cell in exercises:
    print(f"Cell {idx}: {cell['cell_type']}")
```
