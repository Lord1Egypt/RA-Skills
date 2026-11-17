## Description:

Enables autonomous agents to store, retrieve, and recall long-term, durable memory fragments and state across independent sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ndp](https://clawhub.ai/user/ndp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Memory Vault to persist durable notes, compact summaries, preferences, and execution state so autonomous agents can recall context across independent sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agent memory is stored in the provider's cloud service and may contain sensitive context if users send it.

Mitigation: Use only after reviewing the provider's retention, deletion, and access-control practices; do not store credentials, tokens, regulated data, private prompts, or sensitive project material unless approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ndp/skills/ndpsoftware-memory-vault)
- [Memory Vault service endpoint](https://memory-vault.ndpsoftware.com)

## Skill Output:

**Output Type(s):** [text, configuration, guidance]

**Output Format:** [Markdown guidance with endpoint and authentication configuration details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports persistent cloud memory for logs, vector fragments, notes, preferences, summaries, and state recall.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
