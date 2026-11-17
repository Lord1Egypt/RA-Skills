## Description:

Converts a GitHub open-source project into an OpenClaw skill package and guides publishing it to ClawHub.

This skill is ready for commercial/non-commercial use.

## Publisher:

[antonia-sz](https://clawhub.ai/user/antonia-sz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill publishers use this skill to turn suitable GitHub projects into OpenClaw skills, including README analysis, duplicate checks, SKILL.md drafting, release metadata preparation, publishing, and basic error handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles ClawHub tokens during publishing workflows.

Mitigation: Use a least-privileged temporary token, avoid pasting long-lived or broad-scope tokens into chat, and rotate or revoke the token after use.

Risk: The skill can publish content remotely to ClawHub.

Mitigation: Require an explicit GitHub-to-ClawHub publishing request and a final confirmation before publishing.

Risk: The artifact documents a workaround that patches a system-wide ClawHub CLI file and auto-accepts license terms.

Mitigation: Do not allow the skill to patch /usr/local/lib or auto-accept license terms; prefer an official CLI update or a reviewed local fix.

Risk: The security verdict is suspicious because safeguards around remote publishing, token handling, and CLI patching are insufficient.

Mitigation: Review before installing, use a dedicated workspace, and scan generated skill files before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/antonia-sz/skills/github-to-clawhub)
- [Publisher profile](https://clawhub.ai/user/antonia-sz)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and generated SKILL.md content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include publishing status, slug, release URL, and remediation guidance for common ClawHub CLI errors.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
