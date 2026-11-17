<!-- Migrated from shuorenhua/evals/run-eval.md. SF/SNF cases validate the bilingual subtraction engine. -->

# Evaluation Instructions

## General evaluation prompt

Paste the following block into any model with a long enough context window to run the evaluation.

---

You are an evaluator for an AI-tone-removal rule set.

**Rule files:**
- Main entry: `./SKILL.md`
- Positive Style Contract: `./references/positive-style.md`
- Protected Spans: `./references/protected-spans.md`
- Chinese phrase list: `./references/phrases-zh.md`
- English phrase list: `./references/phrases-en.md`
- Structural anti-patterns: `./references/structures.md`
- Severity tiers: `./references/severity.md`
- Rewrite examples: `./references/examples.md`
- Micro-operation manual: `./references/operation-manual.md`
- Scene guardrails: `./references/scene-guardrails.md`
- Scene packs: `./references/scene-packs.md`
- Quick checklist: `./references/quick-checklist.md`
- Human review rubric: `./references/human-rubric.md`
- Boundary cases: `./references/boundary-cases.md`

**Evaluation set:**
`./evals/benchmark.md`

**Your task:**

1. Read `SKILL.md` first and understand the main flow: scene judgment -> protected spans -> tier judgment -> rewrite tier -> scope judgment -> fidelity reread -> residue reread -> output contract.
2. Then read the relevant files under `references/` as needed to fill in phrase lists, structural rules, boundary cases, second-pass checks, and false-positive protection.
3. Then read `./evals/benchmark.md` and evaluate every test case in it.

### For Should Fix (`SF-01` to `SF-42`)
- Judge the primary scene (`chat`, `status`, `docs`, `public-writing`) and the problem type first.
- Judge the rewrite tier (`minimal`, `standard`, `aggressive`).
- Judge the scope (`structural`, `bounded`, `in-place`). Long `public-writing` defaults to `bounded`: fully empty sentences go to a deletion list, substantive sentences get in-sentence cleanup, and no sentence merge or paragraph reorder is allowed. If the user explicitly wants near-original structure, or the sample is marked `Long-form / in-place`, obey the `in-place` boundary instead.
- Do a fidelity reread first. Only run `Residual Audit` if the first pass preserved the facts but still feels obviously AI-shaped.
- The second pass checks exactly five things: opener residue, summary residue, narrator residue, vague judgment residue, and over-even sentence length.
- Apply the rules to the original text. By default, output a rewrite. If the sample passes under `audit-only`, you may output only a risk note about missing sourcing or attribution instead of rewriting the full passage.
- You may consult `human-rubric.md` when judging rewrite quality, but do not mix rubric scores into engine `score`.
- List the hits: problem family plus the exact words or structures triggered.
- Judge the result as pass (`✅`), partial pass (`⚠️`), or fail (`❌`) and explain briefly.
- For unsupported-attribution SF cases, also judge by scene: in `public-writing` or `chat`, deleting unsupported authority framing counts as `✅`; in `docs` or `status`, clearly marking missing attribution without presenting the claim as proven counts as `✅`.
- For `Residual Audit` SF cases, verify that the second pass only makes light corrections. If it rewrites the whole piece for polish, invents facts, or makes `status`/`docs` more casual than they should be, mark `❌`.
- For `Scene Packs` SF cases, also determine whether the sample belongs to the `README`, `release-note`, `forum-post`, or `issue-reply` sub-scene and shape the tone for that publishing purpose.
- For `Long-form / in-place` SF cases, also check whether sentence count, paragraph order, and key transitions are preserved. If whole sentences are deleted, adjacent sentences are merged, or paragraphs are reordered, mark `❌`.

### For Should NOT Fix (`SNF-01` to `SNF-33`)
- Explain why the text should not be changed.
- If it stays as is or gets only the smallest harmless adjustment, mark `✅`.
- If the rewrite incorrectly changes terminology, system subjects, technical reporting, quoted text, or valid phrasing from boundary cases, mark `❌` as a false positive and explain the failure.
- For `Scene Packs` SNF cases, also verify that an already-direct README, release note, forum post, or issue reply was not pushed into the wrong scene.
- For `Long-form / in-place` SNF cases, also verify that rhythm-carrying repetition, handoff sentences, and transition sentences were not deleted.

### Final summary
Output a summary table:

```text
| Case | Type | Result | Notes |
|------|------|------|------|
| SF-01 | Should Fix | ✅/⚠️/❌ | ... |
| ... | ... | ... | ... |
| SNF-01 | Should NOT Fix | ✅/❌ | ... |
| ... | ... | ... | ... |
```

