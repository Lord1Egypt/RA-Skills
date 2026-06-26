# llm_wiki 摄入流程详解

> 本文件记录两步摄入流程的提示词逻辑。供高级用户定制 schema.md 时参考，或在 claude.md 中补充工作流说明。

---

## 摄入两步流程

### Step 1：分析（Analysis）

系统提示词核心：
```
You are an expert research analyst. Read the source document and produce a structured analysis.

## Language Rule
- ALWAYS match the language of the source document.

Your analysis should cover:

## Key Entities
- Name and type
- Role in the source (central vs. peripheral)
- Whether it likely already exists in the wiki (check the index)

## Key Concepts
- Name and brief definition
- Why it matters in this source
- Whether it likely already exists in the wiki

## Main Arguments & Findings
- Core claims or results
- Evidence supporting them
- Strength of the evidence

## Connections to Existing Wiki
- What existing pages does this source relate to?
- Does it strengthen, challenge, or extend existing knowledge?

## Contradictions & Tensions
- Does anything in this source conflict with existing wiki content?
- Are there internal tensions or caveats?

## Recommendations
- What wiki pages should be created or updated?
- What should be emphasized vs. de-emphasized?
- Any open questions worth flagging?
```

### Step 2：生成（Generation）

系统提示词核心（关键约定）：

**文件块格式**（LLM 输出必须遵守）：
```
---FILE: wiki/sources/filename.md---
(complete file content with YAML frontmatter)
---END FILE---
```

**必须生成的文件**：
1. 来源摘要页：`wiki/sources/{source-basename}.md`（必须使用此精确路径）
2. 实体页：`wiki/entities/` 下的关键实体
3. 概念页：`wiki/concepts/` 下的关键概念
4. 更新 `wiki/index.md`（追加新条目，保留所有现有条目）
5. 日志条目：`wiki/log.md`（格式：`## [YYYY-MM-DD] ingest | Title`）
6. 更新 `wiki/overview.md`（反映整个 wiki 的最新状态，2-5 段综述）

**Frontmatter 强制要求**：
- 每个页面必须含 `sources: ["原始文件名"]` 字段，将 wiki 页面追溯到原始资料
- 使用 `[[wikilink]]` 语法跨页引用
- kebab-case 文件名

**审核块格式**（Review Items）：
```
---REVIEW: type | Title---
Description of what needs the user's attention.
OPTIONS: Create Page | Skip
PAGES: wiki/page1.md, wiki/page2.md
SEARCH: search query 1 | search query 2 | search query 3
---END REVIEW---
```

审核类型：
- `contradiction`：来源与现有 wiki 内容冲突
- `duplicate`：实体/概念可能已以不同名称存在于 wiki
- `missing-page`：重要概念被引用但没有专属页面
- `suggestion`：值得进一步研究的话题或关联来源

---

## log.md 追加逻辑

`wiki/log.md` 是特殊文件——只追加，从不覆盖，**逆序排列**（最新条目在文件顶部）：
```typescript
// log.md 处理逻辑
if (relativePath === "wiki/log.md" || relativePath.endsWith("/log.md")) {
  const existing = await readFile(fullPath)
  // 新条目插入到已有内容之前（逆序）
  const appended = existing ? `${content.trim()}\n\n${existing}` : content.trim()
  await writeFile(fullPath, appended)
} else {
  await writeFile(fullPath, content)
}
```

在 schema.md 中，可以明确告知 LLM：
> "wiki/log.md 是 append-only 文件。每次操作只输出新追加的条目，不要输出完整文件内容。"

---

## 摄入缓存机制

Wiki 系统内置摄入缓存：如果资料内容未变更，跳过重复摄入。
缓存基于文件内容哈希，存储已写入的 wiki 页面列表。

---

## 语言规则（关键）

```typescript
export const LANGUAGE_RULE = "## Language Rule\n- ALWAYS match the language of the source document. If the source is in Chinese, write in Chinese. If in English, write in English. Wiki page titles, content, and descriptions should all be in the same language as the source material."
```

此规则在摄入分析和生成两步中都强制执行。在 schema.md 末尾加上此语言规则，可确保 LLM 一致遵守。