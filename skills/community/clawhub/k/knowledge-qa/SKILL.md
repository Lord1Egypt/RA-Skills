---
name: knowledge-qa
description: 本地知识库问答技能。当用户需要基于个人知识库文档（PDF/Markdown/Word）进行问答、生成报告、制作思维导图、或上传文件到向量库时触发。触发词包括："基于知识库"、"基于mysql查询"、"基于某个分区"、"查一下知识库"、"帮我写报告"、"生成思维导图"、"根据文档"、"从我的资料"、"结合我的笔记"、"整理成报告"、"做个导图"、"上传知识库"、"有新文件"、"索引文档"、"建向量库"、"有哪些分区"、"分区列表"、"创建知识库"、"初始化知识库"、"知识库列表"。
---

# 知识库问答技能 (knowledge-qa)

## 概述

本技能支持**多知识库**架构，每个知识库对应一个独立的 DashVector Collection。用户可在同一工作目录下创建多个互不干扰的知识库（如"MySQLNotes"、"JavaNotes"等）。

**核心特性：**
- 多知识库支持（一个知识库 = 一个 DashVector Collection）
- 语义向量检索（基于阿里云 DashVector + 百炼 Embedding）
- 自动分区（raw_docs 子目录自动映射为分区）
- 多分区并行查询 + 结果合并
- 报告 + 思维导图双输出
- **需要 Python 环境**（用户需安装 Python 3.8+）

---

## 前置要求

### 1. 安装 Python 环境

用户需在系统上安装 Python 3.8 或更高版本，以及以下依赖：

```bash
pip install pdfplumber python-docx requests
```

### 2. 安装 WorkBuddy 并打开工作目录

用户用 WorkBuddy 打开一个工作目录，在该目录下管理所有知识库。

---

## 多知识库架构

```
工作空间 (WorkBuddy 打开的目录)
│
├── MySQLNotes/              ← 知识库 A → Collection: MySQLNotes
│   ├── raw_docs/
│   │   ├── mysql/           ← 分区: mysql
│   │   └── default/
│   ├── config.json          ← 独立配置（不同的 DashVector Collection）
│   ├── indexed_files.json
│   └── README.md
│
├── JavaNotes/               ← 知识库 B → Collection: JavaNotes
│   ├── raw_docs/
│   │   ├── java基础/        ← 分区: java_
│   │   └── default/
│   ├── config.json
│   └── README.md
│
└── scripts/                 ← （由技能提供，用户不可见）
    ├── init_knowledge_base.py
    ├── upload_to_vector.py
    ├── query_knowledge_base.py
    └── partition_list.py
```

**映射关系：**
- 1 个知识库文件夹 = 1 个 DashVector Collection（独立配置）
- Collection 内按 raw_docs 子目录分区（mysql / oracle / java_ 等）
- 切换知识库：由用户在提问时指定，如"基于 MySQLNotes 知识库回答..."

---

## 工作流程一：创建新知识库

**触发词：** "创建知识库"、"初始化一个知识库"、"新建知识库"

### 步骤 1：确认知识库名称和工作目录

用户告诉 AI 要创建的知识库名称，以及是否在当前工作目录下创建。

### 步骤 2：运行初始化脚本

```bash
python <技能路径>/scripts/init_knowledge_base.py <知识库名称> --path <工作目录>
```

AI 自动执行脚本，在工作目录下创建以下结构：

```
知识库名称/
├── raw_docs/
│   └── default/
├── config.json       ← 模板文件，用户需填写阿里云凭证
├── indexed_files.json
└── README.md
```

### 步骤 3：提示用户填写配置

告知用户打开 `config.json`，填入：
- `dashvector.api_key`
- `dashvector.endpoint`
- `dashvector.collection_name`（建议与知识库名一致）
- `bailian.api_key`

凭证获取地址：
- DashVector: https://dashvector.console.aliyun.com/api-key
- 百炼: https://bailian.console.aliyun.com/api-key

---

## 工作流程二：上传文件到向量库

**触发词：** "上传知识库"、"有新文件了"、"帮我索引文件"

### 步骤 1：确认目标知识库

用户必须指定知识库名称（如"MySQLNotes"）。AI 在工作目录下查找对应的知识库文件夹。

### 步骤 2：运行上传脚本

```bash
python <技能路径>/scripts/upload_to_vector.py --kb-path <知识库路径>
```

脚本自动：
1. 扫描 `raw_docs/` 下所有文件
2. 识别新增或变更的文件（对比 `indexed_files.json`）
3. 提取文本内容并分块
4. 调用百炼 API 生成向量
5. 调用 DashVector API 上传（自动创建分区）
6. 更新 `indexed_files.json`

