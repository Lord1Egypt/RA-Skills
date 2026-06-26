## Description: <br>
Runs adversarial multi-agent war-room evaluations for strategic decisions by assigning Analyst, Guardian, Treasurer, Builder, and Strategist roles, then synthesizing a GO, NO-GO, or REWORK ruling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scytheshan-pixel](https://clawhub.ai/user/scytheshan-pixel) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees, developers, and decision owners use this skill to stress-test proposals for investments, products, architecture, hiring, and other decisions that benefit from structured adversarial review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Strategic proposal details may be shared across spawned subagents and written to local files. <br>
Mitigation: For confidential decisions, instruct the agent not to use temporary files and only provide information approved for subagent review. <br>
Risk: The artifact asks agents to store decisions in long-term memory, commit reports to git, and update logs. <br>
Mitigation: Require explicit approval for memory writes, git commits, log updates, and report destinations before running the workflow. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/scytheshan-pixel/iris-war-room) <br>
- [Domain Adaptation](artifact/references/domains.md) <br>
- [Prompt Templates](artifact/references/prompts.md) <br>
- [Role Definitions](artifact/references/roles.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report with role summaries, scenario projections, ruling, action items, and optional local file outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce spawned-agent prompts and local report paths as part of the workflow.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
