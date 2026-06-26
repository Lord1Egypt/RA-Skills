## Description: <br>
Manages sensitive data access by marking resources with privacy levels and enforcing share, export, display, and internal-use restrictions through a local registry. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaobu2020](https://clawhub.ai/user/xiaobu2020) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to label local resources by privacy level, check whether a planned action is allowed, and review audit records before data is shared or exported. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Registry and audit files can reveal sensitive file names, privacy categories, reasons, and access decisions. <br>
Mitigation: Store the registry and audit log locally with access limited to trusted users and agents. <br>
Risk: Incorrect or stale privacy labels can allow an agent to make the wrong share, export, display, or internal-use decision. <br>
Mitigation: Review labels before sensitive operations and use the audit command, especially the deny-only view, to inspect enforcement decisions. <br>


## Reference(s): <br>
- [Privacy Shield on ClawHub](https://clawhub.ai/xiaobu2020/privacy-shield) <br>
- [Publisher profile](https://clawhub.ai/user/xiaobu2020) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Text, JSON] <br>
**Output Format:** [Markdown guidance with CLI commands and local JSON/JSONL registry records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local privacy labels, permission check results, and audit-log entries; no hidden network, credential, or privilege behavior was reported by security evidence.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
