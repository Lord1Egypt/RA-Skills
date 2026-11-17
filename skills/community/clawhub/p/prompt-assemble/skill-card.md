## Description:

Prompt Safe helps agents assemble prompts with optional memory retrieval, context construction, token estimation, and a memory safety valve to reduce token-overflow risk.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexunitario-sketch](https://clawhub.ai/user/alexunitario-sketch)

### License/Terms of Use:


## Use Case:

Developers and agent builders use this skill to construct LLM prompts that include recent dialog and optional retrieved memories while applying token-budget checks before the final prompt is sent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release claims strong token-overflow protection, but the evidence states its guarantees are stronger than the implementation supports.

Mitigation: Treat it as a starter implementation, replace heuristic token checks with model-appropriate token counting, and enforce a final hard limit immediately before the LLM call.

Risk: Retrieved memories may contain untrusted or instruction-like content that could influence prompt behavior.

Mitigation: Wrap retrieved memories as untrusted reference data and keep the memory layer discardable under the safety valve.

## Reference(s):

- [Memory Data Standards](references/memory_standards.md)
- [Token Estimation Strategies](references/token_estimation.md)
- [ClawHub Skill Page](https://clawhub.ai/alexunitario-sketch/skills/prompt-assemble)
- [Publisher Profile](https://clawhub.ai/user/alexunitario-sketch)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python code examples and generated prompt strings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses configurable model token limits, safety margins, memory retrieval count, and memory summary length; token counts are heuristic unless replaced with a model-specific tokenizer.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
