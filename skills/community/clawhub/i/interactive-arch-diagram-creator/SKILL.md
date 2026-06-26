---
name: arch-diagram
description: >
  生成代码仓架构可视化图，输出为独立静态 HTML 网页。
  仅支持在代码仓根目录下运行，自动扫描当前目录。
  Claude 扫描代码文件、理解架构、生成层次思维导图和各模块子流程图，
  最终输出可在浏览器直接打开的 HTML 文件。
---

# 代码仓架构可视化 Skill

## 概述

将任意本地代码仓转换为一份交互式架构可视化 HTML 页面，流程分三个阶段：

1. **Stage 1 — 文件摘要**：扫描代码文件，批量生成每个文件的一句话摘要（可利用缓存加速）
2. **Stage 2 — 主架构图**：根据摘要生成 PlantUML mindmap 格式的层次架构图
3. **Stage 3 — 子流程图**：对每个架构节点逐一生成 Mermaid flowchart 子图
4. **生成 HTML**：调用脚本将所有数据填充到 HTML 模板，输出静态网页

---

## Skill 资源路径

本 skill 所在目录（以下用 `$SKILL_DIR` 指代）包含：

- `scripts/scan_repo.py` — 扫描代码文件
- `scripts/parse_mindmap.py` — 解析 mindmap，提取节点列表
- `scripts/build_html.py` — 构建最终 HTML
- `assets/arch_diagram_static.html` — HTML 模板
- `references/prompts.md` — 所有 prompt 模板（**使用前必须读取**）

---

## 第一步：理解用户意图

用户要求生成当前代码仓的架构图，直接在当前目录下运行。

确认以下信息后再开始：
- 当前目录即为代码仓根目录
- 输出目录（默认 `./output`，可让用户指定）
- 是否跳过缓存（有已有 `cache/code_map_dict_<name>.json` 时默认复用）

---

## 第二步：读取 Prompt 模板

在开始处理之前，先读取 `references/prompts.md`，里面包含 Stage 1/2/3 所需的完整 prompt 模板。

---

## 第三步：Stage 1 — 文件摘要

### 3.1 检查缓存

运行扫描脚本，优先使用缓存：

```bash
python $SKILL_DIR/scripts/scan_repo.py \
  . \
  --cache <cache_dir>/code_map_dict_<repo_name>.json \
  --stats-output /tmp/<repo_name>_meta.json
```

- `--stats-output` 会将文件数、LOC、技术栈等元信息写入 JSON，供最终 HTML 标题栏使用。
- 如果输出的 `"source"` 是 `"cache"`，直接使用缓存的 `summary` 字典，跳到 Stage 2（`--stats-output` 仍会被写入）。
- 如果是 `"scan"`，需要生成摘要。

### 3.2 批量生成摘要

将扫描结果的 `files` 数组分批处理：

- **每批最多 30 个文件**，或预估总内容不超过 60k tokens
- 对每批，按 `references/prompts.md` 中的「Stage 1」prompt 模板，构造请求：
  - 将文件列表格式化为 `=== 文件: path ===\n<内容>` 的形式
  - 让 Claude（自己）生成一个 JSON 对象 `{"文件路径": "摘要"}`
- 合并所有批次的摘要，得到完整的 `code_summary` 字典

> **注意**：摘要要体现业务语义，不超过30字。如果某个文件内容过长（>5000字），只取前3000字生成摘要。

### 3.3 保存缓存

将 `code_summary` 字典保存到 `<cache_dir>/code_map_dict_<repo_name>.json`，供下次使用。

`<cache_dir>` 默认是当前工作目录下的 `cache/`，如用户有指定则使用用户指定的路径。

---

## 第四步：Stage 2 — 生成主架构图

使用 `references/prompts.md` 中的「Stage 2」prompt 模板。

### 规模判断

粗略估算 `code_summary` 的总字符数（乘以 0.7 估算 token 数）：

- **< 76,800 tokens**（128k × 60%）：使用「直接模式」prompt，一次生成完整 mindmap
- **>= 76,800 tokens**：使用「分块模式」，先对每块生成子架构，再合并

分块大小：每块约 76,800 tokens，按文件顺序依次分组。

### 输出