### 分区识别规则

| 文件位置 | 分区名 |
|---------|--------|
| `raw_docs/文档.pdf` | `default` |
| `raw_docs/mysql/文档.pdf` | `mysql` |
| `raw_docs/MySQL实战/文档.pdf` | `mysql_`（小写、非字母数字转下划线）|

---

## 工作流程三：知识问答与报告生成

**触发词：** "基于知识库回答"、"查一下知识库"、"帮我写报告"

### 步骤 1：确认目标知识库和分区

用户必须指定知识库名称（如"基于 MySQLNotes 知识库"）。
可选指定分区（如"基于 MySQLNotes 的 mysql 和 oracle 分区"）。

### 步骤 2：运行查询脚本

```bash
python <技能路径>/scripts/query_knowledge_base.py "<问题>" --kb-path "<知识库路径>" --partition <分区名>
```

示例（单分区）：
```bash
python scripts/query_knowledge_base.py "InnoDB 有哪些特性" --kb-path "MySQLNotes" --partition mysql
```

示例（多分区）：
```bash
python scripts/query_knowledge_base.py "MySQL 和 Oracle 有什么区别" --kb-path "MySQLNotes" --partition mysql,oracle
```

示例（全分区）：
```bash
python scripts/query_knowledge_base.py "介绍一下这个知识库" --kb-path "MySQLNotes"
```

**多分区查询说明：** DashVector 查询 API 的 `partition` 参数只接受字符串（不支持数组），脚本通过**串行多次查询**实现多分区，每个分区独立查询后合并结果，按相似度排序。

### 步骤 3：读取原始文档补充上下文

根据检索结果中的 `source` 字段，用 `read_file` / `pdf` / `docx` 加载相关章节。

### 步骤 4：网络搜索补充（如需要）

使用 `Web Search` 搜索实时信息或知识库未覆盖的背景知识。

### 步骤 5：生成 Markdown 报告

报告格式规范：

```markdown
# [报告标题]

> 生成时间：[YYYY-MM-DD HH:mm]
> 知识库：[知识库名称]
> 来源：[x] 篇相关文档 + 网络补充

## 摘要
[简要概述]

## 一、[章节标题]
[内容...]

## 参考来源
- [文件名] - 分区: [分区名]
```

**报告保存路径：** `<工作目录>/<知识库名称>/reports/report_[时间戳]_[主题].md`

### 步骤 6：生成思维导图

使用 `visualizer:interactive` 工具生成交互式思维导图：
- 提取标题层级（# / ## / ###）
- 每个节点不超过 20 字
- 最多 3 级展示

**导图保存路径：** `<工作目录>/<知识库名称>/mindmaps/mindmap_[时间戳]_[主题].html`

### 步骤 7：输出结果

1. 对话中展示 Markdown 报告
2. `visualizer:interactive` 展示思维导图
3. 告知用户文件保存路径

---

## 工作流程四：查看分区状态

**触发词：** "有哪些分区"、"分区列表"、"查看分区"

```bash
python <技能路径>/scripts/partition_list.py --kb-path <知识库路径>
```

---

## 文档格式支持

| 格式 | 读取方式 |
|------|--------|
| `.md` | 直接 `read_file` |
| `.pdf` | `pdf` skill |
| `.docx` / `.doc` | `docx` skill |

---

## 脚本汇总

| 脚本 | 用途 | 关键参数 |
|------|------|--------|
| `init_knowledge_base.py` | 创建新知识库 | `<名称> --path <工作目录>` |
| `upload_to_vector.py` | 上传/索引文件 | `--kb-path <知识库路径>` |
| `query_knowledge_base.py` | 多分区查询 | `<问题> --kb-path --partition` |
| `partition_list.py` | 查看分区状态 | `--kb-path` |

所有脚本均支持 **自动发现知识库**：不传 `--kb-path` 时，自动在当前目录或父目录中查找第一个包含 `raw_docs/` + `config.json` 的文件夹。

---

## 注意事项

1. **Python 环境**：用户需先安装 Python 3.8+ 和依赖包（pdfplumber, python-docx, requests）
2. **首次使用**：提醒用户先创建知识库并填写 `config.json`
3. **知识库为空**：告知用户先往 `raw_docs` 目录放入文档
4. **上传失败**：提示检查 API Key、Endpoint、Collection 名称是否正确
5. **分区路由**：上传时 `partition` 必须放在请求体顶层
6. **分区查询**：DashVector `partition` 参数只接受字符串，多分区通过串行查询实现
7. **多知识库切换**：由用户指定知识库名称，AI 负责在工作目录下查找
