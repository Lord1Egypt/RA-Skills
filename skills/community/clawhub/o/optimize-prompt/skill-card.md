## Description:

Optimizes, compresses, scores, and audits natural-language prompts for LLMs and agent workflows while preserving constraints and avoiding task execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[margaretzybgl](https://clawhub.ai/user/margaretzybgl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, prompt engineers, and agent builders use this skill to turn conversational or ambiguous requests into compact downstream-agent prompts with an audit ledger, validation status, and writing-quality feedback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing with a floating @latest command can pull a version different from the reviewed release.

Mitigation: Pin the ClawHub installer and install a specific skill version when using this release.

Risk: When integrated with a remote model provider, prompt text may be sent to that provider.

Mitigation: Avoid including secrets or sensitive data unless the provider setup is approved for that data.

Risk: Prompt rewriting can drop or alter execution-affecting constraints if validation is bypassed.

Mitigation: Use the skill's conservative fallback and review optimized_prompt before passing it to downstream tools.

## Reference(s):

- [Optimize Prompt on ClawHub](https://clawhub.ai/margaretzybgl/skills/optimize-prompt)
- [LLM Prompt Firewall related skill](https://clawhub.ai/margaretzybgl/skills/llm-prompt-firewall)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [JSON object containing an optimized prompt, audit ledger, validation status, confidence, and prompt-quality feedback.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The optimized_prompt field is the downstream instruction; Prompt IR is audit and debugging context only.]

## Skill Version(s):

0.1.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
