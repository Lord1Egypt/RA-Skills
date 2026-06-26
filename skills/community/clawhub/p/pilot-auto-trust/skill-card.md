## Description: <br>
Automatic trust management with configurable policies for Pilot Protocol agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to list Pilot Protocol trust requests and generate policy-based shell commands for approving or rejecting known agents, networks, or reputation thresholds. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automate bulk trust approvals or rejections without sufficient review controls. <br>
Mitigation: List pending requests first, confirm the active Pilot daemon and profile, and keep an audit and revocation path before applying approve or reject pipelines. <br>
Risk: Score, hostname, or network-prefix heuristics can trust the wrong agent when identities are unknown or potentially malicious. <br>
Mitigation: Prefer verified allowlists or cryptographic identity checks, and require manual review for unknown agents or fine-grained trust decisions. <br>


## Reference(s): <br>
- [Pilot Protocol](https://pilotprotocol.network) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with bash command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires pilotctl and jq; commands can approve or reject pending trust requests.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
