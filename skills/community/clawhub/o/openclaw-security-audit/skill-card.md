## Description: <br>
Audit OpenClaw/Clawdbot deployments for misconfigurations and attack vectors. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[misirov](https://clawhub.ai/user/misirov) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to review OpenClaw, Clawdbot, or Moltbot environments for gateway exposure, unsafe tool policy, credential leakage, persistence risks, and hardening gaps. It produces a read-only audit report with findings, impact, and remediation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill inspects local system state, including logs, process listings, listener ports, and configuration paths. <br>
Mitigation: Install it only when you want an agent to perform local security inspection, and review proposed commands before approval. <br>
Risk: Security checks may encounter secrets or sensitive log data. <br>
Mitigation: Report only redacted summaries or file paths, and do not expose secret values in output. <br>
Risk: Remediation steps can change services, firewall rules, credentials, or permissions if the user asks for active fixes. <br>
Mitigation: Keep the workflow read-only by default and require explicit confirmation before proposing or running active remediation commands. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Terminal-style Markdown report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports OK, VULNERABLE, and UNKNOWN findings; redacts secrets; proposes active remediation only after explicit user approval.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
