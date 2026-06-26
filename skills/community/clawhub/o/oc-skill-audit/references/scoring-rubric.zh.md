# 评分标准 — 详细示例

各维度评分的具体示例。

---

## A. 结构 (Structure) 示例

### name 验证
| name | 分数 | 原因 |
|------|------|------|
| `summarize` | ✅10 | 小写、连字符 |
| `unit-converter` | ✅10 | 小写、连字符 |
| `Skill_Creator` | ❌0 | 包含大写、下划线 |
| `my-skill-is-really-long-and-descriptive-of-what-it-does` | ❌0 | 超过64字符 |
| `123skill` | ❌0 | 以数字开头 |

### description 质量
| description | 分数 | 原因 |
|------------|------|------|
| "摘要, 详细摘要, 5倍摘要, 帮我摘要, 整理, summary, summarize, digest..."（200词, what+when+keywords） | ✅15+10 | 清晰 + 关键词 |
| "有用的技能。" | ❌0 | 过于模糊 |
| "总结内容。" | ❌5 | 有what，但缺少when/keywords |

### 辅助文件 (auxiliary files)
| 文件组成 | 分数 |
|-----------|------|
| SKILL.md + references/ | ✅10 |
| SKILL.md + README.md | ❌0 |
| SKILL.md + CHANGELOG.md + INSTALL.md | ❌0 |

---

## B. 触发 (Triggering) 示例

### "When" 的放置位置
| 位置 | 分数 | 原因 |
|------|------|------|
| description包含 "Use when..." | ✅25 | 在正文之前加载 |
| SKILL.md正文有 "When to Use" 章节 | ❌0 | 正文在触发之后才加载 |
| 两者都有 | ⚠️15 | 正文存在对触发没有意义 |

### 关键词
| description | zh | en | 分数 |
|------------|----|----|------|
| "摘要, 简短摘要, 200字, summarize, digest" | ✅ | ✅ | ✅30 |
| "Summarize content into structured markdown" | ❌ | ✅ | ⚠️15 |

---

## C. 风格指南 (Style Guide) 示例

### 好的示例（摘要技能）
```markdown
### Preservation Criteria (never discard)
- Core arguments and evidence — convey the author's intent
- Specific examples — concretize abstract claims
- Figures and data — with sources

### Compression Criteria
- Repeated arguments — if the same content appears in multiple places, keep only one
```
→ ✅ preservation(30) + compression(25) + essence(20) = 75+

### 差的示例（仅格式）
```markdown
## Output Format
- Each chapter 3-5 sentences
- Include key takeaways
```
→ ❌ 无保留标准，无压缩标准 = 0

### N/A 适用例外
技能完全不使用sub-agent且为单一任务操作时：
- 应用Style Guide满分的50%（最高50 → N/A调整为70%分数）
- 原因：单一任务代理已内置自身的判断标准

---

## D. 工作流 (Workflow) 示例

### 好的示例（明确的 Phase 0）
```markdown
### Phase 0: Structure Analysis (★ most important)
1. Scan entire text to understand outline/section structure
2. Map topic flow
3. Include this information in sub-agent prompts

### Phase 1: ...
```
→ ✅ Phase 0(30) + 编号(15) + 上下文规划(25) = 70+

### 差的示例（无 Phase 0）
```markdown
## How to Use
1. Extract text from PDF
2. Split into chunks
3. Send to sub-agent
```
→ ❌ 无Phase 0 = 上下文规划0分，整体分数低

---

## E. Sub-Agent 设计示例

### 好的模板（使用 `[ ]`）
```markdown
## Context
[Full structure — filled by Phase 0]
[This chunk's position — filled by Phase 0]

## Preserve (this chunk only)
[Preservation list — filled by Phase 0]
```
→ ✅ template(20) + placeholders(20) + context(20) = 60+

### 差的模板（无上下文注入）
```markdown
Summarize the following text in 3-5 sentences.

---
[chunk text]
---
```
→ ❌ 无占位符，无上下文 = 低分

---

## F. 简洁性 (Conciseness) 示例

| SKILL.md 行数 | 分数 | 备注 |
|--------------|------|------|
| 120行 | ✅50 | 300行以下，奖励 +10 = 50 |
| 280行 | ✅40 | 500行以下 |
| 520行 | ⚠️20 | 略超，建议拆分 |
| 800行 | ❌0 | 大幅超标，必须拆分 |

### "代理很聪明" 违规
```markdown
## How to Read a File
Use the `read` tool to read the contents of a file. The `read` tool takes a
`path` parameter which specifies the file to read...
```
→ ❌ 冗余解释代理已知的工具用法 → -15

---

## 分数解读指南

### A (90+)：生产就绪
技能在所有维度上具有高质量，设计良好。仅需小幅改进即可部署。

### B (75–89)：良好
满足大部分标准，但在1-2个维度上有改进空间。

### C (60–74)：及格
基本功能可用，但如果使用sub-agent，质量可能会下降。
Style Guide或Phase 0可能缺失。

### D (45–59)：需要改进
多个维度不足。sub-agent结果可能不一致。
需要结构性改进。

### F (<45)：不合格
基本规格合规可能存在问题。需要重写frontmatter或description。
