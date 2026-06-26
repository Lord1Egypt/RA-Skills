## Description: <br>
Create, edit, and export Google Slides presentations. Use when creating new presentations, adding or updating slides, reading slide content, exporting to PDF/PPTX, or building a deck from scratch. Requires gog auth to be working. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nethunter](https://clawhub.ai/user/nethunter) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to create, inspect, update, comment on, and export Google Slides presentations through gog CLI commands and the bundled Slides API helper. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses Google account credentials and broader Google authority than its Slides-focused purpose requires. <br>
Mitigation: Use only an intentionally selected Google account, grant the minimum needed scopes, and review gog authentication before running Slides operations. <br>
Risk: Raw batch updates and comment resolve or reply operations can change presentation content or comment state. <br>
Mitigation: Review target presentation IDs and JSON batch requests before execution, test risky edits on copies, and require explicit approval before resolving comments or running arbitrary batch operations. <br>


## Reference(s): <br>
- [Google Slides Batch Request Patterns](references/batch_requests.md) <br>
- [Google Slides API batchUpdate reference](https://developers.google.com/slides/api/reference/rest/v1/presentations/batchUpdate) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON request examples, and generated presentation export files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or modify Google Slides presentations and export decks as PDF or PPTX files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
