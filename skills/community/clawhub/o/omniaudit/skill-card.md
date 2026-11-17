## Description:

OmniAudit scans OpenClaw skills, SKILL.md files, and code for prompt injection, credential theft, malware, reverse shells, and other threat patterns before installation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[legarams](https://clawhub.ai/user/legarams)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use OmniAudit to assess ClawHub/OpenClaw skills, shared code, GitHub raw files, and repository ZIPs before installation or execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local files, code snippets, ZIPs, or paid scans may send data to an external scanning service or incur cost.

Mitigation: Require explicit user approval before transmitting local content, scanning snippets or ZIPs, or initiating any paid scan.

Risk: Free public GitHub raw URL scans still contact an external service.

Mitigation: Notify the user before starting a public URL scan and respect a declined scan.

## Reference(s):

- [OmniAudit homepage](https://omniaudit.fly.dev)
- [ClawHub skill page](https://clawhub.ai/legarams/skills/omniaudit)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text security report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May involve external URL, code snippet, or ZIP scanning; paid scans require explicit user approval.]

## Skill Version(s):

1.0.4 (source: server release metadata; artifact frontmatter lists 1.0.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
