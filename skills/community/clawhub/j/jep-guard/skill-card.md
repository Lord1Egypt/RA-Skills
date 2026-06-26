## Description: <br>
JEP Guard intercepts high-risk OpenClaw skill actions, asks for confirmation when needed, issues temporary tokens, and records audit events for traceability. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[schchit](https://clawhub.ai/user/schchit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and teams using OpenClaw skills use JEP Guard to gate risky skill execution, trace cross-skill delegation, and export audit evidence for security or compliance review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scanner verdict is suspicious because installation behavior and local execution-data sharing are sensitive for a security module that observes and gates OpenClaw skill executions. <br>
Mitigation: Install only when that monitoring role is intended; start in passive mode, review ~/.jep-guard/config.json, and enable full mode only after accepting local command-metadata logging and runtime hooks. <br>
Risk: Full-protection mode can intercept skill execution, write audit data, and rely on a persistent local daemon. <br>
Mitigation: Require explicit consent, keep daemon startup manual, and verify audit retention and local file permissions before using full mode in shared or compliance-sensitive environments. <br>
Risk: The release advertises wallet and sensitive-credential capability tags, so workflows may involve high-impact credentials or assets. <br>
Mitigation: Use least-privilege credentials, confirm risky operations interactively, and inspect audit receipts before trusting automated delegation chains. <br>


## Reference(s): <br>
- [JEP Guard on ClawHub](https://clawhub.ai/schchit/jep-guard) <br>
- [IETF JEP Draft](https://datatracker.ietf.org/doc/draft-wang-jep/) <br>
- [IETF JAC Draft](https://datatracker.ietf.org/doc/draft-wang-jac/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command examples and local configuration details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local audit logs, guard tokens, status output, and exportable JEP audit receipts when configured and run.] <br>

## Skill Version(s): <br>
2.0.4 (source: server-resolved release metadata, skill.yaml, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
