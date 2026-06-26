## Description: <br>
OneNote API integration with managed OAuth via Microsoft Graph for accessing and managing notebooks, sections, section groups, and pages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to work with Microsoft OneNote content through Maton-managed OAuth, including reading, creating, and organizing notebooks, sections, section groups, and pages. It is suited for agents that need to generate API requests, shell commands, code examples, and configuration guidance for OneNote workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires MATON_API_KEY and Microsoft OAuth access to OneNote data. <br>
Mitigation: Keep MATON_API_KEY private and install the skill only when the user trusts Maton to broker access to the connected OneNote account. <br>
Risk: Requests may affect the wrong OneNote account when multiple connections are active. <br>
Mitigation: Use the Maton-Connection header and confirm the intended connection before acting. <br>
Risk: Create, update, or delete operations can change notebooks, sections, pages, or connections. <br>
Mitigation: Confirm the exact target resource and intended effect with the user before executing any write or delete request. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/byungkyu/one-note) <br>
- [Publisher profile](https://clawhub.ai/user/byungkyu) <br>
- [Maton homepage](https://maton.ai) <br>
- [OneNote API overview](https://learn.microsoft.com/en-us/graph/integrate-with-onenote) <br>
- [OneNote REST API reference](https://learn.microsoft.com/en-us/graph/api/resources/onenote-api-overview) <br>
- [OneNote page HTML reference](https://learn.microsoft.com/en-us/graph/onenote-input-output-html) <br>
- [Microsoft Graph Explorer](https://developer.microsoft.com/graph/graph-explorer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline API paths, JSON, HTML, Python, JavaScript, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Microsoft Graph and Maton API request examples that require MATON_API_KEY and an active OneNote OAuth connection] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
