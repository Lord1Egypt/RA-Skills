## Description: <br>
Guides an agent through a multi-round PRD drafting and review workflow that uses user-confirmed writer and reviewer models to produce final Markdown PRD deliverables. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[galaxy-operations-guide](https://clawhub.ai/user/galaxy-operations-guide) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Product managers, founders, and product-oriented agents use this skill to turn a product topic, background material, and target platform into iterated PRD drafts, review notes, and a final Markdown PRD. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-provided links or background material may be processed by the selected writer and reviewer models. <br>
Mitigation: Confirm that the user is comfortable sharing the material with those models before fetching or processing it. <br>
Risk: The workflow writes multiple PRD and review Markdown files to disk. <br>
Mitigation: Confirm the output folder before starting and report generated file paths after each round. <br>
Risk: Using the skill for quick one-off PRD advice may produce more process overhead than needed. <br>
Mitigation: Use it when a structured multi-round drafting and review loop is appropriate. <br>


## Reference(s): <br>
- [PRD standard structure reference](references/prd-templates.md) <br>
- [ClawHub skill page](https://clawhub.ai/galaxy-operations-guide/prd-iterative) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, guidance] <br>
**Output Format:** [Markdown PRD drafts, Markdown review reports, and concise status updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes versioned PRD and review files to a user-confirmed output path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
