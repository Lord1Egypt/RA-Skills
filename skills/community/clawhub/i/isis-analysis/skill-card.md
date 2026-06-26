## Description: <br>
IS-IS protocol analysis with adjacency diagnosis, LSPDB analysis, level 1/2 routing validation, and NET address verification across Cisco IOS-XE, Juniper JunOS, and Arista EOS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vahagn-madatyan](https://clawhub.ai/user/vahagn-madatyan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Network engineers and operators use this skill to troubleshoot IS-IS adjacency formation, LSP database consistency, level 1/2 routing behavior, NET addressing, and post-change validation across supported router platforms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Collected CLI output can reveal network topology, routing details, and operational state. <br>
Mitigation: Treat gathered command output as sensitive operational data and share it only with authorized reviewers. <br>
Risk: Router access with broad privileges can exceed the skill's read-only posture. <br>
Mitigation: Use least-privilege read-only SSH or console accounts for collection and review any remediation before applying changes. <br>


## Reference(s): <br>
- [IS-IS CLI Reference](references/cli-reference.md) <br>
- [IS-IS Adjacency State Machine and LSPDB Flooding](references/state-machine.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown report with vendor-specific CLI command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only diagnostic guidance; does not execute commands by itself.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
