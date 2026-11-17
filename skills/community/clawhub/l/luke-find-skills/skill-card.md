## Description:

Helps users discover and install agent skills when they ask questions like "how do I do X", "find a skill for X", "is there a skill that can...", or express interest in extending capabilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[banalit](https://clawhub.ai/user/banalit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to identify relevant installable skills for a task, compare options, and run Skills CLI search or install commands when they choose to extend an agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may suggest remote Skills CLI commands that install third-party skills globally or skip confirmation prompts.

Mitigation: Inspect the candidate skill source and publisher profile before installing, prefer pinned CLI or package versions, and avoid global unattended installs unless explicitly approved.

Risk: Broad user requests could be converted into skill searches or installs when the user only wanted direct help.

Mitigation: Use the skill only when the user explicitly wants to find, compare, or install skills, and confirm before running install or update commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/banalit/skills/luke-find-skills)
- [Skills CLI catalog](https://skills.sh/)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Markdown]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include install commands and links to skill catalog pages; users should review candidate skills before installing.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
