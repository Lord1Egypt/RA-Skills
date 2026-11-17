## Description:

Turn a plain-language request into an importable iOS .shortcut file by preparing a recipe, building it, self-signing it, and providing delivery guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wukong-a](https://clawhub.ai/user/wukong-a)

### License/Terms of Use:

MIT

## Use Case:

Developers and iOS users can turn a plain-language automation request into a JSON recipe and an importable iPhone Shortcut, with setup and delivery instructions. The skill also explains when a shortcut needs a separate trigger configured on the device.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented file-sharing workflow may expose private certificate keys if the project directory is served or shared.

Mitigation: Keep certificate keys outside shared directories and do not serve or share the project directory; distribute only intended output files.

Risk: Installing the generated root certificate and enabling full trust is a lasting, broad device trust change.

Mitigation: Avoid installation until the delivery workflow and packaged signing executable have been independently reviewed, and proceed only if the device trust change is accepted.

Risk: The security inspection was partial and did not inspect the packaged signing executable.

Mitigation: Have the packaged executable and delivery workflow independently reviewed before use.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/wukong-a/skills/ios-shortcut-builder)
- [Action reference](references/actions.md)

## Skill Output:

**Output Type(s):** [Files, JSON, Shell commands, Guidance]

**Output Format:** [Importable .shortcut files, JSON recipes, and Markdown setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Signing requires Linux x86-64; first-time import requires installing and trusting a user-generated root certificate on the iPhone.]

## Skill Version(s):

2.0.0 (source: frontmatter, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
