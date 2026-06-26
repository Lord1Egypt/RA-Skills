# 採点ルーブリック — 詳細例

各次元の採点に関する具体的な例です。

---

## A. 構造 (Structure) の例

### name バリデーション
| name | 点数 | 理由 |
|------|------|------|
| `summarize` | ✅10 | 小文字、ハイフン |
| `unit-converter` | ✅10 | 小文字、ハイフン |
| `Skill_Creator` | ❌0 | 大文字、アンダースコア |
| `my-skill-is-really-long-and-descriptive-of-what-it-does` | ❌0 | 64文字超過 |
| `123skill` | ❌0 | 数字で開始 |

### description 品質
| description | 点数 | 理由 |
|------------|------|------|
| "要約, 詳細要約, 5倍要約, 要約して, まとめ, summary, summarize, digest..." (200語, what+when+keywords) | ✅15+10 | 明確 + キーワード |
| "役立つスキルです。" | ❌0 | 曖昧すぎる |
| "内容を要約します。" | ❌5 | whatはあるが、when/keywordsがない |

### 補助ファイル (auxiliary files)
| ファイル構成 | 点数 |
|-----------|------|
| SKILL.md + references/ | ✅10 |
| SKILL.md + README.md | ❌0 |
| SKILL.md + CHANGELOG.md + INSTALL.md | ❌0 |

---

## B. トリガリング (Triggering) の例

### "When" の配置場所
| 場所 | 点数 | 理由 |
|------|------|------|
| descriptionに "Use when..." が含まれる | ✅25 | 本文より先にロードされる |
| SKILL.md本文に "When to Use" セクションがある | ❌0 | 本文はトリガリング後にロードされる |
| 両方にある | ⚠️15 | 本文の存在はトリガリングに意味がない |

### キーワード
| description | ja | en | 点数 |
|------------|----|----|------|
| "要約, 短く要約, 200文字, summarize, digest" | ✅ | ✅ | ✅30 |
| "Summarize content into structured markdown" | ❌ | ✅ | ⚠️15 |

---

## C. スタイルガイド (Style Guide) の例

### 良い例 (要約スキル)
```markdown
### Preservation Criteria (never discard)
- Core arguments and evidence — convey the author's intent
- Specific examples — concretize abstract claims
- Figures and data — with sources

### Compression Criteria
- Repeated arguments — if the same content appears in multiple places, keep only one
```
→ ✅ preservation(30) + compression(25) + essence(20) = 75+

### 悪い例 (形式のみ)
```markdown
## Output Format
- Each chapter 3-5 sentences
- Include key takeaways
```
→ ❌ preservation基準なし、compression基準なし = 0

### N/A 適用例外
スキルがsub-agentを全く使用せず、単一タスクである場合：
- スタイルガイドスコアの50%を適用（最大50 → N/A調整で70%スコア）
- 理由：単一タスクエージェントは既に独自の判断基準を内蔵している

---

## D. ワークフロー (Workflow) の例

### 良い例 (明示的な Phase 0)
```markdown
### Phase 0: Structure Analysis (★ most important)
1. Scan entire text to understand outline/section structure
2. Map topic flow
3. Include this information in sub-agent prompts

### Phase 1: ...
```
→ ✅ Phase 0(30) + 番号付け(15) + コンテキスト計画(25) = 70+

### 悪い例 (Phase 0 なし)
```markdown
## How to Use
1. Extract text from PDF
2. Split into chunks
3. Send to sub-agent
```
→ ❌ Phase 0なし = コンテキスト計画0点、全体的に低スコア

---

## E. Sub-Agent 設計の例

### 良いテンプレート (`[ ]` 使用)
```markdown
## Context
[Full structure — filled by Phase 0]
[This chunk's position — filled by Phase 0]

## Preserve (this chunk only)
[Preservation list — filled by Phase 0]
```
→ ✅ template(20) + placeholders(20) + context(20) = 60+

### 悪いテンプレート (コンテキスト注入なし)
```markdown
Summarize the following text in 3-5 sentences.

---
[chunk text]
---
```
→ ❌ placeholdersなし、コンテキストなし = 低スコア

---

## F. 簡潔性 (Conciseness) の例

| SKILL.md 行数 | 点数 | 備考 |
|--------------|------|------|
| 120行 | ✅50 | 300行未満、ボーナス +10 = 50 |
| 280行 | ✅40 | 500行未満 |
| 520行 | ⚠️20 | やや超過、分割推奨 |
| 800行 | ❌0 | 大幅超過、分割必須 |

### "エージェントは賢い" 違反
```markdown
## How to Read a File
Use the `read` tool to read the contents of a file. The `read` tool takes a
`path` parameter which specifies the file to read...
```
→ ❌ エージェントが既に知っているツール使用法を冗長に説明 → -15

---

## スコア解釈ガイド

### A (90+): 本番稼働準備完了
全次元で高品質を備えた well-designed なスキルです。軽微な改善のみでデプロイ準備完了です。

### B (75–89): 良好
ほとんどの基準を満たしていますが、1〜2次元で改善の余地があります。

### C (60–74): 可
基本的には機能しますが、sub-agentを使用すると品質が低下する可能性があります。
Style GuideまたはPhase 0が欠落している可能性が高いです。

### D (45–59): 改善が必要
複数次元で不足しています。sub-agentの結果が不整合になる可能性が高いです。
構造的改善が必要です。

### F (<45): 不足
基本仕様の遵守に問題がある可能性があります。frontmatterまたはdescriptionの書き直しが必要です。
