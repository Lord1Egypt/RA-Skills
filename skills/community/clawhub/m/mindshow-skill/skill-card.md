## Description: <br>
Calls the Mindshow/AIPPT API to generate PPTs from keywords or uploaded files, including outline generation, Markdown content generation, PPT task creation, progress polling, template and resource operations, account information, PDF or jump-link retrieval, and API schema inspection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xcwen](https://clawhub.ai/user/xcwen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and end users use this skill to ask an agent to create presentation decks from topics, keywords, or uploaded documents through Mindshow/AIPPT. It also helps inspect API schemas, choose templates, upload resources, poll generation jobs, and retrieve generated PPT or PDF links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Mindshow/AIPPT bearer token for protected API calls. <br>
Mitigation: Keep tokens in runtime environment variables or a local .env file only, and do not print or persist tokens elsewhere. <br>
Risk: Prompts, generated content, and selected source files may be sent to Mindshow/AIPPT. <br>
Mitigation: Use only authorized content and avoid uploading sensitive or regulated documents unless approved. <br>
Risk: Some API endpoints can modify AIPPT account data. <br>
Mitigation: Use delete or template-changing endpoints only when the user explicitly requests those changes. <br>


## Reference(s): <br>
- [Mindshow API Documentation](https://api-doc.mindshow.vip/) <br>
- [Mindshow API Service](https://api.mindshow.vip) <br>
- [ClawHub Skill Page](https://clawhub.ai/xcwen/mindshow-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Markdown, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON request and response bodies, raw SSE streams, and generated PPT or PDF links.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses bearer-token-authenticated Mindshow/AIPPT API calls; streaming endpoints emit raw SSE data.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
