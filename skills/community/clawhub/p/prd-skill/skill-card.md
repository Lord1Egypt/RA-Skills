## Description: <br>
Generate structured Product Requirements Documents (PRD) from natural language user requirements. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tc1993](https://clawhub.ai/user/tc1993) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Product managers, developers, and agent users use this skill to turn app ideas or feature requests into a structured PRD covering product overview, functional requirements, user flows, technical specifications, and non-functional requirements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can move from PRD generation into downstream development or QA activity without an explicit approval checkpoint. <br>
Mitigation: Require the agent to return the PRD for review and ask for explicit approval before saving files, sending session messages, or invoking dev-skill or qa-skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tc1993/prd-skill) <br>
- [Publisher profile](https://clawhub.ai/user/tc1993) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Guidance] <br>
**Output Format:** [Markdown PRD with structured section headers] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save a timestamped PRD file and hand the PRD to downstream development and QA skills when allowed by the agent workflow.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
