## Description: <br>
Evaluates an OpenClaw skill with three independent sub-agent reviewers and summarizes scores, disagreements, strengths, issues, and recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[54lynnn](https://clawhub.ai/user/54lynnn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this skill to review OpenClaw skill directories, compare independent evaluator feedback, and identify practical improvements before release. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads target skill text files and shares them with evaluator sub-agents. <br>
Mitigation: Use it only on skill directories intended for review, and remove secrets or private material from target files before evaluation. <br>
Risk: Multi-agent reviews can produce subjective or inconsistent recommendations. <br>
Mitigation: Treat the report as advisory, check cited file evidence, and manually review any proposed changes before relying on them. <br>


## Reference(s): <br>
- [Evaluation protocol](references/evaluation-protocol.md) <br>
- [ClawHub release page](https://clawhub.ai/54lynnn/multi-agent-skill-evaluator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown evaluation report with a score table, disagreement analysis, strengths, issues, and recommendation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes three independent evaluator perspectives and optional follow-up analysis for large scoring disagreements.] <br>

## Skill Version(s): <br>
1.4.0 (source: frontmatter and server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
