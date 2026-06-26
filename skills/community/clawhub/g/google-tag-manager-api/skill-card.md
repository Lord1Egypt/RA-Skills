## Description: <br>
Google Tag Manager API integration with managed OAuth for managing GTM accounts, containers, workspaces, tags, triggers, variables, environments, and container versions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, marketing operations teams, and agents use this skill to inspect and manage Google Tag Manager resources through Maton-managed OAuth-backed API calls. It is suited for listing resources, preparing GTM workspace changes, and creating, updating, deleting, or publishing GTM entities after explicit user confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create, update, delete, publish, and change user-permission resources in Google Tag Manager. <br>
Mitigation: Require explicit user confirmation of the target account, container, workspace, resource, and intended effect before any write, publish, delete, or user-permission request. <br>
Risk: Brokered OAuth access and MATON_API_KEY expose sensitive account capabilities if mishandled. <br>
Mitigation: Install only when Maton is trusted, keep MATON_API_KEY private, and use the Maton-Connection header to select the intended connection when multiple connections exist. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/byungkyu/google-tag-manager-api) <br>
- [Maton homepage](https://maton.ai) <br>
- [Google Tag Manager API overview](https://developers.google.com/tag-platform/tag-manager/api/v2) <br>
- [Google Tag Manager API reference](https://developers.google.com/tag-platform/tag-manager/api/reference/rest) <br>
- [Google Tag Manager concepts](https://developers.google.com/tag-platform/tag-manager/api/v2/concept) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with HTTP request examples and JSON response patterns] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and a valid Maton-managed Google Tag Manager OAuth connection.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
