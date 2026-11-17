## Description:

Persistent memory for OpenClaw agents. Exact recall in milliseconds - your agent remembers everything across sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lgrant1234](https://clawhub.ai/user/lgrant1234)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external OpenClaw users use this skill to give agents persistent local memory for recalling decisions, summaries, project state, snippets, files, and git history across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory can retain sensitive files, git history, raw conversation text, credentials, client data, personal data, or proprietary code.

Mitigation: Before importing content, verify where data is stored, define exclusions for sensitive material, and establish a process to review and delete retained memory.

Risk: Broad recall without clear scoping, consent, or retention controls can expose information beyond the user's intended context.

Mitigation: Use the skill only where long-term local memory is intentional, limit imported sources to approved project material, and periodically audit retained memory.

## Reference(s):

- [Grantai Memory ClawHub listing](https://clawhub.ai/lgrant1234/skills/grantai-memory)
- [GrantAi OpenClaw integration documentation](https://solonai.com/grantai/integrations/openclaw)
- [GrantAi download page](https://solonai.com/grantai/download)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text with inline code or configuration blocks when relevant]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include recalled memory, stored summaries, code snippets, project state, configuration guidance, and token savings status.]

## Skill Version(s):

1.3.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
