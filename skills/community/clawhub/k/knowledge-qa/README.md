# 知识库问答技能 - 用户安装手册

> 适用对象：有 Word/PPT/PDF/Markdown 课件或笔记，希望基于自有文档进行 AI 问答的教师。

---

## 一、技能简介

本技能让你的 AI 助手能够：

1. **向量化存储**：将本地文档（PDF/MD/DOCX）上传到阿里云 DashVector 向量数据库
2. **语义问答**：基于文档内容回答问题，像聊天一样检索知识
3. **分区管理**：按主题分类管理（如 MySQL / Oracle / Java 分区隔离）
4. **多知识库**：在同一个工作目录下管理多个独立知识库
5. **报告生成**：将问答结果整理为 Markdown 报告 + 思维导图

---

## 二、系统要求

| 项目 | 要求 |
|------|------|
| Python | 3.8 或更高版本 |
| 依赖包 | `pdfplumber`, `python-docx`, `requests` |
| 阿里云账号 | DashVector + 百炼（Embedding）免费额度可用 |

### 安装 Python 依赖

```bash
pip install pdfplumber python-docx requests
```

---

## 三、阿里云凭证申请（免费）

### 3.1 DashVector（向量数据库）

1. 访问：https://dashvector.console.aliyun.com
2. 登录阿里云账号（可用支付宝账号）
3. 进入「API-KEY」页面，创建一个 API Key
4. 进入「集合」页面，创建一个 Collection：
   - 名称：任意（如 `my-knowledge-base`）
   - 向量维度：**1024**
   - 距离类型：Cosine（余弦相似度）
5. 复制 **Collection 访问地址**（格式如 `https://vrs-cn-xxxx.dashvector.cn-hangzhou.aliyuncs.com`）

### 3.2 百炼（向量生成）

1. 访问：https://bailian.console.aliyun.com
2. 登录后进入「API-KEY」页面
3. 创建一个 API Key

> **免费额度**：DashVector 新用户有免费额度，百炼 Embedding 也有免费调用次数，日常个人使用足够。

---

## 四、安装步骤

### 4.1 安装技能（复制文件夹）

将本技能包（`knowledge-qa-skill/`）完整复制到 WorkBuddy 的技能目录：

```
~/.workbuddy/skills/knowledge-qa/
```

> 如果你不清楚 WorkBuddy 的技能目录位置，请询问你的 AI 助手。

### 4.2 创建第一个知识库

假设你的工作目录下有课件文件，现在开始创建知识库：

**通过 AI 助手执行：**

```
请帮我创建一个名为 MyNotes 的知识库
```

AI 会运行初始化脚本，自动创建目录结构：

```
MyNotes/
├── raw_docs/
│   └── default/        ← 在这里放你的文档
├── config.json          ← 下一步要填写
├── indexed_files.json
└── README.md
```

### 4.3 填写配置

打开 `MyNotes/config.json`，将以下字段替换为你的阿里云凭证：

```json
{
  "knowledge_base": {
    "name": "MyNotes",
    "root_path": "MyNotes/raw_docs",
    "indexed_files_path": "MyNotes/indexed_files.json"
  },
  "dashvector": {
    "api_key": "在这里填入你的 DashVector API Key",
    "endpoint": "在这里填入 Collection 访问地址",
    "collection_name": "my-knowledge-base",
    "dimension": 1024,
    "model": "text-embedding-v3"
  },
  "bailian": {
    "api_key": "在这里填入你的百炼 API Key",
    "model": "text-embedding-v3"
  }
}
```

### 4.4 放入文档

将你的课件/笔记放到 `raw_docs/` 目录下：

```
MyNotes/raw_docs/
├── default/              ← 默认分区，直接放根目录
│   ├── 课程介绍.md
│   └── 第一章笔记.pdf
├── mysql/                ← MySQL 专题分区（创建子文件夹=创建分区）
│   └── InnoDB特性.pdf
└── oracle/
    └── 备份恢复.docx
```

---

## 五、使用流程

### 5.1 上传文档到向量库

告诉 AI：

```
帮我把 MyNotes 知识库的文件上传索引
```

AI 自动：
- 扫描 `raw_docs/` 下所有文件
- 提取文本内容
- 生成向量并上传到 DashVector
- 完成后告知结果

### 5.2 提问

告诉 AI：

```
基于 MyNotes 知识库回答：InnoDB 有哪些特性？
```

AI 自动：
- 在向量库中检索相关内容
- 结合原始文档给出回答
- 在对话中展示答案

### 5.3 生成报告

如果回答满意，告诉 AI：

```
把这个回答整理成报告并生成思维导图
```

AI 自动：
- 生成 Markdown 格式报告
- 生成交互式思维导图
- 保存到 `MyNotes/reports/` 和 `MyNotes/mindmaps/`

---

## 六、分区使用指南

### 什么是分区？

分区用于**按主题隔离检索范围**。例如：
- `raw_docs/mysql/` 下的文件 → 属于 `mysql` 分区
- `raw_docs/oracle/` 下的文件 → 属于 `oracle` 分区
- 直接放在 `raw_docs/` 根目录 → 属于 `default` 分区

### 查询指定分区

```
基于 MyNotes 知识库的 mysql 分区回答：主键索引和唯一索引有什么区别？
```

### 查询多个分区

```
基于 MyNotes 知识库的 mysql 和 oracle 分区回答：两者的索引机制有何不同？
```

### 查询全部分区

```
基于 MyNotes 知识库回答：这个知识库涵盖了哪些内容？
```

---

## 七、常见问题

### Q: 上传失败怎么办？
检查 `config.json` 中的 API Key、Endpoint、Collection 名称是否正确。

### Q: 文档格式支持哪些？
支持 `.md`、`.pdf`、`.docx`、`.doc`。

### Q: 可以管理多个知识库吗？
可以！在同一个工作目录下创建多个知识库文件夹（如 `MyNotes`、`JavaNotes`），每个有独立的配置和向量库。

### Q: 如何删除分区中的数据？
删除 `raw_docs/` 下对应子目录中的文件，然后重新运行上传脚本（会自动清理旧记录）。

---

## 八、文件结构一览

```
knowledge-qa-skill/              ← 技能包（复制到此目录）
├── SKILL.md                     ← 技能定义（AI 使用）
├── README.md                    ← 本手册（用户阅读）
├── config.template.json          ← 配置模板
└── scripts/
    ├── init_knowledge_base.py   ← 创建知识库
    ├── upload_to_vector.py      ← 上传/索引文件
    ├── query_knowledge_base.py  ← 语义问答
    └── partition_list.py        ← 查看分区状态

工作目录/
└── MyNotes/                    ← 用户创建的知识库
    ├── raw_docs/                ← 放文档
    ├── config.json              ← 填凭证
    ├── indexed_files.json       ← 自动维护
    └── README.md                ← 自动生成
```
