## Description: <br>
A local-first Instagram content system for hooks, captions, content structure, and draft storage. Acts as The Attention Sculptor to optimize stop-rate and retention. No API connection, no auto-posting, no automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agenticio](https://clawhub.ai/user/agenticio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and content teams use this skill to improve Instagram hooks, captions, carousel structure, CTAs, and account strategy. It can optionally save finalized caption drafts locally while leaving publishing and account actions manual. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Saved caption drafts can persist in local workspace memory and may be exposed if that workspace is shared or backed up. <br>
Mitigation: Avoid saving sensitive draft text in shared or backed-up workspaces, and remove local drafts when they are no longer needed. <br>
Risk: Generated Instagram strategy or caption guidance may be unsuitable, misleading, or too aggressive for a specific brand or audience. <br>
Mitigation: Review and edit all hooks, captions, CTAs, and account strategy recommendations before publishing manually. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/agenticio/instagram) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with optional shell command usage for local draft storage] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create a local captions.json draft file only when persistence is requested.] <br>

## Skill Version(s): <br>
2.1.1 (source: frontmatter, skill.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
