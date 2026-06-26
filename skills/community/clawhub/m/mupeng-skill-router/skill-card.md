## Description: <br>
Context-based skill auto-routing + federated skill composition. Analyzes user input to auto-select single or multiple skills and execute in order. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mupengi-bot](https://clawhub.ai/user/mupengi-bot) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to classify a user request, select one or more matching skills, order them into a workflow, and synthesize the downstream results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad automatic routing can run and chain other skills, including account and deployment workflows, without enough clear scoping or user control. <br>
Mitigation: Disable universal routing by default, require explicit confirmation before script execution or account/deployment actions, and allowlist trusted downstream skills. <br>
Risk: Chained hooks and event files can make automation behavior hard to inspect during multi-skill workflows. <br>
Mitigation: Make event files and hooks easy to inspect and clear before and after execution. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/mupengi-bot/mupeng-skill-router) <br>
- [Publisher profile](https://clawhub.ai/user/mupengi-bot) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and text guidance with inline shell command examples and workflow descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or coordinate chained skill execution; external account, posting, email, payment, git, or deployment actions should require explicit approval.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
