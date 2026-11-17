## Description:

MagBox is a local dropbox between a human and an agent, moving files through two local directories with browser views.

This skill is ready for commercial/non-commercial use.

## Publisher:

[highnoonoffice](https://clawhub.ai/user/highnoonoffice)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and agent users use MagBox to exchange non-sensitive files between a human browser and an agent machine when chat is awkward for file handoffs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Anyone who can reach the MagBox port can read served files and upload into the inbox.

Mitigation: Keep the default loopback binding unless LAN access is intentionally needed; do not forward the raw port to the internet or use it on public or shared networks.

Risk: Sensitive files placed in the inbox or outbox can be exposed through the local browser-accessible file bridge.

Mitigation: Keep credentials, private records, and confidential documents outside both served directories and use an approved private channel for sensitive handoffs.

Risk: Service templates can keep the unauthenticated file bridge running across sessions.

Mitigation: Install a service only when persistent access is intended, run it as the directory owner rather than root, and use owner-controlled storage directories.

## Reference(s):

- [MagBox README](README.md)
- [MagBox Deployment](references/deploy.md)
- [Validation Record](references/validation.md)
- [ClawHub Skill Page](https://clawhub.ai/highnoonoffice/skills/magbox)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, local URLs, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include localhost or private-network URLs and filesystem paths; no external service output is produced.]

## Skill Version(s):

0.2.1 (source: server release evidence; artifact frontmatter and README say 0.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
