---
name: localization-release-copilot
description: "Shadow-mode copilot for localization / translation release operations. Given a source draft and its target-language version(s), it locks terminology, machine-checks numbers and proper nouns, preserves source attributions, flags structure loss, and produces a reviewable diff preview — without rewriting the translation. Designed for editorial long-form ZH↔EN localization; SaaS locale-file features (.po / placeholders / plurals) are flagged as pending until real samples exist."
description_zh: "本地化发布运营影子助手"
description_en: "Localization Release Copilot"
version: "1.0.1"
agent_created: true
---

# Localization Release Copilot

For a localization / translation release flow, take the **source draft** and its **target-language version(s)** and act as a shadow reviewer that catches release-breaking drift *before* publish: terminology drift, number mismatches, dropped proper nouns, lost source attributions, and structure loss. Output only a reviewable diff and a preview-ready checklist — never rewrite the translation itself.

## When to use

- You have a finished source (ZH article, paper, docs page, release note) and a human or model translation into another language (EN / others), and you want a pre-publish consistency pass.
- You publish the **same content in multiple languages** (WeChat ZH → LinkedIn EN / Substack EN; docs ZH → EN; in-product copy → locale) and want to confirm the target did not silently drop a number, a proper noun, or a source citation.
- You maintain a **glossary / term base** and need every release to respect locked terms (product names, framework names, units, branded metrics).
- You want a **reviewable PR-style preview** of what changed between source and target so a human reviewer can approve in one pass.
- You suspect "the English version reads fine but lost the data" — this skill is built to catch exactly that class of bug.

## Do not use

- A single-language copyedit / proofread of one draft → use `claim-to-source-auditor` or a dedicated compliance-review skill if one is installed.
- Consistency across *different materials on the same topic* (PR vs pitch vs deck) → use `cross-material-consistency-auditor`.
- Topic selection / portfolio evaluation → use `editorial-topic-portfolio`.
- Machine translation generation → this skill reviews, it does not translate.
- Directly modifying or rewriting the target text.

## Input

```yaml
source:
  path:
  language: zh | en | ...
targets:
  - path:
    language:
    label: LinkedIn | Substack | docs-EN | locale-EN
  - path:
glossary:          # optional: locked terms the target must respect
  - source_term:
    target_term:
    mandatory: true | false
preserve_attribution: true   # default true
review_only: true            # never rewrite; output a diff + preview
```

## Workflow

### Step 1: [Deterministic] Load source + targets

1. Read the source and every target.
2. Detect language, length, section count, and status (draft / final).
3. If a glossary is provided, load it as the locked-term table.

### Step 2: [Deterministic] Extract & normalize

For each file extract:

- Numbers **with units**, normalized to a canonical magnitude (locale-aware):
  - ZH `亿` → ×1e8, `万` → ×1e4; EN `B`/`billion` → ×1e9, `M`/`million` → ×1e6, `K`/`thousand` → ×1e3.
  - `8.3亿` ≈ `830M`, `117亿` ≈ `€11.7B`, `1.5亿` ≈ `€150M` are **equivalent, not mismatches**.
- Proper nouns / entities (capitalized tokens, quoted terms, org names, person names, product names).
- Source attributions (`（Source, Year）`, `Source (Year)`, inline citations).
- Glossary terms (if a glossary is supplied).
- Section-level structural promises (headings, promised lists).

Output `01-extracted-claims.json`.

### Step 3: [LLM] Build the diff matrix

Compare source → each target item by item; for each inconsistency record:

- Dimension: `terminology` | `number` | `proper_noun` | `attribution` | `structure_loss` | `locale_format`.
- Source wording vs Target wording.
- Difference type: term not honored, number dropped/changed, entity missing, citation lost, section omitted, correct locale adaptation misread as error.
- Severity:
  - **P0**: a number or legal/factual claim in the source is missing or contradicted in the target.
  - **P1**: a source attribution (org + year) is dropped or changed; a mandatory glossary term is not honored; a key proper noun is missing.
  - **P2**: non-mandatory term drift; section depth mismatch that does not change the claim; platform-specific condensation.
- Recommended unified wording (cite the source).
- Whether re-check is needed after the target is revised.

Consistent items are kept as positive records but not listed line by line.

### Step 4: [LLM] Produce a reviewable preview

Render a **PR-style preview** the human reviewer can approve in one pass:

- A short summary: source → target(s), what passed, what needs attention.
- A line-level diff for each P0/P1: source sentence → target sentence → suggested fix (do not auto-apply).
- A glossary-compliance block: which locked terms were honored / violated.
- A "ready to publish?" gate: **blocked** if any P0 remains, **needs review** if any P1 remains, **clear** otherwise.

### Step 5: [Deterministic] Human confirmation

Pause after the preview. Confirm:

