## Description:

Manage Helmet library accounts in the Helsinki capital region from an AI agent, including renewals, holds, fines, catalog search, and family account summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vijaykodam](https://clawhub.ai/user/vijaykodam)

### License/Terms of Use:

MIT-0

## Use Case:

External users and their agents use this skill to inspect and manage Helmet library accounts, including loans, holds, fines, catalog searches, and multi-profile family summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs an unpinned npm CLI that handles library card numbers, PINs, and session cookies locally.

Mitigation: Install only when the publisher and npm package are trusted, prefer a reviewed pinned version when available, and protect the local Helmet configuration and session files.

Risk: The skill can guide renewals and hold changes that affect a user's library account.

Mitigation: Review commands before execution and require explicit profile selection for destructive or state-changing operations when multiple profiles are saved.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/vijaykodam/skills/helmet)
- [@helmet-ai/helmet npm package](https://www.npmjs.com/package/@helmet-ai/helmet)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command output expectations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the helmet CLI with --json for machine-readable account data; state-changing actions require explicit profile selection when multiple profiles exist.]

## Skill Version(s):

0.3.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
