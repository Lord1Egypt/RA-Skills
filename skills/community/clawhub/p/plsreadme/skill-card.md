## Description: <br>
Share markdown files and text as clean, readable web links via plsreadme.com. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[FacundoLucci](https://clawhub.ai/user/FacundoLucci) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, writers, and agents use this skill to turn markdown files, generated notes, PRDs, proposals, or plain text into clean public web links after confirming the content is safe to publish. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Shared links are permanent and publicly accessible, so sensitive documents or private notes could be exposed. <br>
Mitigation: Confirm with the user before each upload and avoid sharing secrets, private notes, or confidential content. <br>
Risk: The local setup runs the plsreadme MCP package through npx. <br>
Mitigation: Inspect or pin the npm MCP package before local use, or use the remote MCP endpoint when that better matches the deployment policy. <br>
Risk: Plain text or refactored non-markdown content may be restructured before sharing. <br>
Mitigation: Review the final content and title before publishing the generated page. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/FacundoLucci/plsreadme) <br>
- [plsreadme MCP endpoint](https://plsreadme.com/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown or plain text guidance with returned readable and raw markdown URLs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Shared links are permanent and publicly accessible; local file uploads are limited to 200KB.] <br>

## Skill Version(s): <br>
0.4.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
