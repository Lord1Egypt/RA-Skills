## Description: <br>
Publishes user-selected content to Nosi and returns shareable content and raw text URLs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[billhao](https://clawhub.ai/user/billhao) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to publish selected text, markdown, or files to nosi.pub and return a shareable URL for the published content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Published content may be public and permanent, including confidential or personal information if submitted. <br>
Mitigation: Confirm the user intends to publish the selected content and avoid confidential or personal material before calling nosi.pub. <br>
Risk: The workflow uses a Nosi API key provided by the user. <br>
Mitigation: Use only a Nosi API key intended for this service and do not expose it in published content or final responses. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/billhao/nosi) <br>
- [Nosi](https://nosi.pub) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Guidance, API calls] <br>
**Output Format:** [Markdown or plain text with published URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns a human-friendly content URL and raw machine-readable URL when publishing succeeds.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
