## Description:

Short.io (short.io). Use this skill for ANY Short.io request — reading, creating, updating, and deleting data. Whenever a task involves Short.io, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People managing Short.io links use this skill to inspect domains, retrieve links and click statistics, and create, update, or delete links through their connected Short.io account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup directs automatic execution of remote CLI installers without a separate approval or integrity check.

Mitigation: Review the installer separately, prefer a reviewed version-pinned installation, and check whether setup changes other installed agent skills.

Risk: Short.io access is mediated by OOMOL, and link creation, updates, and deletions can change account data.

Mitigation: Retain the skill's explicit approval requirements for write and destructive actions.

## Reference(s):

- [Short.io API documentation](https://developers.short.io/reference)
- [Short.io](https://short.io)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [Shell commands, API calls, JSON, Guidance]

**Output Format:** [Shell commands with JSON payloads and JSON responses, accompanied by Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Consult the live action schema before building payloads; confirm write actions and explicitly approve destructive actions.]

## Skill Version(s):

1.0.5 (source: frontmatter; server-resolved release 1.0.5)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
