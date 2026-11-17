## Description:

Generate Unreal Engine material node graphs from natural language descriptions, supporting nodes such as TextureSample, Multiply, Lerp, Constant, TexCoord, and MaterialOutput.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tianheihei002](https://clawhub.ai/user/tianheihei002)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical artists use this skill to describe Unreal Engine material effects in natural language and obtain a material node graph structure they can inspect, modify, or adapt.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact includes a plaintext MiniMax API key, which should be treated as compromised.

Mitigation: Revoke and rotate the key before reuse, then move provider credentials to environment variables or a secret manager.

Risk: A deployed app that calls an external model provider can expose credentials or create uncontrolled usage if secrets are kept client-side.

Mitigation: Keep provider credentials server-side and add rate limits, monitoring, and user controls before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tianheihei002/skills/material-generator)
- [Deployed Material Generator app](https://k2lucelsen19.space.minimaxi.com)
- [Example blood post-process material JSON](https://k2lucelsen19.space.minimaxi.com/BP_BloodPostProcess.json)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance, Configuration]

**Output Format:** [Markdown guidance with JSON material graph examples and linked app resources]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Material graphs may include Unreal Engine material nodes, pins, colors, and layout-oriented node metadata.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
