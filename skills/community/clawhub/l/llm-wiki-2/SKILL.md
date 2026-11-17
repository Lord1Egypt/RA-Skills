# LLM Wiki

基于 Andrej Karpathy 的 LLM Wiki 模式，让 AI Agent 持续构建和维护结构化、交叉链接的 Markdown 知识库。

## 触发条件

当用户提到以下关键词时激活本 skill：
- "知识库"、"wiki"、"llm-wiki"、"知识管理"
- "ingest"、"摄入"、"整理资料"、"消化"
- "lint"、"检查知识库"、"查矛盾"
- 对已有 wiki 的查询请求

## 核心理念

> 与其每次查询时从原始文档重新检索（RAG），不如让 LLM **增量构建和维护一个持久化的 Wiki**——一个结构化、交叉链接的 Markdown 文件集合，位于你和原始资料之间。

- `raw/` = 源代码（不可变）
- LLM = 编译器
- `wiki/` = 编译产物（LLM 维护）
- Lint = 测试
- Query = 运行时

每次摄入新资料，知识就**复利增长**——后续所有查询都受益于之前的整理工作。

## 三层架构

```
<wiki-root>/
├── raw/                      # Layer 1: 不可变原始文档
│   ├── articles/             #   网页文章、博客
│   ├── papers/               #   论文 PDF/Markdown
│   ├── books/                #   书籍笔记
│   ├── videos/               #   视频/播客转录
│   └── notes/                #   个人笔记、想法
├── wiki/                     # Layer 2: LLM 生成的 Wiki
│   ├── index.md              #   内容目录（每次操作后更新）
│   ├── log.md                #   追加式操作日志
│   ├── overview.md           #   领域综述
│   ├── concepts/             #   概念页
│   ├── entities/             #   实体页（人物、组织、工具）
│   ├── sources/              #   来源摘要（每篇原始文档一个）
│   └── comparisons/          #   对比分析页
├── outputs/                  # 生成的报告、lint 结果
├── SCHEMA.md                 # Layer 3: Schema 配置（本文件）
└── .gitignore
```

## 核心操作

### 1. Init — 初始化 Wiki

当用户在新目录或新主题下首次使用时。

**步骤：**
1. 确认 wiki 根目录路径和主题
2. 创建上述完整目录结构
3. 初始化 `wiki/index.md`（空目录）
4. 初始化 `wiki/log.md`（空日志）
5. 创建 `SCHEMA.md`（从本模板定制）
6. 初始化 Git 仓库（如用户同意）
7. 报告创建结果

### 2. Ingest — 摄入资料

当用户添加新资料到 `raw/` 后触发。

**步骤：**
1. 扫描 `raw/` 中尚未在 `wiki/sources/` 有对应摘要的文件
2. 对每个新文件：
   a. **读取**原始文档，提取关键信息
   b. **讨论**关键发现（向用户汇报要点）
   c. **创建** `wiki/sources/<source-name>.md` 摘要页
   d. **更新/创建**相关的 concept 和 entity 页面
   e. **建立交叉引用**（`[[wikilink]]`）到相关页面
   f. **检查矛盾**：新信息是否与已有知识冲突
3. 更新 `wiki/index.md`
4. 追加 `wiki/log.md`（格式：`## YYYY-MM-DD ingest | 标题`）
5. 报告：新建/更新了哪些页面，发现了哪些值得注意的信息

**来源摘要页模板：**
```markdown
---
title: "来源标题"
type: source-summary
source: raw/articles/filename.md
date-ingested: YYYY-MM-DD
confidence: high
tags: [tag1, tag2]
related:
  - "[[concept-page]]"
  - "[[entity-page]]"
---

# 来源标题

## 一句话总结
...

## 关键要点
- 要点1
- 要点2

## 新概念
- [[new-concept]] — 简要描述

## 与我已有知识的关联
- 关联到 [[existing-page]]：...

## 值得深入的方向
- ...
```

### 3. Query — 查询 Wiki

当用户对 wiki 内容提问时触发。

