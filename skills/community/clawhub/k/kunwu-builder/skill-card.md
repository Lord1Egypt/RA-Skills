## Description:

Controls the Kunwu Builder industrial simulation software HTTP API for model management, robot control, logistics equipment, cameras, sensors, scenes, and behavior configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samwlh](https://clawhub.ai/user/samwlh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation engineers use this skill to control a trusted Kunwu Builder industrial simulation instance through HTTP API calls for scene and model management, robot and equipment control, sensor/camera operations, and behavior configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can control a real Kunwu Builder scene through HTTP endpoints and includes unsafe remote defaults.

Mitigation: Install only for a trusted, isolated Kunwu Builder instance; set KUNWU_API_URL explicitly and avoid hardcoded remote API defaults.

Risk: Scene reset, delete, export, batch execution, robot/equipment movement, and cloud model-loading actions can alter or destroy shared work.

Mitigation: Require manual confirmation and backups before destructive or high-impact actions, and do not run destructive test scripts on shared or production scenes.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/samwlh/skills/kunwu-builder)
- [Skill Usage Guide](artifact/SKILL_USAGE.md)
- [Kunwu Builder API Reference](artifact/api-reference.md)
- [Export Guide](artifact/EXPORT-GUIDE.md)
- [Industrial Patterns](artifact/INDUSTRIAL-PATTERNS.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON payload examples, shell commands, and JavaScript helper code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are intended for an agent controlling a trusted Kunwu Builder HTTP API endpoint.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
