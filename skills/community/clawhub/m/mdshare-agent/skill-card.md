## Description: <br>
Create, read, unlock, update, and delete temporary Markdown shares through the MDShare service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cced3000](https://clawhub.ai/user/cced3000) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, agents, and external users use this skill to publish Markdown as temporary MDShare links, retrieve shared Markdown, and manage edits, settings, or deletion through public, edit, and manage links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Markdown content may include secrets, personal data, or internal material before it is published to MDShare or another deployment. <br>
Mitigation: Review content before creating a share, and avoid publishing sensitive material unless the user explicitly accepts that exposure. <br>
Risk: Manage and edit links include tokens that allow anyone with the link to edit settings, modify content, or delete the share. <br>
Mitigation: Keep token-bearing links private and return them only when the user asks for them or needs them to manage the share. <br>
Risk: Burn-after-read shares can become unavailable after access is confirmed. <br>
Mitigation: Explain burn-after-read behavior and require clear user intent before sending confirmView for gated content. <br>
Risk: Concurrent edits can overwrite another update if conflict handling is bypassed. <br>
Mitigation: When the API reports a conflict, summarize the remote update and force-save only after explicit confirmation. <br>


## Reference(s): <br>
- [MDShare API Reference](references/api.md) <br>
- [MDShare Agent Workflows](references/workflows.md) <br>
- [MDShare Agent Install Examples](references/install-examples.md) <br>
- [MDShare default deployment](https://share.yekyos.com) <br>
- [ClawHub skill page](https://clawhub.ai/cced3000/mdshare-agent) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, guidance] <br>
**Output Format:** [Markdown responses with links, JSON request examples, and HTTP API guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce public, edit, and manage links; manage and edit links contain tokens and should be kept private.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
