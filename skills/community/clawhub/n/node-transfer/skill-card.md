## Description:

High-speed, memory-efficient file transfer between OpenClaw nodes using Node.js native streams and token-secured HTTP streaming without Base64 encoding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eisonme](https://clawhub.ai/user/eisonme)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to deploy, verify, and run streamed file transfers between OpenClaw nodes while avoiding Base64 payload overhead and large in-memory file handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote deployment and installation checks can perform privileged operations on OpenClaw nodes.

Mitigation: Install only in trusted, controlled node environments and treat deploy.js and ensure-installed.js as privileged operations.

Risk: Plain HTTP streaming can expose transferred data on untrusted networks even when token-protected.

Mitigation: Avoid transferring sensitive files over untrusted networks and restrict sender exposure with firewall or interface controls.

Risk: Incorrect source or destination paths can transfer unintended files or write to the wrong location.

Mitigation: Validate source and destination paths before each transfer.

Risk: Security evidence notes unresolved PowerShell quoting and executable manifest issues.

Mitigation: Review and fix those deployment and manifest issues before relying on the skill in sensitive workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/eisonme/skills/node-transfer)
- [README](artifact/README.md)
- [Complete usage guide](artifact/SKILL.md)
- [Core integration proposal](artifact/CONTRIBUTING_PROPOSAL.md)
- [Investigation report](artifact/INVESTIGATION_REPORT.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline JavaScript, shell commands, PowerShell deployment scripts, and JSON status or transfer results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The artifact includes executable Node.js scripts that can emit JSON transfer metadata, progress updates, version checks, and generated deployment commands.]

## Skill Version(s):

1.0.0 (source: evidence release metadata, package.json, version.js)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