得到 PlantUML mindmap 字符串，格式如下：
```
@startmindmap
* {"name": "项目名"}
** {"name": "层级名", "files": ["path/to/file"]}
*** {"name": "模块名", "files": ["path/to/file"]}
@endmindmap
```

将 mindmap 字符串保存到临时文件：`/tmp/<repo_name>_mindmap.txt`

---

## 第五步：Stage 3 — 生成节点子流程图

### 5.1 解析节点

```bash
python $SKILL_DIR/scripts/parse_mindmap.py /tmp/<repo_name>_mindmap.txt
```

得到节点列表：`[{"name": "节点名", "key": "唯一key", "files": ["..."]}]`

### 5.2 逐节点生成 Mermaid 子图

对每个节点，串行处理：
1. 从 `code_summary` 中提取该节点 `files` 对应的摘要，格式化为 `文件路径: 摘要` 的形式
2. 用 `references/prompts.md` 中「Stage 3」prompt 模板生成 Mermaid flowchart
3. 提取 ` ```mermaid ... ``` ` 代码块中的内容，存入 `flowchart_data[node_key]`

> 如果某节点生成失败或返回内容不符合 Mermaid 语法，跳过该节点，继续处理下一个，不中断整体流程。

### 5.3 保存结果

将 `flowchart_data` 字典保存为 `/tmp/<repo_name>_flowchart.json`

---

## 第五点五步：提取 edges 数据

Stage 2 的输出包含两个代码块：`plantuml` mindmap 和 `json` edges。
从 Stage 2 的输出中提取 ` ```json ... ``` ` 代码块的内容，
得到节点间关系数组，格式为 `[{"from": "节点名A", "to": "节点名B", "label": "调用"}, ...]`。

将其保存为 `/tmp/<repo_name>_edges.json`。

**注意**：对提取出的 edges 做以下过滤后再保存：
1. 过滤掉 from/to 同层或反向（下层→上层）的无效边
2. 过滤掉 from 是 to 的直接父节点的边（父子关系已由 mindmap 层级结构表达，无需重复）
3. 对同一 from→to 对存在多条边时，只保留第一条（禁止平行重复边）

---

## 第六步：生成 HTML

```bash
python $SKILL_DIR/scripts/build_html.py \
  --repo-name "<repo_name>" \
  --mindmap /tmp/<repo_name>_mindmap.txt \
  --flowchart /tmp/<repo_name>_flowchart.json \
  --edges /tmp/<repo_name>_edges.json \
  --meta /tmp/<repo_name>_meta.json \
  --template $SKILL_DIR/assets/arch_diagram_static.html \
  --output <output_dir>
```

> **可选**：如果用户提供了代码仓简介，追加 `--description "一句话介绍该仓库的用途"` 参数，
> 它将显示在 HTML 标题栏的仓库名下方。

脚本输出 `SUCCESS: /path/to/output/<repo_name>.html`

---

### 标题栏说明

生成的 HTML 顶部会展示一个深色标题栏，包含：
- **仓库名称**（来自 `--repo-name`）
- **仓库简介**（来自 `--description`，可选）
- **文件数统计**（来自 `scan_repo.py` 扫描结果）
- **总代码行数 LOC**（来自 `scan_repo.py` 扫描结果）
- **技术栈分布**（按文件数降序排列的语言 pill，最多 8 种）

---

## 第七步：完成

告诉用户：
- HTML 文件的完整路径
- 如何在浏览器打开（`open <path>` 或直接拖入浏览器）
- 页面功能说明：
  - 左侧层级侧边栏点击可切换层级，右侧卡片点击可查看该模块的子流程图
  - 节点上方短横线表示有入边（被上层调用），下方短横线表示有出边（调用下层）
  - 鼠标悬停节点可显示与该节点相连的调用关系边及标签，其他节点同时变暗

---

---

## 常见问题处理

**没有找到代码文件**：告知用户当前支持的文件类型（.py .js .ts .java .go .rs 等），并建议检查是否在代码仓根目录运行。

**Stage 2 返回空内容**：重试一次，提示摘要过多可能影响质量，建议缩小仓库范围。

**Mermaid 渲染失败**：这是浏览器侧的问题，HTML 文件本身是正确的，建议用现代浏览器（Chrome/Edge）打开。
