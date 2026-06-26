## Description: <br>
Userflow (userflow.com) skill for reading, creating, updating, and deleting Userflow data through the oo CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to manage Userflow users, groups, and events through an OOMOL-connected Userflow account. It supports read actions, upserts, event tracking, and explicitly approved delete operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan flags install guidance that pipes a remotely fetched installer directly into a shell without pinning or verification. <br>
Mitigation: Review the installer first, prefer official pinned releases where available, and avoid use in sensitive environments until checksum- or signature-verified installation guidance is available. <br>
Risk: The skill can run write and destructive Userflow actions that alter or delete users and groups. <br>
Mitigation: Confirm the exact payload and effect before write actions, and require explicit approval for each destructive target before execution. <br>
Risk: The skill requires sensitive Userflow credentials through an OOMOL-connected account. <br>
Mitigation: Use only trusted OOMOL and Userflow connections, keep credentials out of prompts and local files, and revoke or rotate access if a connection is no longer needed. <br>


## Reference(s): <br>
- [Userflow homepage](https://userflow.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-userflow) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands call the oo CLI and may return JSON containing data and meta.executionId.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