**步骤：**
1. **先读 `wiki/index.md`** 定位相关页面（而非加载整个 wiki）
2. **精读相关页面**，综合信息
3. **引用来源**，使用 `[[wikilink]]` 格式
4. 如果答案新颖且有价值，**主动提议**将其保存为新的 wiki 页面

**重要原则：**
- 永远不要一次性加载整个 wiki 到上下文
- 通过 index.md 导航，按需读取
- 无法从 wiki 中找到答案时，诚实说明并建议摄入相关材料

### 4. Lint — 知识库健康检查

定期或按需触发。

**检查项：**
1. **矛盾检测**：不同页面间的冲突声明
2. **孤立页面**：没有任何入链的 wiki 页面
3. **缺失概念**：被引用但尚未创建页面的概念
4. **过时声明**：被新来源取代的旧断言
5. **低置信度页面**：标记为 `confidence: low` 且长期未更新
6. **死链**：指向不存在页面的 `[[wikilink]]`

**输出：** 保存到 `outputs/lint-YYYY-MM-DD.md`

**Lint 报告模板：**
```markdown
# Wiki Lint 报告 — YYYY-MM-DD

## 矛盾发现
| 页面A | 声明 | 页面B | 冲突声明 | 建议 |
|-------|------|-------|---------|------|
| ... | ... | ... | ... | ... |

## 孤立页面
- [[orphan-page]] — 无入链，建议链接到相关概念

## 缺失概念
- "概念名" 被 [[page-a]] 和 [[page-b]] 引用，建议创建页面

## 过时声明
- [[page]] 中关于 X 的断言已被 raw/articles/new-source.md 取代

## 统计
- 总页面数: N
- 概念页: N | 实体页: N | 来源摘要: N
- 交叉引用数: N
- 健康评分: X/100
```

## 页面规范

### 文件命名
- 使用 `kebab-case`：`attention-mechanism.md`、`large-language-model.md`
- 与概念名称一致，便于 `[[wikilink]]` 引用

### YAML Frontmatter（所有 wiki 页面必需）
```yaml
---
title: "页面标题"
type: concept | entity | source-summary | comparison
sources:
  - raw/articles/source.md
related:
  - "[[related-page]]"
created: YYYY-MM-DD
updated: YYYY-MM-DD
confidence: high | medium | low
---
```

### 交叉引用
- 内部链接使用 `[[wikilink]]` 格式
- 源引用使用 `raw/` 相对路径
- 外部 URL 使用标准 Markdown 链接

## 与 RAG 的对比

| 维度 | RAG | LLM Wiki |
|------|-----|----------|
| 状态 | 无状态，每次独立 | 有状态，知识复利累积 |
| 基础设施 | 向量数据库+嵌入管线 | 文件夹+Markdown |
| 交叉引用 | 每次查询临时发现 | LLM 预构建，始终可用 |
| 维护成本 | 嵌入更新、索引重建 | LLM 每次摄入自动更新 |
| 可追溯性 | 块级引用（常有损） | 源级引用，追溯到 raw/ |
| 适用规模 | 企业级（百万文档） | 个人/团队（50-200源） |
| 矛盾检测 | 无 | Lint 操作主动标记 |

## 最佳实践

1. **保持 raw/ 不可变**：永远不修改 raw/ 中的文件。如需修正，用户自行修改后重新摄入
2. **每次摄入都是复利**：摄入不仅创建摘要，还要级联更新相关概念页
3. **先读 index 再导航**：查询时不要全量加载，先读 index.md 定位
4. **有价值的答案要存档**：好的查询结果应提议保存为 wiki 页面
5. **定期 Lint**：建议每摄入 5-10 篇资料后运行一次 lint
6. **Git 就是审计日志**：每次操作后 commit，可追溯知识演化

## 工具参考

在 SimpleAgent 环境中：
- 读取文件：`read_file`
- 搜索内容：`grep`
- 写入页面：`write_file`
- 网络搜索：`internet_search`（用于补充上下文）
- 记忆存储：`remember`（用于跨会话持久化用户偏好）
