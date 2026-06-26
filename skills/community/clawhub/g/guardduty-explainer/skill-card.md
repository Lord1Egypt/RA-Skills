## Description: <br>
Translate GuardDuty findings into plain-English incident summaries with actionable response steps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anmolnagpal](https://clawhub.ai/user/anmolnagpal) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Security analysts and cloud engineers use this skill to turn exported AWS GuardDuty findings into incident summaries, false-positive assessments, MITRE ATT&CK mappings, and prioritized response playbooks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may paste AWS credentials, access keys, secret keys, or session tokens with finding data. <br>
Mitigation: Use only exported findings or console text and check inputs for credentials before analysis. <br>
Risk: Generated containment or remediation AWS CLI commands could affect live cloud resources if run without review. <br>
Mitigation: Review and adapt generated commands with an AWS operator before running them in a real account. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/anmolnagpal/guardduty-explainer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with structured sections and inline AWS CLI commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses user-provided GuardDuty data only; generated AWS CLI commands should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
