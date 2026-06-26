## Description: <br>
OSPF protocol analysis with adjacency diagnosis, area design validation, LSA interpretation, and SPF convergence assessment, with multi-vendor coverage for Cisco IOS-XE, Juniper JunOS, and Arista EOS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vahagn-madatyan](https://clawhub.ai/user/vahagn-madatyan) <br>

### License/Terms of Use: <br>
Apache-2.0 <br>


## Use Case: <br>
Network engineers and operations teams use this skill to investigate OSPF adjacency failures, validate area design, interpret LSAs and LSDB health, and assess SPF convergence across Cisco IOS-XE, Juniper JunOS, and Arista EOS environments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Router command output can include network topology, addressing, or operational details. <br>
Mitigation: Use read-only credentials where possible and share only the router output needed for diagnosis. <br>
Risk: Some recommended remediations, such as clearing OSPF, changing MTU handling, configuring virtual links, or changing redistribution filters, can disrupt routing. <br>
Mitigation: Treat remediation commands as change-control actions that require explicit approval, an appropriate maintenance window, and a rollback plan. <br>


## Reference(s): <br>
- [OSPF CLI Reference - Cisco / JunOS / EOS](references/cli-reference.md) <br>
- [OSPF Neighbor Finite State Machine (FSM)](references/state-machine.md) <br>
- [ClawHub release page](https://clawhub.ai/vahagn-madatyan/ospf-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with read-only network diagnostic commands and structured analysis guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces diagnostic reasoning and recommended next checks; does not execute device changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
