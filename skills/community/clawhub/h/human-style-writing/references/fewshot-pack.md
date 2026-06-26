# Building a Few-shot Pack to make LLM outputs more human

## Goal
Create a reusable set of examples that teaches a model your target voice/register without changing model weights.

## Steps
1) Pick a single target: e.g., "CN workplace email", "EN casual text", "news brief".
2) Collect 10–30 human samples (remove sensitive info).
3) Derive a **Style Card** (5–10 bullets).
4) Create 3–8 few-shot pairs:
   - Input: bullet facts + audience + constraints
   - Output: final message/article
5) Add a rubric from `human-checklist.md`.
6) Iterate: keep the best-performing examples; delete confusing ones.

## Few-shot template
**Instruction:** Write in the following style card: [..]

**Example 1**
Input:
- Audience:
- Context:
- Facts:
- Ask:
Constraints:
Output:
[final]

(Repeat)

## Notes
- Include at least one hard case: apology, refusal, negotiation, uncertainty.
- For bilingual: keep one-language-per-example unless code-switching is desired.
