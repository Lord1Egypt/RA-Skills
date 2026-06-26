## Description: <br>
Agent coordination layer via Workledger - shared work orders, claim/release leases, cross-machine memory sync, and handoff between OpenClaw instances. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ppiankov](https://clawhub.ai/user/ppiankov) <br>

### License/Terms of Use: <br>
BUSL-1.1 <br>


## Use Case: <br>
Developers and agent operators use this skill to coordinate multiple OpenClaw instances through shared work orders, leases, context sync, and handoff workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to install a remote Workledger binary into a system-wide location. <br>
Mitigation: Install only when the publisher is trusted, prefer a user-local bin directory, and verify checksums or signatures when available. <br>
Risk: Context sync can send sensitive project memory to the configured Workledger service. <br>
Mitigation: Review context before syncing and avoid storing secrets or confidential data in shared project memory. <br>
Risk: Work-order deletion is destructive. <br>
Mitigation: Confirm the work order should be permanently removed before running delete commands. <br>


## Reference(s): <br>
- [Hiveram service](https://hiveram.com) <br>
- [Workledger CLI distribution](https://github.com/ppiankov/hiveram-dist) <br>
- [ClawHub Hiveram release](https://clawhub.ai/ppiankov/hiveram) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the workledger CLI and a Workledger API key.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill footer) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
