---
name: knowledge
description: |
  结构化知识归档、索引、检索与反思补全。将周报、笔记、知识文档自动拆解为标准化主题目录结构，维护全量索引，支持快速检索与信息缺失追问。TRIGGER: 归档/存储/记录/保存周报笔记文档, 追加更新知识, 索引生成刷新更新, 结构化检索读取查询, 反思补充补全缺失信息, 结构化记忆, 结构化存储, 结构化总结, knowledge archive index retrieve reflect structured memory structured storage structured summary.
metadata:
  {
    "openclaw":
      {
        "emoji": "🧠",
        "tags": ["knowledge", "archive", "index", "search", "reflect"],
        "category": "productivity",
      },
  }
---

# Knowledge 结构化归档

将非结构化文档拆解为标准化主题目录结构，维护索引，支持检索与反思补问。

## 配置

配置文件存放在 **skill 目录**下：`./.knowledge-config.json`（相对于本 SKILL.md 所在目录）

首次调用时检查该配置文件：

- 不存在 → 向用户询问源文件夹路径和结构化存储路径，验证后创建配置文件并建 `source_path/done/` 子目录。
- 已存在 → 读取配置继续执行。

```json
{
  "source_path": "源文件夹路径",
  "storage_path": "结构化存储路径",
  "created_at": "创建时间"
}
```

路径约定：
- `source_path`: 待处理的 .txt / .md 文件
- `storage_path`: 结构化输出根目录
- `source_path/done/`: 处理完成的源文件移动目标

> **注意**：配置文件与归档数据分离存储，配置文件始终位于 skill 目录下，不受 storage_path 变更影响。

## 核心流程

### 1. 写入归档

**输入来源（按优先级）：**
1. 用户直接粘贴文本
2. 用户提供的文件或文件夹路径
3. 自动遍历 `source_path` 下未处理文件（跳过 `done/`），多个文件时列出清单供选择

**写入流程：**
1. 读取并分析文档内容
2. 归纳 2-8 字主题名称，检查是否合并已有主题
3. 创建/打开主题文件夹，确保 `resource/` 存在
4. 依次写入：description.md → process.md → meta.md → code.md，复制资源文件
5. 将源文件移动到 `source_path/done/`
6. 触发索引生成，全量刷新 `index.json`
7. 触发反思补问
8. 汇报结果

文件写入规则详见 [references/file-rules.md](references/file-rules.md)。

### 2. 索引生成

**触发时机：** 写入完成后自动触发，或用户主动要求。

读取所有主题子文件夹的 `description.md`，生成 `{storage_path}/index.json`：

```json
[
  {
    "boxName": "{主题名}",
    "description": "50-150字概要",
    "keyWord": ["关键词1", "关键词2", "关键词3", "关键词4"]
  }
]
```

每次全量覆盖，不做增量更新。

### 3. 检索

**触发时机：** 用户需要查询已有知识沉淀。

1. 读取 `index.json`，对比 keyWord 和 description，筛选最相关的前 1-2 个主题
2. 阅读候选主题的 `description.md` 确认匹配度
3. 根据需求读取对应文件：完整上下文→process.md，事实→meta.md，代码→code.md

### 4. 反思补问

**触发时机：** 每次写入完成后自动触发。

1. 回顾本次写入内容，识别信息盲区（人物、时间、原因、关联系统、决策背景等）
2. 最多提出 **3 个**问题，附带原文片段
3. 用户回答后回写对应文件

**主动反思：** 用户主动选择主题进行深度反思，生成结构化问卷，不限问题数量。

反思流程详见 [references/reflection.md](references/reflection.md)。

## 目录结构

````
./                              # skill 目录
└── .knowledge-config.json      # 配置文件（固定位置）

{storage_path}/
├── index.json            # 全量索引
├── {主题}/
│   ├── description.md    # 概述
│   ├── process.md        # 完整记录
│   ├── meta.md           # 独立事实
│   ├── code.md           # 代码片段
│   └── resource/         # 引用文件副本
````

## 约束

- 不丢失信息，宁可多记不遗漏
- 代码完整保留，不截断不省略
- 元信息必须明确、可验证的事实
- 追加模式保留所有已有内容
- 输出语言跟随源文档语言