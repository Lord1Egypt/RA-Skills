## Description:

Provides Chinese-language behavior-pattern modules for agent reasoning, tool orchestration, long-context handling, prompt compression, safety checks, and expert routing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chen6896qqwee](https://clawhub.ai/user/chen6896qqwee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill as a local helper for composing reusable Python behavior patterns for reasoning, tool use, summarization, prompt compression, safety checks, and expert routing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The built-in safety guard may not redact or block secrets reliably.

Mitigation: Do not pass passwords, tokens, financial identifiers, or private documents to the skill.

Risk: Tool and subagent examples could be adapted into real external calls without adequate review.

Mitigation: Require explicit user approval and review before adapting examples into operational tool or subagent workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chen6896qqwee/skills/llm-behavior-distill)

## Skill Output:

**Output Type(s):** [text, code, guidance]

**Output Format:** [Markdown and Python code patterns]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local behavior modules return structured dictionaries, strings, and dataclass-style results.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
