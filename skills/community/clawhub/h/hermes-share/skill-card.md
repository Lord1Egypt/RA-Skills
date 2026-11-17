## Description:

Share Hermes skills with other users by packaging skills as ZIP archives, sending them through messaging platforms, or creating temporary expiring download links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[almohalhel1408](https://clawhub.ai/user/almohalhel1408)

### License/Terms of Use:

MIT

## Use Case:

Developers and Hermes users use this skill to package, transfer, and install Hermes skills between agents without relying on ClawHub or GitHub for the transfer path.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Skill archives may be uploaded to public temporary file hosts.

Mitigation: Use temporary links only for intended recipients, avoid sharing sensitive or private skills, and delete or let links expire after transfer.

Risk: The receiving workflow installs downloaded archives by running shell code from the archive.

Mitigation: Install only from trusted senders; inspect the ZIP contents and install.sh before execution.

## Reference(s):

- [Hermes Share on ClawHub](https://clawhub.ai/almohalhel1408/skills/hermes-share)
- [Publisher Profile](https://clawhub.ai/user/almohalhel1408)
- [Bilingual Frontmatter](references/bilingual-frontmatter.md)
- [Delivery Platform Quirks](references/delivery-platform-quirks.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with bash commands plus generated ZIP archives and share messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local ZIP archives and temporary public download links when the agent executes the workflow.]

## Skill Version(s):

1.2.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
