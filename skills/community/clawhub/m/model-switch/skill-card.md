## Description:

Helps OpenClaw users switch, add, compare, and diagnose AI model configurations across agent defaults, model allowlists, and auth profiles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samsonvacity](https://clawhub.ai/user/samsonvacity)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers using OpenClaw use this skill to switch active models, update model defaults, add provider models, compare model profiles, and diagnose provider/API-key configuration problems.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist provider API keys into local OpenClaw configuration and agent auth-profile JSON files.

Mitigation: Use least-privilege API keys, back up ~/.openclaw before running add-key or switch commands, verify file permissions afterward, and rotate keys if those files may have been exposed.

Risk: The skill can change OpenClaw model defaults, agent model selections, and model allowlists.

Mitigation: Review the target provider/model before execution, run diagnostic or listing commands first when possible, and keep a backup of OpenClaw configuration so model settings can be restored.

## Reference(s):

- [ClawHub Model Switch Skill Page](https://clawhub.ai/samsonvacity/skills/model-switch)
- [OpenClaw Project](https://github.com/openclaw/openclaw)
- [Matt Pocock Skills](https://github.com/mattpocock/skills)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and configuration-change instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local OpenClaw JSON configuration changes and shell commands that affect model defaults and provider authentication profiles.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
