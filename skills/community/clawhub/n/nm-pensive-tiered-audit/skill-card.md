## Description: <br>
Runs a three-tier codebase audit covering git history, targeted scans, and gated full review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering reviewers use this skill to audit codebase quality, branch changes, instability, churn, and pre-PR readiness through staged review tiers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad triggers such as review or audit may activate the skill during routine code-review requests. <br>
Mitigation: Confirm the intended audit scope before allowing Tier 2 or Tier 3 review. <br>
Risk: Audit findings and generated local files may influence code decisions if accepted without review. <br>
Mitigation: Review the findings, cited evidence, and any proposed commands before relying on them. <br>
Risk: Full-codebase Tier 3 review can expand scope and resource use beyond the initial audit. <br>
Mitigation: Require documented Tier 2 justification and explicit user approval before Tier 3 begins. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-pensive-tiered-audit) <br>
- [Project homepage](https://github.com/athola/claude-night-market/tree/master/plugins/pensive) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown findings with inline shell commands and YAML output contracts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local findings under .coordination/agents and requires explicit user approval before Tier 3 full-codebase review.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
