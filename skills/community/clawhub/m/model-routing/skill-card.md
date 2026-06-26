## Description: <br>
Automatically routes agent requests to an appropriate model based on task type, explicit model controls, cost caps, concurrency limits, and fallback behavior. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sam-k-migz](https://clawhub.ai/user/sam-k-migz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to apply consistent model-selection guidance for coding, reasoning, simple, and general requests while respecting explicit overrides and configured limits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Routing telemetry records task type, chosen model, and applied caps to an internal trace. <br>
Mitigation: Confirm that this limited routing metadata is acceptable for the deployment environment before installation. <br>
Risk: Automatic routing can affect cost, latency, and output quality if model selection or caps are misaligned with organizational needs. <br>
Mitigation: Respect explicit user, organization, channel, and session model locks first, and tune safety caps and the per-turn budget ceiling before broad use. <br>


## Reference(s): <br>
- [Model Routing Skill on ClawHub](https://clawhub.ai/sam-k-migz/model-routing) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration] <br>
**Output Format:** [Markdown instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only routing policy with lightweight telemetry fields, token caps, budget ceiling, concurrency limits, and downgrade-only fallbacks.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
