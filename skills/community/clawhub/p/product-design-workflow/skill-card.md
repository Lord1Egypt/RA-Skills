## Description: <br>
Guides an agent through a daily product-design workflow that generates product ideas, PRD documents, HTML prototypes, upload steps, and staged status reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hoovaycn](https://clawhub.ai/user/hoovaycn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Product managers, designers, and agent operators use this skill to produce a repeatable daily flow of consumer finance product ideas, product design documents, prototype pages, and report messages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review flags server credentials and report destinations as requiring human review before use. <br>
Mitigation: Use a restricted server account, prefer SSH keys over passwords, confirm upload and report destinations, and review the workflow before installing or running it. <br>
Risk: The upload workflow handles credentials and shell command construction for remote SSH/SCP operations. <br>
Mitigation: Avoid running the upload script until credential logging and command construction have been reviewed and fixed. <br>
Risk: A hard-coded or stale report group destination could send generated status updates to the wrong audience. <br>
Mitigation: Remove or parameterize fixed group IDs and verify the target group ID for each deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hoovaycn/product-design-workflow) <br>
- [Workflow guide](references/workflow-guide.md) <br>
- [Idea template](references/idea-template.md) <br>
- [Idea content specification](references/idea-content-spec.md) <br>
- [PRD template](references/prd-template.md) <br>
- [PRD design specification](references/prd-design-spec.md) <br>
- [Step-by-step report specification](references/step-by-step-report-spec.md) <br>
- [Report template specification](references/report-template-spec.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, generated product documents, HTML prototype files, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-supplied server, upload, report destination, schedule, and working-directory parameters before execution.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
