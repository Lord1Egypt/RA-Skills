## Description: <br>
PPT Creator helps an agent create, review, edit, style, and download PowerPoint presentations from topics, outlines, local text documents, or project summaries through Yoo AI APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daan0701](https://clawhub.ai/user/daan0701) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, employees, and developers use this skill to generate presentation decks, review and revise outlines before generation, add speaker notes, insert slides, change styles, preview covers, and create image-based PPTs when visual quality is more important than text editability. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PPT topics, document text, outlines, and project summaries are sent to the external Yoo AI service. <br>
Mitigation: Use the skill only with content approved for Yoo AI processing, and avoid submitting confidential or regulated information unless the deployment has appropriate approval. <br>
Risk: A Yoo AI API key is required and could be exposed if stored directly in config.json. <br>
Mitigation: Set YOO_AI_API_KEY as an environment variable when possible; protect or remove config.json if it contains a real key and rotate any key that may have been exposed. <br>
Risk: Generated presentations, task metadata, editor links, and download paths may be written locally or printed in command output. <br>
Mitigation: Review local output directories and .tasks.json for sensitive content, and avoid sharing terminal logs that include task IDs or editor URLs. <br>
Risk: Image-based PPT mode produces slides whose text cannot be edited after generation. <br>
Mitigation: Confirm the user wants image-based mode before use and choose standard editable PPT generation when downstream text editing is required. <br>


## Reference(s): <br>
- [PPT Creator ClawHub Listing](https://clawhub.ai/daan0701/ppt-creator) <br>
- [Yoo AI API Service Endpoint](https://saas.api.yoo-ai.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Files, Markdown, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with node commands; generated PPTX files, task status text, editor or download URLs, and JSON or Markdown outlines.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May persist task status in .tasks.json and write generated presentations to a local output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
