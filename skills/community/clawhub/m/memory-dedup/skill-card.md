## Description:

Automatically identify, merge, and clean duplicate or outdated entries in MEMORY.md to maintain concise, organized, and up-to-date information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weidadong2359](https://clawhub.ai/user/weidadong2359)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators maintaining persistent agent memory use this skill to preview and run MEMORY.md cleanup, merge similar sections, and reduce outdated or duplicate entries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can rewrite persistent MEMORY.md content by default with incomplete safeguards.

Mitigation: Run --dry-run first, use a copy or version-controlled MEMORY.md, and review the resulting changes before accepting them.

Risk: Unattended scheduled cleanup could merge or remove memory content without reliable review or rollback.

Mitigation: Do not enable the weekly cron workflow unless review, content preservation, and reliable rollback controls are added.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/weidadong2359/skills/memory-dedup)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files]

**Output Format:** [Markdown guidance with shell commands and a text cleanup report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can modify MEMORY.md and create a backup file when run without dry-run mode.]

## Skill Version(s):

1.0.0 (source: package.json and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
