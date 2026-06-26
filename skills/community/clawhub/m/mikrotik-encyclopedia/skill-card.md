## Description: <br>
MikroTik RouterOS documentation-first workflow for MikroTik-specific questions, troubleshooting, command planning, live CLI/API work, configuration review, log analysis, security review, performance tuning, and diagnostics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kklouzal](https://clawhub.ai/user/kklouzal) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Network administrators, developers, and engineers use this skill to answer MikroTik RouterOS/device questions, plan commands, review configurations and logs, inspect live devices, and maintain a workspace-local cache of official docs plus operational notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may fetch external MikroTik documentation into the workspace. <br>
Mitigation: Use it only where fetching and storing official MikroTik documentation under .MikroTik-Encyclopedia is acceptable. <br>
Risk: Workspace notes may retain sensitive operational network details. <br>
Mitigation: Review or delete stored notes regularly, and do not record secrets, credentials, full topology, or sensitive network details unless intentionally retained. <br>
Risk: Live RouterOS CLI/API work can affect routing, firewalling, VLANs, CAPsMAN, DHCP, DNS, queues, or management reachability. <br>
Mitigation: Consult relevant official MikroTik docs first, inspect before changing devices, and avoid high-impact commands when uncertainty remains. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kklouzal/mikrotik-encyclopedia) <br>
- [Official MikroTik documentation](https://help.mikrotik.com/docs/) <br>
- [MikroTik Encyclopedia Workflow](references/workflow.md) <br>
- [MikroTik Topic Map](references/topic-map.md) <br>
- [MikroTik Encyclopedia Cache Layout](references/cache-layout.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, Code, Files] <br>
**Output Format:** [Markdown with inline shell commands, RouterOS configuration snippets, and optional workspace-local cache or note files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update .MikroTik-Encyclopedia cache and notes in the current workspace.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
