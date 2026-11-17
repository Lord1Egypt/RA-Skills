## Description:

mymind (mymind.com). Use this skill for ANY mymind request — reading, creating, updating, and deleting data. Whenever a task involves mymind, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using mymind can search and read saved items, spaces, tags, links, and content, or manage that information through an OOMOL-connected account. The skill also supports creating and updating items and spaces, with approval checks for changes and deletions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may run changeable downloaded installation code, and the remote installers and hosted backend were not verified.

Mitigation: Review and approve CLI installation separately, using a verified release instead of automatically executing fallback scripts.

Risk: Automatic installation and synchronization of other agent skills may affect the environment.

Mitigation: Check whether synchronization is acceptable; use OO_SKILLS_SYNC_DISABLED as a control where needed.

Risk: Write and destructive actions can change or remove mymind data.

Mitigation: Keep the skill's explicit approval checks for changes and deletions.

## Reference(s):

- [mymind](https://mymind.com)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [Connector responses as JSON; retrieved item content may be Markdown or text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results vary by the selected mymind action.]

## Skill Version(s):

1.0.6 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
