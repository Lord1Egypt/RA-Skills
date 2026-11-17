## Description:

TinyFish (tinyfish.ai). Use this skill for ANY TinyFish request — reading, creating, updating, and deleting data. Whenever a task involves TinyFish, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to read and manage TinyFish data through an OOMOL-connected account, including search, research, URL fetching, browser automation, monitors, profiles, and vault connections.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup executes an unverified online installer, and broader changes to agent environments are not disclosed.

Mitigation: Review and install a verified CLI release yourself. Set OO_SKILLS_SYNC_DISABLED=1 to prevent startup writes to agent skill directories.

Risk: Some TinyFish actions change or remove account data, browser state, profiles, monitors, or payment settings.

Mitigation: Keep approval checks in place for browser actions, profile uploads, vault connections, monitors, and payments; confirm the exact target and effect before proceeding.

## Reference(s):

- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [TinyFish](https://tinyfish.ai)
- [TinyFish API documentation](https://docs.tinyfish.ai/)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Text, Guidance]

**Output Format:** [Markdown instructions with inline shell commands and JSON payloads; action results in JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action results may include data and execution metadata.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
