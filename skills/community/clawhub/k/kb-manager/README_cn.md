# kb-manager

一个轻量的 OpenClaw skill，用于在 agent 工作区中构建并维护结构化的本地知识库。

它可以帮助你：

- 初始化标准知识库结构
- 判断内容是否值得保存
- 按内容用途自动分类
- 以结构化 Markdown 形式保存知识
- 在分类不确定时，将内容安全放入 `00_inbox`
- 后续再整理 inbox 内容
- 长期保持命名、模板和元数据的一致性

这个版本刻意保持小而实用，便于直接上手，也方便后续扩展。

---

## 目录结构

```text
kb-manager/
  SKILL.md
  templates/
    default-entry.md
    project-entry.md
    research-entry.md
    reference-entry.md
  docs/
    classification-rules.md
    naming-rules.md
  examples/
    init.txt
    intake-article.txt
    intake-pdf.txt
    organize-inbox.txt
```

---

## 这个 skill 会做什么

`kb-manager` 适合放在一个专门负责知识管理的 `knowledge` agent 工作区中使用。

它的核心职责包括：

- 初始化 `knowledge/` 目录
- 创建标准子目录和核心 `_meta` 文件
- 判断输入内容是否值得保存
- 按内容用途进行分类
- 用 Markdown 模板格式化保存内容
- 在不确定时将内容放入 `knowledge/00_inbox/`
- 在用户要求时帮助整理 inbox
- 长期保持知识库结构清晰、内容一致

---

## 推荐使用方式

建议为知识管理单独创建一个 OpenClaw agent。

例如：

```bash
openclaw agents add knowledge
```

然后把这个 skill 放到该 agent 的工作区中：

```text
skills/
  kb-manager/
    SKILL.md
    templates/
    docs/
    examples/
```

---

## 标准知识库结构

初始化时，skill 应创建如下结构：

```text
knowledge/
  00_inbox/
  01_reference/
  02_learning/
  03_projects/
  04_research/
  05_playbooks/
  06_prompts/
  99_archive/
  _meta/
```

### 初始化时创建的核心元数据文件

```text
knowledge/_meta/README.md
knowledge/_meta/classification-rules.md
knowledge/_meta/naming-rules.md
knowledge/_meta/template.md
knowledge/_meta/intake-log.md
```

### 后续按需创建的可选元数据文件

```text
knowledge/_meta/topics.md
knowledge/_meta/projects-index.md
knowledge/_meta/recent.md
```

只有当知识库规模增长到确实有必要时，才建议创建这些可选索引文件。

---

## 安装方式

### 方式 A：安装现成 skill

如果 ClawHub 上已经有合适的知识库 skill，可以直接安装。

```bash
clawhub search "knowledge base"
clawhub install <skill-slug>
```

### 方式 B：手动加入当前 skill

把 `kb-manager/` 目录复制到 agent 工作区中：

```text
skills/kb-manager/
```

这是体验当前版本最直接的方式。

---

## 快速开始

### 1. 创建 knowledge agent

```bash
openclaw agents add knowledge
```

### 2. 添加 skill

把 `kb-manager` 文件夹放入该 agent 的 `skills/` 目录中。

### 3. 启动一个新的 knowledge 会话

确保新会话中已经加载了这个 skill。

### 4. 初始化知识库

可以直接使用 `examples/init.txt` 中的示例提示词，或者发送类似下面的内容：

```text
请使用 kb-manager 初始化一个知识库。

要求：
1. 在当前工作区中创建 `knowledge/` 目录
2. 创建标准子目录：
   - 00_inbox
   - 01_reference
   - 02_learning
   - 03_projects
   - 04_research
   - 05_playbooks
   - 06_prompts
   - 99_archive
   - _meta
3. 将 `docs/classification-rules.md` 复制到 `knowledge/_meta/classification-rules.md`
4. 将 `docs/naming-rules.md` 复制到 `knowledge/_meta/naming-rules.md`
5. 将 `templates/default-entry.md` 复制到 `knowledge/_meta/template.md` 作为当前激活模板
6. 创建 `knowledge/_meta/README.md` 和 `knowledge/_meta/intake-log.md`
7. 可选索引文件先不要创建，除非用户明确要求：
   - `knowledge/_meta/topics.md`
   - `knowledge/_meta/projects-index.md`
   - `knowledge/_meta/recent.md`
8. 项目相关内容优先使用 `templates/project-entry.md`
9. 分类不确定的内容先放入 `00_inbox`
10. 输出创建后的目录结构和初始化完成的 `_meta` 文件列表
```

---

## 常见使用示例

### 保存文章

可以使用 `examples/intake-article.txt`，或者发送：

```text
请把这篇文章保存到知识库中。

要求：
1. 先判断它是否值得保存
2. 自动完成分类
3. 选择最合适的模板
4. 如果分类不确定，放入 `00_inbox`
5. 输出保存路径、文件名和结构化 Markdown 内容
```

### 保存 PDF

可以使用 `examples/intake-pdf.txt`，或者发送：

```text
请把这个 PDF 整理成一个知识条目。

要求：
1. 如果它是官方文档，优先归入 `01_reference`
2. 如果它是教程或学习材料，优先归入 `02_learning`
3. 选择最合适的模板
4. 输出最终保存路径、文件名和结构化 Markdown 内容
```

### 整理 inbox

可以使用 `examples/organize-inbox.txt`，或者发送：

```text
请整理 `knowledge/00_inbox/`。

要求：
1. 对高置信度条目重新分类
2. 补充或优化标签
3. 对低价值内容给出归档或删除建议
4. 不确定的内容继续保留在 inbox
5. 输出一份简短的整理报告
```

---

## 模板说明

当前 skill 包含以下模板：

- `templates/default-entry.md`
- `templates/project-entry.md`
- `templates/research-entry.md`
- `templates/reference-entry.md`

### 默认条目模板

用于一般笔记、文章、学习材料、提示词和通用知识条目。

### 项目条目模板

用于项目相关讨论、计划、会议纪要、架构说明和决策记录。

### 研究条目模板

用于对比分析、评估、调研、探索性报告等内容。

### 参考条目模板

用于命令、规范、操作说明以及长期参考资料。
