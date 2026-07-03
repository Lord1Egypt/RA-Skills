---
name: obsidian-wiki-manager
description: Manage an Obsidian-based personal knowledge base (wiki) with strict ingestion, query, lint, reflect, merge, and system maintenance protocols. Trigger on ingest/摄入/query/lint/检查/reflect/综合分析/merge/去重/add question operations.
official: false
version: 1.0.0
name_zh: "知识库管理器"
description_zh: "管理基于 Obsidian 的个人知识库（wiki），包含严格的摄入、查询、检查、反射、合并和系统维护协议。当用户执行 ingest/摄入/query/lint/检查/reflect/综合分析/merge/去重/add question 等操作时触发。"
---

# Obsidian Wiki Manager

个人知识库管理系统，遵循 **Raw → Wiki → Outputs** 三层架构。

## 架构概览

| 层 | 目录 | 说明 | 权限 |
|---|---|---|---|
| **Raw** | `raw/` | 原始素材（文章、剪藏、图片、PDF、笔记、个人写作） | 只读，由人类拥有 |
| **Wiki** | `wiki/` | 结构化知识（来源页、概念卡片、实体页、综合分析） | 完全读写 |
| **Outputs** | `wiki/outputs/` | 输出产物（QUERY 答案、LINT 报告、Gap 报告等） | 写入，graph-excluded |

**核心原则**：
- LLM 完全拥有 `wiki/` 目录的读取和写入权限
- `raw/` 目录由人类拥有，LLM 只能读取，**绝不修改**
- 系统文件（index/log/overview/QUESTIONS）不参与 Obsidian 图谱

## 配置要求

```yaml
vault_root: "D:\\obsidian-job\\job"
qmd_cmd: "D:\\obsidian-job\\job\\qmd.bat"  # qmd 封装脚本
```

---

## 一、INGEST（摄入）操作规范

**触发词**：`ingest`、`摄入`、`处理这个`

### 来源类型判断

1. frontmatter 含 `type: personal-writing` → 走「个人写作」流程
2. 文件路径包含 `raw/personal/` → 走「个人写作」流程
3. frontmatter 含 `type: pdf-reference` → 走「PDF 参考」流程
4. 其他 → 走「外部来源」标准流程

### URL 直接输入处理规则

1. **获取内容**：使用 web-content-fetcher 技能或 `win_web_read` 获取页面完整内容，转换为 Markdown
2. **确定文件名**：根据页面标题或 URL 路径生成文件名，保存到 `raw/clippings/` 目录
3. **确定作者和日期**：从页面元数据中提取 author 和 publish_date，无法提取则标注「来源未知」
4. **保存后继续标准流程**：对保存的文件执行完整 INGEST 流程
5. **source_url 记录**：在 source 页中同时保留 `raw_file` 和 `source_url`
6. **去重检查**：如果已有相同或高度相似来源，更新已有 source 页，不创建重复

### 缺少 frontmatter 的处理规则

- 从文件第一个 `#` 标题提取 title；若无标题则从文件名推断
- `source` 字段留空，在 source 页中标注「来源未知」
- `date` 使用文件系统修改时间
- **不中断 INGEST**，但在 log.md 记录警告

### 外部来源标准流程（12 步）

**Step 1**：读取目标原始来源

**Step 2**：计算 SHA-256 哈希（Python `hashlib`）

**Step 3**：与用户确认核心要点

**Step 4**：生成 slug（小写英文，用连字符）

**Step 5**：创建 `wiki/sources/<slug>.md`，frontmatter 写入：
- `raw_file`：相对路径
- `raw_sha256`：SHA-256 哈希值
- `last_verified`：摄入日期
- `canonical_source`：翻译/转述来源同源标记
- 来源超过 2 年前：标注 `possibly_outdated: true`

**Step 5.5 — canonical_source 译文同源检测**：
1. 遍历已有 source 页的 `canonical_source` 字段
2. 若指向同一原始来源：标记为同源，不创建新概念/实体
3. 在 Contradictions 节记录
4. 同源来源仅计为 1 个来源

**Step 6 — 概念名称对齐检查**：
1. 映射为英文小写连字符 slug
2. 查已有 concept 文件
3. **检查所有 concept 页的 `aliases` 字段**
4. 匹配则更新，不创建新页
5. 不匹配才创建新页

**Step 7**：为每个概念：更新或创建 concept 页
- Evolution Log 追加规则：「强化」/「修正」/「新增分歧」

**Step 8**：为每个实体：同上逻辑

**Step 9**：更新 `wiki/index.md`

**Step 10**：检查 `wiki/QUESTIONS.md` 匹配

**Step 11**：追加 `wiki/log.md`

**Step 12（索引同步）**：执行 `qmd update` + `qmd embed`，报错则跳过记录

### 个人写作流程

