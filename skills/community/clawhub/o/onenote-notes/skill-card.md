## Description: <br>
Manage OneNote notebooks, sections, pages, and page content via Microsoft Graph API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to connect OpenClaw to a Microsoft OneNote account through ClawLink, then inspect notebooks, sections, pages, and page HTML. It also supports confirmed create, update, copy, and delete workflows for OneNote content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires connecting a Microsoft OneNote account through ClawLink and can access notebook, section, page, and page-content data within that account. <br>
Mitigation: Review the Microsoft permission prompt before connecting, use the intended Microsoft account, and disconnect the integration when access is no longer needed. <br>
Risk: Write and delete operations can change or remove OneNote content. <br>
Mitigation: Confirm the exact target resource and intended effect before any create, update, copy, or delete action, and preview write operations where supported. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hith3sh/onenote-notes) <br>
- [Publisher profile](https://clawhub.ai/user/hith3sh) <br>
- [Microsoft Graph OneNote API overview](https://learn.microsoft.com/en-us/graph/api/resources/onenote) <br>
- [OneNote notebook resource](https://learn.microsoft.com/en-us/graph/api/resources/notebook) <br>
- [OneNote page resource](https://learn.microsoft.com/en-us/graph/api/resources/page) <br>
- [OneNote section resource](https://learn.microsoft.com/en-us/graph/api/resources/section) <br>
- [ClawLink OpenClaw docs](https://docs.claw-link.dev/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown with inline bash commands and JSON tool parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include HTML page content or Microsoft Graph tool-call parameters when the user requests OneNote operations.] <br>

## Skill Version(s): <br>
1.0.5 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
