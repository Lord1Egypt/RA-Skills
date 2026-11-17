## Description:

Optimizes context window via MECW principles and memory tiering

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to assess context pressure and choose memory, compression, routing, or delegation strategies for long or complex agent tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Checkpoint examples using shared temporary paths may expose or collide with saved state.

Mitigation: Review checkpoint paths and use an isolated, access-restricted temporary location.

Risk: Sharing logs may expose sensitive information.

Mitigation: Review and redact sensitive information from logs before sharing them.

## Reference(s):

- [Project homepage](https://github.com/athola/claude-night-market/tree/master/plugins/conserve)
- [Anthropic prompt caching documentation](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)
- [vLLM automatic prefix caching documentation](https://docs.vllm.ai/en/stable/features/automatic_prefix_caching/)

## Skill Output:

**Output Type(s):** [Guidance, Analysis, Markdown, Code, Shell commands]

**Output Format:** [Markdown guidance with checklists and occasional code or command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommendations are tailored to the current task and context state.]

## Skill Version(s):

1.10.3 (source: artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