- 不生成 Summary 节，跳过客观摘要
- 核心论点写入 `## My Position` 节（标注「个人认知」）
- 不参与 confidence 的 `source_count` 计数
- Evolution Log 记录：「YYYY-MM-DD 个人写作 [[slug]] 确立了对此概念的明确立场」

---

## 二、QUERY（查询）操作规范

**触发词**：直接提问，或「根据我的知识库」

**Step Q1**：执行 `qmd search "<query>" -n 5 --json`（本机环境 `qmd query` 的 LLM 扩充会超时，故用 search 替代）
- 若报错则降级读取 `wiki/index.md`

**Step Q2**：逐一完整读取 top 5 文件

**Step Q3**：合成答案
- 每个核心结论必须溯源到具体 `wiki/sources/<slug>.md`
- 注明各来源 confidence 级别
- 来源矛盾时显式标注分歧

**Step Q4**：若答案有复用价值，写入 `wiki/outputs/`

### 输出格式

| 问题类型 | 输出格式 |
|---|---|
| 普通问题 | Markdown 正文 |
| 比较类 | Markdown 表格 |
| 演示类 | Marp 幻灯片 |
| 趋势类 | Python matplotlib 代码块 |
| 清单类 | 结构化 bullet list |

---

## 三、LINT（检查）操作规范

**触发词**：`lint`、`检查`、`健康检查`

1. 运行 `scripts/lint.py`（9 项检查）
2. 报告写入 `wiki/outputs/lint-YYYY-MM-DD.md`
3. 执行 `qmd status`，对比索引；落后则执行 `qmd update`
4. 展示摘要并询问是否修复

---

## 四、REFLECT（反射）操作规范

**触发词**：`reflect`、`综合分析`、`发现规律`

**Stage 0 — 反向检验**：主动搜索反驳证据，无则标注「⚠ 回音室风险」

**Stage 1 — 模式扫描**：
- `qmd multi-get "wiki/concepts/*.md" -l 40`
- `qmd multi-get "wiki/entities/*.md" -l 40`
- `qmd multi-get "wiki/synthesis/*.md" -l 60`

**Stage 2 — 深度合成**：写入 `wiki/synthesis/<topic>-synthesis.md`

**Stage 3 — Gap Analysis**：
- source_count=1 且创建 >30 天的孤立概念
- 多处提及但无独立页面的概念/实体
- 输出到 `wiki/outputs/gap-report-YYYY-MM-DD.md`

---

## 五、MERGE（合并）操作规范

**触发词**：`merge`、`去重`

### 同语言合并
1. 与用户确认（绝不自动合并）
2. 主 slug 保留，更新 wikilinks
3. 被合并文件替换为重定向文件

### 跨语言合并
1. 主 slug 保留英文
2. aliases 取并集
3. 内容按并集+去重合并
4. 旧 slug 保留为 redirect 文件

---

## 六、ADD-QUESTION 操作规范

**触发词**：`我想搞清楚`、`add question`、`记录一个问题`

1. 将问题规范化
2. 追加到 `wiki/QUESTIONS.md`（checkbox 格式）
3. 追加 `wiki/log.md`

---

## 七、系统规则

### Wikilink 格式铁律

所有 wikilink 目标必须使用**英文小写连字符格式**：

| ✅ 正确 | ❌ 错误 |
|---|---|
| `[[value-investing]]` | `[[价值投资]]` |
| `[[attention-mechanism]]` | `[[ValueInvesting]]` |

中文名称写入 concept 页 `aliases` 字段。

### 禁止使用 wikilinks 的场景

- 不得引用系统文件：`[[log]]` `[[index]]` `[[overview]]` `[[QUESTIONS]]`
- 不得引用 lint 报告：`[[outputs/lint-xxx]]`
- 不得以操作名称作为 wikilink：`[[ingest]]` `[[query]]`
- log.md 使用纯文本路径

### Wiki 语言规范

- Wiki 层统一中文写作
- concept 页 `title` 使用中文主名称
- slug（文件名）统一英文小写连字符
- `aliases` 覆盖中英文所有叫法

### Confidence 更新规则

| 来源数 | Confidence | 处理 |
|--------|------------|------|
| 1 个 | `low` | 自动设置 |
| 3+ 个 | `medium` | 自动设置 |
| 5+ 个无矛盾 | 候选 `high` | 需用户确认 |

个人写作不参与 count。

### Source Integrity Rules

- re-ingest 规则：lint 报告 `⚠ SOURCE MODIFIED` 时重新摄入
- 来源 >2 年标注 `possibly_outdated: true`
- 矛盾来源必须在 Contradictions 节显式记录

### 系统文件隔离规则

以下文件 frontmatter 含 `graph-excluded: true`：
- `wiki/log.md`、`wiki/index.md`、`wiki/overview.md`、`wiki/QUESTIONS.md`
- `wiki/outputs/` 下所有文件

### 文档维护规则

当此 skill 规则更新时，同步更新 `USER_GUIDE.md` 对应章节。