- P0/P1 disposition.
- Whether the target should be revised (this skill never revises it).
- Whether the glossary needs an update.

After confirmation, the human or the corresponding Writer/Editor edits the target. This skill is review-only.

## Hard Rules

1. **Review-only.** Never modify the source or the target. Output a diff + preview; hands-off after delivery.
2. **Locale-aware by default.** `8.3亿` = `830M`, `117亿` = `€11.7B` are correct localizations — never flag them as mismatches. A checker that is not locale-aware will produce false positives and destroy trust.
3. **Attribution is part of the content.** If the source cites `(Synergy Research, 2024)`, the target must retain both the org and the year. Dropping either is a P1.
4. **Glossary terms are mandatory when marked.** A locked product/framework name must appear in the target exactly as specified.
5. **P0 blocks publish.** A missing or contradicted number/factual claim in the target is release-breaking.
6. **Source is authoritative.** When source and target disagree on a fact, the source wins for arbitration; the target is the one to fix.
7. **No fabricated wording.** Recommended fixes must reference an existing source string, never invent.

## Failure Handling

| Scenario | Action |
|---|---|
| Only the source provided, no target | Stop; the task requires at least one target |
| Target unreadable | Mark it and check only the remaining targets |
| Source contains an obvious error | Flag the error; do not propagate it into the target recommendation |
| No glossary supplied | Run with terminology inferred from the source; note "glossary recommended" |
| Source and target are different documents, not a translation pair | Stop and warn: this skill needs a true source→target pair, not two related-but-different docs |
| All checks pass | Report "no localization drift found" and clear |
| P0 found in an already-published target | Flag with extra severity and recommend a correction |

## Output Format

```text
<run-dir>/
├── 01-extracted-claims.json
├── 02-diff-matrix.md
├── 03-preview.md
└── 04-glossary-compliance.json
```

## Verification

- [ ] Every target compared to the source on numbers, proper nouns, attribution, glossary, structure.
- [ ] Every P0/P1 has a recommended fix that cites the source.
- [ ] Locale-equivalent numbers (亿/M, 万/K) treated as matches, not errors.
- [ ] Glossary-compliance block present for every mandatory term.
- [ ] Preview contains no source/target modifications.
- [ ] Human confirmation documented before the task is marked complete.

## Pitfalls

- Treating correct locale adaptation (`8.3亿`→`830M`) as a mismatch — the #1 way to make this skill useless.
- Honoring the target's "reads fine" and skipping the number check — drift hides in fluent text.
- Using two related-but-different documents (e.g. a ZH long article and an EN short commentary on the same theory) as a translation pair — they are not, and the check will produce noise.
- Assuming the model translation is the source of truth — the source draft is authoritative, the target is what gets fixed.
- Forgetting that LinkedIn/Substack condensations are legitimate; only flag structure loss that drops a *claim*, not a *section*.

---

## 中文摘要（Chinese Summary）

本 Skill 是**本地化 / 翻译发布运营**的影子助手：给它源稿和其一/多个目标语言版本，它锁定术语、机检数字与专有名词、保留来源标注、标记结构损失，并产出可审阅的差异预览——**不重写译文本身**。

**当前范围（Scope）：** 聚焦长文 editorial 的 ZH↔EN 本地化子集（源稿→目标稿）。**SaaS locale 文件特性**（.po diff、占位符、复数、翻译记忆）标注为"待真实样本补齐"，本版不依赖这些文件即可运行。

**关键约束（双语要点 / Bilingual key points）：**

- **只审阅不改写 Review-only**：绝不修改源稿或译文，只输出差异矩阵与预览；交付后 hands-off。
- **locale-aware 是生命线 Locale-aware**：`8.3亿`=`830M`、`117亿`=`€11.7B` 是正确本地化，**误报这类等价会被当成 bug 直接毁掉可信度**。
- **来源标注是内容一部分 Attribution matters**：源稿 `(Synergy Research, 2024)` 在目标稿必须保留机构+年份，掉落任一项即 P1。
- **术语表强制 Glossary mandatory**：标了 mandatory 的锁定词（产品名/框架名/单位）必须原样出现在目标稿。
- **P0 阻断发布 P0 blocks**：目标稿缺失或歪曲源稿的数字/事实主张，即为发布阻断级。
- **源稿为权威 Source authoritative**：源稿与目标事实冲突时以源稿仲裁，要改的是目标稿。

**何时该用它（场景引导 / When to reach for it）：** 你有成型的中文源稿 + 英文（或其他语言）译文，想在发布前确认"英文版没悄悄丢数字 / 专有名词 / 来源"；你维护术语表需要每次发布都遵守；你想要一个可一键审阅的 PR 式预览。它专门抓"英文读着通顺但数据丢了"这类 bug。
