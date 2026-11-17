---
name: minimal-edit
display_name: SurgeonEdit
display_name_en: SurgeonEdit
description: 'Apply minimal, tone-preserving edits to existing written text. 对既有文本做最小化局部修改：只动该动的，保持语气、篇幅与结构，不展开、不强调、不标注改动。附一个可选的改动自检脚本 scripts/audit_edit.py，文本只经文件或标准输入传入。Use when the user asks to revise, correct, change, delete, soften, reword, or adjust a specific part of an existing Chinese or English document, report, article, prompt, meeting minutes, or message, especially when the edit should not be expanded, emphasized, marked, or look like a patch. 中文触发词：不要展开、不要强调、别把改动标出来、改动处不要标出来、改得自然一点、不要 AI 味、删掉就好、只改观点、改完像伤疤。English triggers: don''t expand, don''t emphasize, don''t mark the change, keep it natural, remove the AI tone, just delete it, change only the opinion. 词表与自检规则只覆盖中文和英文，其他语言仅人工判断。Do not use when there is no existing text to edit; not for translation, summarization, drafting from scratch, or repackaging and restructuring a whole document, unless the user explicitly asks for a large transformation.'
---

# Minimal Edit

## Core Rule

Treat every request as a local edit unless the user explicitly asks for a full rewrite. Change exactly the semantic unit in scope and preserve everything else: sentence rhythm, length, emphasis, structure, tone, facts, examples, and formatting.

## Workflow

1. Read the original text and mark the smallest span that must change.
2. Classify the intent:
   - Change viewpoint: replace the claim, keep the same sentence shape.
   - Delete: remove the span and repair only what grammar requires.
   - Lower emphasis: demote the point to an ordinary sentence, remove bold, callouts, or examples.
   - Fix fact or wording: swap only the wrong tokens.
   - De-AI tone: remove formulaic markers without adding new framing.
   - Composite: split the request into atomic operations; apply content changes first, then tone, then emphasis and format.
   - Full rewrite: only if the user asks for a large restructuring or new draft.
3. Apply the edit with the original as the invariant baseline.
4. Deliver clean revised text only.
5. Run the self-check below before returning.

## Operation Rules

### Change viewpoint

Replace the semantic claim, not the paragraph around it. Keep the same sentence structure, level of detail, and length. If the original is one clause, the replacement stays one clause. Do not add caveats, examples, reasoning, or transition sentences unless the user asks for them.

That rule governs style. It never authorises removing substance the reader needs in order to act on the text:

- factual corrections, and stated data caveats such as 口径、来源、统计区间、样本范围;
- risk, safety, compliance, legal, or eligibility warnings;
- conditions that qualify a claim, such as 尚未验证、处于早期阶段、取决于量产节奏;
- anything the user's own conventions require to be disclosed.

If the edit would delete or weaken one of these, keep it and say so separately — which one you kept and why. If the user still insists on removing it, state plainly what the removal costs, then comply.

If the user says to recommend something implicitly, keep the recommendation implicit. Do not turn it into an explicit conclusion, and do not append hedging or a list of fresh disclaimers that were not in the original.

### Delete

Remove the target text. Fix only the connectors needed to keep the sentence grammatical and the surrounding flow intact. Do not add a replacement sentence that summarizes what was deleted. Do not add "总之", "因此", or a new conclusion to fill the gap.

### Lower emphasis

Remove or reduce the visual and rhetorical weight: drop bold, headings, callouts, repeated examples, and superlatives if they are the reason the passage stands out. Keep the factual content, but state it at the same level as neighboring sentences.

### Fix fact or wording

Change only the incorrect fact or expression. Preserve the rest of the sentence exactly, including its punctuation and surrounding clauses.

### De-AI tone

Remove formulaic AI-sounding phrases and mechanical structure. Keep facts, logic, and the user's point. Do not replace one AI phrase with another AI phrase, and do not add new framing or summary sentences.

