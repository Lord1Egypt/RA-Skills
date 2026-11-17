# Universal optimization profile

Use this profile for every rewrite. Provider overlays may refine it but must not weaken preservation or safety rules.

## Core rules

- Make the desired outcome, audience, and completion bar explicit.
- Preserve the original prompt's facts, variables, required artifact, language, format, and hard constraints.
- Remove duplicated rules and examples that do not demonstrate otherwise hard-to-describe behavior.
- Prefer positive, observable instructions. Keep prohibitions for real invariants and failure prevention.
- Separate instructions, context, examples, and user data when they could be confused.
- Define evidence boundaries for grounded tasks: what sources may be used, what needs support, and what to do when evidence is missing.
- Define autonomy boundaries for agents: safe reads, allowed local changes, approval-requiring actions, validation, fallback, and stop conditions.
- Define the exact output shape when downstream parsing or review depends on it.
- Avoid requesting hidden reasoning. Ask for an answer, brief rationale, citations, calculations, checks, or a verifiable artifact.
- Keep the prompt no longer than required to change behavior.

## Preservation priority

When shortening, preserve in this order:

1. Goal and requested artifact.
2. Facts, explicit values, variables, and source material.
3. Safety, privacy, business, evidence, and permission boundaries.
4. Success criteria, required output, and validation.
5. Tone and optional process preferences.

## Generic complex-prompt skeleton

Use only relevant sections:

```text
Role: [function and necessary context]
Goal: [user-visible outcome]
Success criteria: [conditions the result must satisfy]
Inputs: [data, sources, variables, and trust boundaries]
Constraints: [policy, evidence, scope, and side-effect limits]
Tools: [available tools, routing, and failure behavior]
Output: [format, required fields, language, and length]
Validation: [checks before completion]
Stop rules: [ask, retry, fallback, abstain, or finish]
```

## Official cross-provider sources

- OpenAI GPT-5.6 prompt guidance: https://developers.openai.com/api/docs/guides/prompt-guidance-gpt-5p6
- Anthropic prompt engineering overview: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview
- Google prompt design strategies: https://ai.google.dev/gemini-api/docs/prompting-strategies
- Kimi prompt best practices: https://platform.moonshot.ai/docs/guide/prompt-best-practice

