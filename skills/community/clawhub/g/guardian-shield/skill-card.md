## Description: <br>
Locally scans untrusted text and documents to detect prompt injection, jailbreak, exfiltration, social engineering, and code execution threats before an agent processes the content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jtil4201](https://clawhub.ai/user/jtil4201) <br>

### License/Terms of Use: <br>
Source-available <br>


## Use Case: <br>
Developers and agent operators use Guardian Shield to scan untrusted messages, web-fetch results, pasted content, and documents before passing them to an OpenClaw agent. It returns a clean, suspicious, or threat verdict with score and category details so the agent can warn, block, or continue according to local policy. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: False positives can occur on security research text or examples that contain jailbreak or prompt-injection language. <br>
Mitigation: Review suspicious results before blocking critical workflows and tune config.json thresholds for the deployment context. <br>
Risk: Optional Python dependencies affect coverage for ML, PDF, and HTML scanning. <br>
Mitigation: Pin and install required optional dependencies in the target environment when those scanning modes are needed. <br>
Risk: The bundled attack phrases are detection data and should not be treated as operational instructions. <br>
Mitigation: Use evidence.security as the authoritative security source and keep the phrases isolated as scanner patterns. <br>


## Reference(s): <br>
- [Guardian Shield README](artifact/README.md) <br>
- [Guardian Shield skill instructions](artifact/SKILL.md) <br>
- [Guardian Shield ClawHub listing](https://clawhub.ai/jtil4201/guardian-shield) <br>
- [Fallen Angel Systems](https://fallenangelsystems.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, code, configuration, guidance] <br>
**Output Format:** [Terminal text or JSON scan results, with Markdown usage guidance and Python API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scores content from 0 to 100 and classifies results as clean, suspicious, or threat.] <br>

## Skill Version(s): <br>
1.1.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
