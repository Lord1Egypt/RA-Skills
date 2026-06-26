## Description: <br>
Provides local, real-time conversation analysis that helps an agent monitor goal alignment, confidence boundaries, drift, capability limits, and session quality. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jcools1977](https://clawhub.ai/user/jcools1977) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to add local self-monitoring that can flag goal drift, uncertainty, capability-boundary issues, and declining session quality during active conversations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill's confidence, drift, and quality scores are heuristic and may incorrectly flag or miss issues. <br>
Mitigation: Treat alerts as decision support and review important recommendations against authoritative sources before acting. <br>
Risk: Always-on local analysis may change how the agent responds when thresholds fire. <br>
Mitigation: Enable it only where active self-monitoring is desired, and keep diagnostic output visible only when alerts fire or a user requests it. <br>
Risk: Future telemetry aggregation could expose conversation content or behavioral signals if added without controls. <br>
Mitigation: Do not enable telemetry aggregation without explicit consent, data minimization, retention limits, and privacy controls. <br>


## Reference(s): <br>
- [The Proprioceptive Model - Technical Deep Dive](references/proprioceptive-model.md) <br>
- [ClawHub Proprioception release page](https://clawhub.ai/jcools1977/proprioception) <br>
- [jcools1977 publisher profile](https://clawhub.ai/user/jcools1977) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, text, shell commands, guidance] <br>
**Output Format:** [JSON scores and alerts, with optional terminal text dashboard or brief annotation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local Node.js; evidence indicates no external API calls, credential access, network transfer, or durable storage.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
