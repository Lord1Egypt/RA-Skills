## Description: <br>
Scans source code for WebSocket-specific security issues including plaintext connections, missing Origin validation, unauthenticated accepts, missing size and rate limits, unsafe broadcasts, reflected message relay, error leaks, subprotocol issues, and missing heartbeat or timeout handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PHY041](https://clawhub.ai/user/PHY041) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security engineers use this skill to audit WebSocket server code for known vulnerability patterns and receive findings with suggested fixes before release or in CI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scan results may include matched source snippets from the audited project. <br>
Mitigation: Run the scanner against a specific project folder and review the output before sharing results outside the project team. <br>


## Reference(s): <br>
- [Canlah AI Homepage](https://canlah.ai) <br>
- [ClawHub Skill Page](https://clawhub.ai/PHY041/phy-websocket-audit) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown-style security findings with code snippets and suggested shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can run in CI mode with a minimum-severity fail gate.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
