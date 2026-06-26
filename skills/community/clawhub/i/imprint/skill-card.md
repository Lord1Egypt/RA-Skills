## Description: <br>
Adaptive operator modeling for AI agents. Your agent learns who you are by watching, not by being told, and builds a predictive model of your preferences, patterns, and decision style across sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TheShadowRose](https://clawhub.ai/user/TheShadowRose) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use Imprint to let an OpenClaw-style agent build and maintain a local behavioral profile from derived interaction signals, then adapt communication, context loading, and prediction behavior over time. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill intentionally builds a local profile of the user's work style, which is privacy-sensitive. <br>
Mitigation: Use it only in workspaces where this behavior is expected, keep observations to derived behavioral signals, and periodically review, delete, or reset imprint/operator-model.json and imprint/observations/. <br>
Risk: Shared workspaces can expose operator-model data to other collaborators or agents with workspace access. <br>
Mitigation: Avoid shared workspaces unless everyone understands the profiling behavior, and keep the model local to the workspace with no network/API pre-fetching. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/TheShadowRose/imprint) <br>
- [Publisher profile](https://clawhub.ai/user/TheShadowRose) <br>
- [Implementation guide](artifact/imprint.md) <br>
- [Operator model schema](artifact/operator-model-schema.json) <br>
- [Example operator model](artifact/example-model.json) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, Markdown, JSON] <br>
**Output Format:** [Markdown instructions with JSON schema and example model files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local workspace guidance for maintaining imprint/operator-model.json and imprint/observations/ without network access.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
