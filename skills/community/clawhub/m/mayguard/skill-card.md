## Description: <br>
MayGuard audits agent skill directories for malicious patterns such as credential theft, suspicious network calls, and destructive commands before installation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[balkanblbn](https://clawhub.ai/user/balkanblbn) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use MayGuard to inspect downloaded skill directories before installation and identify suspicious static patterns such as credential access, outbound network calls, destructive commands, and obfuscation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A SAFE result is heuristic and may miss malicious behavior that is outside the configured static patterns. <br>
Mitigation: Treat scan results as advisory and review the target skill before deployment. <br>
Risk: Scanning broad private folders can expose local file names or contents in the generated findings. <br>
Mitigation: Run the scanner only against the specific downloaded skill directory intended for inspection. <br>


## Reference(s): <br>
- [Threat Patterns](references/threat_patterns.json) <br>
- [MayGuard on ClawHub](https://clawhub.ai/balkanblbn/mayguard) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, JSON, Shell commands, Guidance] <br>
**Output Format:** [Plain text audit report or JSON report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports status, risk score, and matched findings for a target skill directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
