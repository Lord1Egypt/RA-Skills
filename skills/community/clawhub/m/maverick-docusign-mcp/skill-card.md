## Description: <br>
Search, read, and manage DocuSign envelopes, recipients, templates, documents, and signing status through a local MCP wrapper. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maverick](https://clawhub.ai/user/maverick) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external collaborators, developers, and operations teams use this skill to inspect DocuSign envelopes, templates, recipients, documents, and signing status, and to send envelopes from templates when the user has clearly authorized the action. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send real DocuSign envelopes and operate on signing workflows using sensitive OAuth credentials. <br>
Mitigation: Use least-privilege OAuth scopes, start in a DocuSign sandbox when possible, and require clear human confirmation before any send, void, update, or document-changing action. <br>
Risk: Unpinned runtime dependencies such as mcporter and Python packages can change behavior over time. <br>
Mitigation: Pin approved dependency versions in controlled environments and review updates before deployment. <br>
Risk: Credential rotation or setup with stale environment values can overwrite refreshed local vault credentials. <br>
Mitigation: Run setup only from the current credential source of truth and reconnect the integration when OAuth grants expire or are revoked. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/maverick/maverick-docusign-mcp) <br>
- [mcporter](https://github.com/steipete/mcporter) <br>
- [uv documentation](https://docs.astral.sh/uv/) <br>
- [DocuSign OAuth token endpoint](https://account-d.docusign.com/oauth/token) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, API calls] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON tool responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Tool calls run through a local stdio MCP wrapper and may access DocuSign envelope, recipient, template, document, and signing-status data.] <br>

## Skill Version(s): <br>
1.0.3 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
