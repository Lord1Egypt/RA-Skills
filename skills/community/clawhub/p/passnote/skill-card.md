## Description: <br>
Create and manage disposable memos using PassNote. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shiweifu](https://clawhub.ai/user/shiweifu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to create temporary PassNote memos and receive a viewing link plus passcode for sharing secure notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Memo contents and the PassNote API token are sent to the configured PassNote server. <br>
Mitigation: Use only trusted PassNote deployments, prefer HTTPS, and configure a scoped or revocable PASSNOTE_API_TOKEN. <br>
Risk: Users may place long-lived passwords, API keys, or regulated data into temporary memos. <br>
Mitigation: Avoid sending regulated data or long-lived secrets unless the configured PassNote deployment is approved for those materials. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shiweifu/passnote) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/shiweifu) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and command output with a PassNote link, passcode, and expiration details.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PASSNOTE_API_URL and PASSNOTE_API_TOKEN; memo contents are sent to the configured PassNote server.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
