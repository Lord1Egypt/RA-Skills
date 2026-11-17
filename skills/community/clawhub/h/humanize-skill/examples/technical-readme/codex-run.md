# Codex Skill E2E Run: Technical README

Run date: 2026-06-04
Host: Codex
Mode: agent-native semantic rewrite, no CLI or regex rewrite pass

## Scope

- Surface: README / project documentation.
- Audience: developers evaluating whether to install the skill.
- Goal: improve README quality by explaining behavior and limits without marketing language.
- Evidence policy: preserve agent-native workflow claims; remove file-format, dependency, and perfect-accuracy promises that belonged to the removed CLI.

## Voice Profile

- Source: `sample.txt`
- Style: plain technical writing.
- Rhythm: short paragraphs, names limits explicitly.
- Constraint: "boring in the good way"; no inflated utility claims.

## AI-pattern Audit

- Removed inflated language: "revolutionary".
- Removed promotional language: "robust and seamless", "effortlessly", "must-have".
- Removed generic conclusion.
- Flagged impossible absolute: "perfect accuracy".

## Fact Decisions

| Claim | Decision | Evidence handling |
| --- | --- | --- |
| Host agent performs the semantic rewrite | Kept | Supported by `evidence.md` |
| Uses user-provided samples and evidence | Kept | Supported by `evidence.md` |
| Checks every claim against public sources with perfect accuracy | Rewritten | Evidence says review is conservative and does not guarantee perfect accuracy |

## Final Rewrite

`humanize-skill` is an agent workflow for rewriting AI-looking drafts.

Codex or Claude does the edit; the skill gives it a process for voice matching, AI-pattern cleanup, and claim review.

Use it with pasted drafts, writing samples, selected local files, exports, evidence files, or authorized connectors. The fact-check pass starts with provided evidence and can use search when the host has it. It is a review step, not a promise of perfect accuracy.

## Final Audit

- Removed all CLI/package claims from the final text.
- Preserved the core behavior: rewrite, voice matching, AI-pattern cleanup, claim review.
- Replaced perfect-accuracy language with a bounded review-step claim.
