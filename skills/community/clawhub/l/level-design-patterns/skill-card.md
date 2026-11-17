## Description:

Helps agents create Unity game scenes and prototypes by guiding level design workflows and Unity Editor automation for terrain, lighting, environment setup, and player controllers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cryptorabea](https://clawhub.ai/user/cryptorabea)

### License/Terms of Use:


## Use Case:

Developers and technical artists use this skill to rapidly prototype Unity scenes and automate common level setup tasks such as terrain generation, lighting, environment placement, and player controller creation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unity Editor menu commands can remove or overwrite scene work such as lights, reflection probes, baked lighting, Player objects, and terrain data without a confirmation dialog or reliable Undo support.

Mitigation: Review the generated Unity changes before applying them, and run the scripts first in a disposable scene or a version-controlled branch with project backups available.

## Reference(s):

- [Unity Level Design API Reference](artifact/references/unity-apis.md)
- [Level Design Best Practices](artifact/references/level-design-patterns.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, configuration]

**Output Format:** [Markdown guidance with C# Unity Editor script examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Unity Editor workflow steps and code intended for review before use in a project.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
