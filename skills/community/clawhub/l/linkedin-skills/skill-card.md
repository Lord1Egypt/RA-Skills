## Description:

LinkedIn automation skill collection that supports authentication, content publishing, feed browsing, search and discovery, social interactions, and compound operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ceoqveda](https://clawhub.ai/user/ceoqveda)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to let an agent operate LinkedIn through a local CLI and browser extension for posting, browsing, profile research, engagement, and lead-generation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local bridge can give agent-driven commands access to a logged-in LinkedIn browser session while it is active.

Mitigation: Use only in a trusted local environment, avoid sensitive Chrome profiles, and stop the bridge when the workflow is complete.

Risk: LinkedIn publishing, commenting, connection, and messaging actions operate through the user's real account.

Mitigation: Require explicit user confirmation before these actions and show the exact content or target before execution.

Risk: Aggressive automation may trigger LinkedIn rate limits or account restrictions.

Mitigation: Keep operation frequency reasonable, add delays for batch workflows, and avoid mass or repetitive outreach.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ceoqveda/skills/linkedin-skills)
- [README.md](README.md)
- [SKILL.md](SKILL.md)
- [Chrome extension manifest](extension/manifest.json)
- [uv documentation](https://docs.astral.sh/uv/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON CLI output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The underlying CLI emits JSON to stdout; agent responses should summarize that output for the user.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
