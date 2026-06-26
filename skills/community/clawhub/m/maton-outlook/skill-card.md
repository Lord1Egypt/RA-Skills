## Description: <br>
Outlook / Microsoft mail integration via Maton managed OAuth and a Microsoft Graph-compatible gateway for reading, searching, summarizing, drafting, sending, labeling, moving, or managing Outlook, Hotmail, Live, and Microsoft 365 email through an existing Maton Outlook connection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[junzhongjunzi](https://clawhub.ai/user/junzhongjunzi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent work with a connected Outlook mailbox through Maton for mailbox triage, message search, summarization, drafting, and confirmation-gated mail operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: MATON_API_KEY authorizes access to a connected Outlook mailbox. <br>
Mitigation: Keep MATON_API_KEY private and install the skill only when the agent should access Outlook through Maton. <br>
Risk: Mailbox messages and metadata can contain sensitive personal or business information. <br>
Mitigation: Use the smallest necessary read scope, keep message pulls narrow, prefer previews before full bodies, and review content before sharing or summarizing it. <br>
Risk: Sending, deleting, moving, or marking messages changes mailbox state and can affect real recipients or records. <br>
Mitigation: Require explicit confirmation of recipients, subject, final body, and target message before any state-changing operation. <br>


## Reference(s): <br>
- [Outlook Graph / Maton examples](references/graph-examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with API request examples, JSON payloads, and Python helper command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May execute Microsoft Graph-style API calls through Maton when MATON_API_KEY and an ACTIVE Outlook connection are available.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
