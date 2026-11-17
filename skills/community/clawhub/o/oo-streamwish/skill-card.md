## Description:

Operate StreamWish through an OOMOL-connected account to read, create, update, clone, and delete files and folders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

StreamWish account users use the skill to inspect account and storage details, list files and folders, retrieve file information and direct links, and manage their files through OOMOL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup directs execution of an unverified remote installer without a separate approval step.

Mitigation: Review setup first; install a verified CLI with approval and review any automatic agent-skill installation.

Risk: Write actions change StreamWish data, and deletion removes files.

Mitigation: Confirm the exact payload and effect before write actions, and obtain explicit approval for deletion.

## Reference(s):

- [StreamWish API documentation](https://streamwish.com/api.html)
- [StreamWish homepage](https://streamwish.com)
- [oo CLI documentation and source](https://github.com/oomol-lab/oo-cli)
- [StreamWish ClawHub release](https://clawhub.ai/oomol/skills/oo-streamwish)

## Skill Output:

**Output Type(s):** [JSON, Text, API Calls]

**Output Format:** [Structured JSON results with concise textual guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Write actions require confirmation; deletion requires explicit approval.]

## Skill Version(s):

1.0.2 (source: target metadata, release evidence, frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
