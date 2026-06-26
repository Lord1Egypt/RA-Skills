## Description: <br>
QA Gate provides a standardized quality check for documents, skills, PRDs, blog posts, and code artifacts before review, release, or publication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freeman88-tch](https://clawhub.ai/user/freeman88-tch) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, writers, and agent operators use this skill as a final quality gate for artifacts that need factual, structural, operational, tone, completeness, and sensitive-data checks before they move forward. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review notes that the skill presents itself as read-only while also directing the agent to create report files and edit artifacts after failed checks. <br>
Mitigation: Ask the agent to report findings first, require explicit approval before fixes, and review any generated report or proposed edit before relying on it. <br>
Risk: The optional dual validation mode may send sensitive artifact content through an additional model path. <br>
Mitigation: Avoid dual validation for sensitive content unless the data handling route is approved for that material. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Guidance, Files] <br>
**Output Format:** [Markdown QA report with a PASS, PASS WITH FIXES, or FAIL verdict and severity-tagged findings.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write a qa-gate/YYYY-MM-DD-<artifact-slug>.md report and may propose or perform fixes after failures.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
