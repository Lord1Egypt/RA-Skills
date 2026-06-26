# llm-benchmark-analyst

This package is intentionally portable.

## Files for different runtimes
- `SKILL.md`: primary AgentSkills/OpenAI/OpenClaw entrypoint

## Important behavior
- benchmark scope is restricted to `references/benchmark-source.md`
- search is domain-first, then benchmark shortlist, then website retrieval
- reports always include benchmark purpose, variant, time point, and data-defect warnings
