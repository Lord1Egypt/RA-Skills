## Description: <br>
A 5-phase framework for reliable AI-to-AI task delegation with task tracking, sub-agent performance logging, automated verification, fallback chains, and multi-axis task scoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Hogpile](https://clawhub.ai/user/Hogpile) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to plan, monitor, verify, and recover delegated AI-agent work. It provides task logs, delegation contracts, fallback chains, scoring guidance, and lightweight verification commands for multi-agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent task logs and performance notes may capture sensitive project context if used carelessly. <br>
Mitigation: Keep logs project-scoped and avoid storing secrets or sensitive data in TASKS.md, performance notes, or delegation records. <br>
Risk: Scheduled follow-up checks and delegated actions may persist beyond the intended task or affect high-impact work. <br>
Mitigation: Approve any scheduled check before creating it, remove checks after completion, and require human approval for irreversible or high-impact actions. <br>
Risk: Automated scoring can understate the risk of irreversible or ambiguous tasks. <br>
Mitigation: Treat scoring output as guidance only and manually review tasks involving sensitive data, unclear requirements, or irreversible effects. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Hogpile/intelligent-delegation) <br>
- [Intelligent AI Delegation paper](https://arxiv.org/abs/2602.11865) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with Python CLI commands and template files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes task tracking templates, delegation scoring recommendations, and verification check outputs.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter, package.json, and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
