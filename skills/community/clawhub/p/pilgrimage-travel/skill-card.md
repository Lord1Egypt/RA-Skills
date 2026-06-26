## Description: <br>
Book flights for pilgrimage travel to sacred sites and religious destinations, with related travel services powered by Fliggy (Alibaba Group). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivan97](https://clawhub.ai/user/ivan97) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travelers and travel-planning agents use this skill to search pilgrimage-related flights and present bookable travel options with validated booking links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install and run a third-party global CLI before searching travel options. <br>
Mitigation: Install the FlyAI CLI only after approval, verify the package source, and review booking links before entering personal details or making purchases. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ivan97/pilgrimage-travel) <br>
- [Parameter Collection & Output Templates](references/templates.md) <br>
- [Scenario Playbooks](references/playbooks.md) <br>
- [Failure Recovery](references/fallbacks.md) <br>
- [Execution Runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with flight comparison tables, booking links, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs must be based on flyai CLI results and include booking links for listed options.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