Also report:
- SF pass rate: X/42
- SNF false-positive rate: X/33
- Whether the target is met: SF > 90%, SNF false-positive rate < 10%

**Notes:**
- Do not falsely flag system subjects, technical terms, academic passive voice, or real debug dialogue.
- For `code-context` samples, only edit prose in comments, docstrings, or commit messages. Do not edit code itself.
- For `Scene Packs` samples, preserve the main scene and protected spans first, then follow the sub-scene publishing purpose. Do not turn a release note into marketing copy, a forum post into an announcement, or an issue reply into customer-support language.
- For `Long-form / in-place` samples, do not delete whole sentences, merge adjacent sentences, or reorder paragraphs. Target retention is `>= 0.90`, with a hard floor of `0.85`.
- For `Bounded` samples, do not delete substantive sentences wholesale, do not place real-content sentences into the deletion list, and do not merge a buzzword shell sentence with the following data sentence.

---

## Quick run in Codex

```bash
codex exec -C . --sandbox read-only \
  "Read ./SKILL.md first, then the relevant files under ./references/, and evaluate every case in ./evals/benchmark.md. For SF cases, judge the scene, tier, rewrite tier, and scope first, then apply the rules and decide whether the case passes. If the sample is a README, release note, forum post, or issue reply, also read ./references/scene-packs.md and handle the matching sub-scene. If it is marked Long-form / in-place, obey the no-whole-sentence-deletion, no-adjacent-sentence-merge, and no-paragraph-reorder boundaries, and check retention, sentence alignment, and key transitions. Do a fidelity reread before any Residual Audit, and only run Residual Audit if the first pass preserved the facts but still leaves obvious AI residue. Residual Audit may check only opener residue, summary residue, narrator residue, vague judgment residue, and over-even sentence length, and it may only make light edits. Default to outputting the rewrite, but for unsupported-attribution samples that pass as audit-only, you may output just the sourcing or attribution risk note. Judge unsupported-attribution SF cases by scene: in public-writing or chat, deleting unsupported authority framing counts as a pass; in docs or status, clearly marking the missing source without presenting the claim as proven counts as a pass. For SNF cases, judge whether the tool creates false positives. In mixed samples, only touch the truly problematic body text; do not alter user instructions, quotations, or discussed terms. In code-context samples, edit only comments, docstrings, and commit messages. In Scene Packs samples, do not remove version numbers, paths, links, identifiers, or ownership. Finish with a summary table, SF pass rate, and SNF false-positive rate."
```

## Quick run in Claude Code

Start Claude Code in the project directory and paste:

```text
Read ./SKILL.md and the relevant files under ./references/, then evaluate every case in ./evals/benchmark.md. For SF cases, judge the scene, tier, rewrite tier, and scope first, then apply the rules and decide whether the case passes. If the sample is a README, release note, forum post, or issue reply, also read ./references/scene-packs.md and handle the matching sub-scene. If it is marked Long-form / in-place, obey the no-whole-sentence-deletion, no-adjacent-sentence-merge, and no-paragraph-reorder boundaries, and check retention, sentence alignment, and key transitions. Do a fidelity reread before any Residual Audit, and only run Residual Audit if the first pass preserved the facts but still leaves obvious AI residue. Residual Audit may check only opener residue, summary residue, narrator residue, vague judgment residue, and over-even sentence length, and it may only make light edits. Default to outputting the rewrite, but for unsupported-attribution samples that pass as audit-only, you may output just the sourcing or attribution risk note. Judge unsupported-attribution SF cases by scene: in public-writing or chat, deleting unsupported authority framing counts as a pass; in docs or status, clearly marking the missing source without presenting the claim as proven counts as a pass. For SNF cases, judge whether the tool creates false positives. In mixed samples, only touch the truly problematic body text; do not alter user instructions, quotations, or discussed terms. In code-context samples, edit only comments, docstrings, and commit messages. In Scene Packs samples, do not remove version numbers, paths, links, identifiers, or ownership. Finish with a summary table, SF pass rate, and SNF false-positive rate.
```

## Generic LLM / API

If you are using ChatGPT, Claude Web, or another API:

1. Use the "General evaluation prompt" block above as the system prompt or first message.
2. Paste in the contents of `SKILL.md`, the relevant files under `references/`, and `evals/benchmark.md`.
3. If the token budget is tight, prioritize `SKILL.md`, `benchmark.md`, `scene-packs.md`, `severity.md`, and `boundary-cases.md`.

Note: shorter-context models may not finish all 75 cases in one pass. Split the run if needed, for example SF first and SNF second.
