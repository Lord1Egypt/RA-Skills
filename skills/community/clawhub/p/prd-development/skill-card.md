## Description: <br>
Turns product requirements, meeting notes, or feature descriptions into PRD content that a coding agent can execute. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xuyinghan02-cell](https://clawhub.ai/user/xuyinghan02-cell) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Product managers, developers, and delivery teams use this skill to turn early product ideas, meeting notes, or feature descriptions into structured PRDs with project background, user stories, feature specifications, interaction flows, and Word-document handoff guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow may hand work to downstream skills such as DNS-analysis, botnet-analysis, or docx_handler. <br>
Mitigation: Review downstream skills before using the workflow with sensitive product plans, meeting notes, or operational details. <br>
Risk: Generated PRD content can contain incomplete, incorrect, or ambiguous requirements if the initial inputs are underspecified. <br>
Mitigation: Review the generated user stories, feature specifications, interaction flows, and any [to confirm] items before relying on the document for implementation. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Structured Markdown PRD guidance and document-writing workflow output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May route domain-specific analysis to named downstream skills and may hand completed PRD content to docx_handler for Word document output.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
