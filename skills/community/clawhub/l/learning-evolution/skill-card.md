## Description: <br>
Create evidence-based learning reviews for skills: analyze usage patterns, track effectiveness, and plan evolutions from real usage data, user feedback, and observed outcomes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrylabsj](https://clawhub.ai/user/harrylabsj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this skill to create local Markdown templates for usage analysis, effectiveness review, churn diagnosis, and evolution planning. It helps keep skill changes grounded in verified logs, feedback, outcomes, and human review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated Markdown reports can persist sensitive user feedback, identifiable logs, or internal review notes if users add them to the templates. <br>
Mitigation: Use anonymized or aggregated evidence where possible, and include sensitive feedback only when retention is intentional and approved. <br>
Risk: LEARNING_DATA_DIR can redirect where reports are written, which may place review files in an unexpected local directory. <br>
Mitigation: Check LEARNING_DATA_DIR before running the scripts when report location matters. <br>
Risk: Unfilled template placeholders could be mistaken for measured usage, satisfaction, completion, or error metrics. <br>
Mitigation: Treat TODO and blank fields as missing evidence, and make product or skill changes only after verified data and human review are added. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/harrylabsj/skills/learning-evolution) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [README.md](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown templates and concise guidance with local shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates dated local Markdown report templates under data/ or LEARNING_DATA_DIR; generated metrics and recommendations remain blank until verified evidence is added.] <br>

## Skill Version(s): <br>
1.0.3 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
