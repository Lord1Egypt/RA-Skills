## Description:

Search and analyze email issue threads from a local knowledge base so agents can find similar past bugs, incidents, fixes, and root-cause patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[petrguan](https://clawhub.ai/user/petrguan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and support engineers use MailWise to search local EML archives for similar past issues, inspect relevant threads, and synthesize debugging guidance from previous resolutions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing an unpinned package or untrusted release can introduce ordinary supply-chain risk.

Mitigation: Install MailWise only from a trusted source or pinned version approved for the environment.

Risk: Indexing broad email archives can expose sensitive or unauthorized content in agent context.

Mitigation: Index only approved email archives and avoid displaying full threads in shared contexts.

Risk: The analyze workflow sends selected email excerpts to Anthropic through Claude Code CLI.

Mitigation: Use analyze only when the organization's data policy permits sending those excerpts to Anthropic.

## Reference(s):

- [MailWise Command Reference](artifact/reference.md)
- [MailWise ClawHub Page](https://clawhub.ai/petrguan/skills/mailwise)
- [Claude Code CLI Documentation](https://docs.anthropic.com/en/docs/claude-code)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands and CLI output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local search and thread commands can include email excerpts; analyze produces Claude-generated synthesis from selected matching threads.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