Common Chinese candidates include 赋能, 抓手, 闭环, 颗粒度, 场景化, 底层逻辑, 战略协同, 深度绑定, 一站式, 全方位, 多维度, 系统性, 组合拳, 矩阵, 拉通, 对齐, 降本增效, and 提质增效. Common English candidates include "it is worth noting", "in conclusion", "leverage", "synergy", "holistic", "ecosystem", and "seamless". Treat these as manual-review candidates, not automatic proof of a problem.

### Composite requests

When a request combines operations, such as "delete this sentence and soften the tone", split it into atomic operations first. Apply content changes first, then tone, then emphasis and formatting. Keep one invariant set across the whole batch: the final result must be the smallest change that satisfies every part. If two parts conflict, choose the lighter interpretation and keep the final text minimal. Audit against every requested operation, not just the first one.

## Forbidden in the Edited Result

- No change labels inside the deliverable: "改动如下", "修改如下", "原文", "加粗", diff markers, or annotations.
- No new transition or emphasis formulas unless they already existed: "综上所述", "总体而言", "值得注意的是", "需要指出的是", "换言之", "换句话说", "更准确地说", "需要说明的是".
- No new Chinese or English AI-flavor markers unless they already existed: 赋能, 抓手, 闭环, 颗粒度, 场景化, 底层逻辑, 战略协同, 深度绑定, 一站式, 全方位, 多维度, 系统性, 组合拳, 矩阵, 拉通, 对齐, 降本增效, 提质增效, "it is worth noting", "in conclusion", "leverage", "synergy".
- No new bold, headings, callouts, bullets, or tables added just to mark the edit.
- No new examples, caveats, hedging, or reasoning unless the user requested more detail. This bars additions only; it never authorises deleting a caveat that already exists — see Change viewpoint.
- No full-paragraph rewrites for a sentence-level request.

## Length Budget

- Replacement text should be roughly the same length as the replaced text: between 0.5x and 1.5x for a clause-level change, up to about 2x for a sentence-level rewording, and never multiple new sentences.
- Deleting should make the result shorter by roughly the deleted length.
- Do not add a new sentence unless grammar or the user's request requires it.
- Every added or removed character must be traceable to the user's request or to a necessary grammatical repair.

## Delivery

Return the clean revised text only. If the user asks why something changed, explain in a separate short note outside the deliverable, never with inline markers in the final text.

## Bundled Script

`scripts/audit_edit.py` is the only executable this skill ships. It compares two pieces of text you hand it and prints warnings about expansion, added bold, new AI-flavor markers, and phrases that should have been removed. It is a self-check aid, not an editor and not part of the deliverable. It reads only the files named on the command line plus stdin: it does not walk the working directory, read environment variables, or use the network. Its marker lists cover Chinese and English only.

## Self-Check

1. Compare before and after side by side. Any changed line must be the user's target or a necessary connector.
2. Run the audit script in the matching mode. Pass document text through files or stdin, never as a command-line argument:
   - Both sides in files: `python scripts/audit_edit.py --before <original.txt> --after <edited.txt>`
   - Revised text piped in: `python scripts/audit_edit.py --before <original.txt> --after-stdin < <revised.txt>`
   - Single channel, for conversation-only edits: `python scripts/audit_edit.py --stdin` with a JSON payload `{"before": "...", "after": "...", "must_remove": ["..."]}`
   - Phrases to delete: `--must-remove-file <list.txt>` when a phrase contains quotes, or repeat `--must-remove "<phrase>"` for short plain phrases.
   Inline `--before-text` and `--after-text` still work but print a warning, because text passed as an argument can be retained in shell history, process listings, and orchestration logs. Do not use them for confidential documents.
   Fix or manually review every warning before delivering. Marker warnings are candidates, not proof that the text is clean.
3. Read the result without looking at the original. If any sentence sounds like an AI patch, remove or rewrite it.
4. Confirm no new formatting emphasis was added.
5. Confirm the edit did not expand the point unless expansion was explicitly requested.

## Examples

When the task feels ambiguous or you need concrete before/after patterns, read `references/examples.md` and match the closest case.
