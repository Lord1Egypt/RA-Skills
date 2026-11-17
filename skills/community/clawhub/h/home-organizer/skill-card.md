## Description:

Home Organizer provides home organization guidance for decluttering, storage planning, room organization, seasonal cleanup, moving checklists, and minimalist living.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain3](https://clawhub.ai/user/bytesagain3)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to get concise home organization tips, decluttering decisions, room-specific checklists, and simple local entry management for home tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Personal home notes may be stored persistently in plaintext under the user's local data directory.

Mitigation: Avoid storing sensitive addresses, schedules, or personal notes; set HOME_ORGANIZER_DIR to a controlled location and review file permissions before use.

Risk: The remove command reports deletion without removing matching records from the stored data file.

Mitigation: Verify data.log manually after removal attempts, and delete or purge stored records directly until real deletion behavior is documented and implemented.

Risk: The package has a suspicious security verdict from the authoritative server scan.

Mitigation: Review the skill and its local storage behavior before installing or running it in a workflow.

## Reference(s):

- [Home Organizer on ClawHub](https://clawhub.ai/bytesagain3/skills/home-organizer)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Plain text and Markdown-style checklists printed to stdout]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some commands may read from or write to local data files under the configured home-organizer data directory.]

## Skill Version(s):

2.0.0 (source: frontmatter and server evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
