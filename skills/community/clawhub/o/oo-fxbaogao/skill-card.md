## Description:

Fxbaogao (fxbaogao.com). Use this skill for ANY Fxbaogao request — searching and reading data. Whenever a task involves Fxbaogao, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using an OOMOL-connected Fxbaogao account can search research reports by keywords, institutions, and publication time, then retrieve report summaries, matching paragraphs, or PDF download URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute changing remote code without asking for approval.

Mitigation: Install a reviewed, fixed CLI release separately and require approval for installation changes. Consider disabling startup skill synchronization with OO_SKILLS_SYNC_DISABLED=1, as documented in the CLI reference.

## Reference(s):

- [Fxbaogao homepage](https://www.fxbaogao.com/)
- [Fxbaogao agent interface documentation](https://www.fxbaogao.com/agent-interface)
- [oo CLI repository and documentation](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [API Calls, Text, Guidance]

**Output Format:** [JSON report data with concise textual summaries and guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only report search and retrieval; requires the oo CLI and an existing Fxbaogao connection.]

## Skill Version(s):

1.0.2 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
