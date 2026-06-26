## Description: <br>
Register, track, and validate state observations against declared constraints without assuming universal truth or enforcing physical laws. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[uniaolives](https://clawhub.ai/user/uniaolives) <br>

### License/Terms of Use: <br>
CC0 1.0 Universal (Public Domain) <br>


## Use Case: <br>
Developers and AI system designers use this skill as a reference protocol and implementation guide for registering observations, declaring constraints, recording non-blocking violations, projecting state, and exporting audit traces. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Exported traces can include sensitive coordinates, observer identifiers, or user-supplied metadata. <br>
Mitigation: Avoid putting secrets, private identifiers, or sensitive operational details in metadata unless redaction and access controls are added. <br>
Risk: The release is a reference protocol, not a complete secure audit system, and traces should not be treated as tamper-proof by default. <br>
Mitigation: Use checksum or signature verification before relying on exported traces for integrity-sensitive workflows. <br>


## Reference(s): <br>
- [CS-RV Protocol Whitepaper](artifact/CS-RV_Protocol_Whitepaper.md) <br>
- [CS-RV Implementation Guide](artifact/skills.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Guidance] <br>
**Output Format:** [Markdown documents with Python reference code blocks and protocol guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include JSON audit-trace examples; exported traces can contain user-supplied metadata.] <br>

## Skill Version(s): <br>
7.7.7 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
