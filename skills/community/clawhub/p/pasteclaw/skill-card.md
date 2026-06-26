## Description: <br>
Use Pasteclaw.com API to create, update, group with session keys, and delete snippets with agent-friendly request patterns and headers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tairov](https://clawhub.ai/user/tairov) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to publish HTML, CSS, JavaScript, Markdown, JSON, YAML, or text snippets to Pasteclaw.com and return stable preview URLs. It also supports updating, grouping, downloading, and deleting snippets when the required IDs and tokens are available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Uploaded snippets, edit tokens, and session keys are sent to an external paste service. <br>
Mitigation: Use the skill only for material intended for external sharing, avoid secrets and private configuration, and keep session keys out of URLs. <br>
Risk: Default curl examples include `-k`, which disables HTTPS certificate verification. <br>
Mitigation: Remove `-k` from curl commands so HTTPS certificates are verified before uploading content or tokens. <br>
Risk: Update and delete operations can affect the wrong snippet if the snippet ID or edit token is incorrect. <br>
Mitigation: Confirm the snippet ID and edit token before performing update or delete requests. <br>


## Reference(s): <br>
- [PasteClaw release page](https://clawhub.ai/tairov/pasteclaw) <br>
- [Pasteclaw service](https://pasteclaw.com) <br>
- [Pasteclaw snippets API](https://pasteclaw.com/api/snippets) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash, Python, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns or explains snippet URLs, IDs, edit tokens, session keys, and concise error messages.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
