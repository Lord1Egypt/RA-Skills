## Description:

List directory contents with detailed file information. Use for browsing files, checking permissions, and examining directory structure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to inspect accessible project directories, compare file details, and check file size information while working in a filesystem.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can reveal directory names and file sizes for paths the agent can access.

Mitigation: Use it on intended project folders and avoid running it over sensitive home, credential, or system directories.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dinghaibin/skills/ls-tool)

## Skill Output:

**Output Type(s):** [Text, Shell commands]

**Output Format:** [Plain text directory listings and Markdown command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include file names and file sizes for paths the agent can access.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
