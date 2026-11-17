## Description:

Helps users discover and install agent skills when they ask questions like "how do I do X", "find a skill for X", "is there a skill that can...", or express interest in extending capabilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[penglovemeng](https://clawhub.ai/user/penglovemeng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to identify installable skills for a task, present relevant options, and optionally prepare skill installation commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can recommend unpinned external package commands and global installs that skip confirmation.

Mitigation: Prefer pinned CLI and package versions, review each skill source before installation, avoid `-g` and `-y` by default, and require explicit approval before any install or update.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/penglovemeng/skills/peng-find-skills)
- [Skills directory](https://skills.sh/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend external skill package commands; installs and updates should require explicit user approval.]

## Skill Version(s):

0.1.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
