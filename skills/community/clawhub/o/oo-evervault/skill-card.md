## Description:

Evervault (evervault.com). Use this skill for ANY Evervault request — reading, creating, and updating data. Whenever a task involves Evervault, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to encrypt or decrypt JSON-compatible values and inspect encrypted token metadata in Evervault through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup can run an external CLI installer that was not verified, and OOMOL-mediated operations use the connected Evervault account.

Mitigation: Review and approve CLI installation separately, including changes to installed agent skills. Prefer a verified, versioned CLI and do not allow automatic setup until the installer and connector are trusted.

## Reference(s):

- [Evervault](https://evervault.com)
- [Evervault API documentation](https://docs.evervault.com/api)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON action results with concise Markdown guidance and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results vary by selected Evervault action and the connected account.]

## Skill Version(s):

1.0.5 (source: SKILL.md frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
