## Description: <br>
电脑维修智能助手通过交互式问诊诊断台式机和笔记本电脑故障，并生成维修方案、成本估算、配件建议和可视化维修报告。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bettermen](https://clawhub.ai/user/bettermen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and support agents use this skill to triage PC hardware, operating-system, network, performance, upgrade, and repair questions. It helps compare emergency self-help, DIY repair, and professional service options with compatibility checks, cost estimates, and safety reminders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Repair commands, disk checks, data recovery, OS reinstall steps, or storage cloning can cause data loss or worsen problems on failing media. <br>
Mitigation: Back up important data first, confirm each command's effect, stop risky disk operations when storage may be failing, and use professional data recovery when the data is valuable. <br>
Risk: Hardware disassembly, cleaning, or component replacement can damage parts, create static-discharge risk, or affect warranty coverage. <br>
Mitigation: Power down and unplug equipment, use anti-static precautions, document serial numbers and warranty status, and choose official or professional service when uncertain. <br>
Risk: Repair prices, parts availability, and compatibility recommendations may vary by market and date. <br>
Mitigation: Verify current part specifications, warranty terms, and local prices before buying components or approving a repair quote. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bettermen/pc-repair) <br>
- [常见电脑故障诊断流程图](references/common_faults.md) <br>
- [硬件兼容性检查表](references/parts_compatibility.md) <br>
- [2024年电脑维修价格参考表](references/repair_costs.md) <br>
- [维修工具和软件使用指南](references/tool_guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance, configuration] <br>
**Output Format:** [Markdown guidance with diagnostic tables, shell command snippets, and optional HTML report content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include hardware compatibility checks, repair cost estimates, shopping keywords, risk notices, and printable report sections.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
