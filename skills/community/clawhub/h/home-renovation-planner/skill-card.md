## Description: <br>
Home Renovation Planner helps homeowners plan renovation budgets, schedules, material choices, inspection checklists, and dispute responses from property details, budget, and requirements. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mcheisenberg](https://clawhub.ai/user/mcheisenberg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Homeowners and renovation planners use this skill to turn area, layout, city, budget, style, and timeline constraints into a staged renovation plan with budget allocation, material guidance, acceptance checks, and dispute-handling paths. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: The Pro unlock flow asks users to pay through an external QR code and share payment proof with the seller. <br>
Mitigation: Install and use the Pro flow only if the publisher is trusted, and keep payment verification outside sensitive agent workflows. <br>
Risk: Activation requires running a local verification script that records activation state in the user's home directory. <br>
Mitigation: Review the script before execution and run it only in an environment where writing ~/.home-renovation-planner.activated is acceptable. <br>
Risk: Renovation plans and dispute guidance may not account for site-specific conditions, contract terms, or local professional requirements. <br>
Mitigation: Treat generated plans as planning support and confirm construction, safety, and legal decisions with qualified local professionals. <br>


## Reference(s): <br>
- [Home Renovation Planner on ClawHub](https://clawhub.ai/mcheisenberg/skills/home-renovation-planner) <br>
- [Renovation Process Nodes](artifact/references/01_装修全流程节点.md) <br>
- [Budget Reference](artifact/references/02_各环节预算参考.md) <br>
- [Material Selection Pitfall Guide](artifact/references/03_材料避坑指南.md) <br>
- [Construction Acceptance Standards](artifact/references/04_施工验收标准.md) <br>
- [Common Dispute Rights Protection](artifact/references/05_常见纠纷维权.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with tables, checklists, and occasional shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Chinese-language renovation guidance; Pro activation can invoke a local verification script that writes activation state under the user's home directory.] <br>

## Skill Version(s): <br>
1.1.0 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
