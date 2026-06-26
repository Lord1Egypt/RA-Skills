## Description: <br>
Gmail triage assistant using Haiku LLM for classification, label application, and draft replies (uses gog CLI; never auto-sends). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[OfficialDelta](https://clawhub.ai/user/OfficialDelta) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Email users with a configured Gmail account use this skill to triage recent inbox messages, apply organizational labels, and prepare concise draft replies without sending email automatically. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill accesses the configured Gmail account through gog. <br>
Mitigation: Install only for an account you intend the skill to access and set GOG_ACCOUNT explicitly. <br>
Risk: The scripts include hardcoded Gmail and keyring defaults. <br>
Mitigation: Set your own GOG_ACCOUNT and GOG_KEYRING_PASSWORD values before use and avoid relying on the default keyring password. <br>
Risk: Inbox summaries, draft queues, label files, and voice-reference content may retain private email-derived data locally. <br>
Mitigation: Delete or restrict the generated cache and voice-reference files when local retention is not desired. <br>
Risk: Generated label classifications could apply labels to the wrong Gmail threads. <br>
Mitigation: Review the generated label JSON before running the label-application script. <br>


## Reference(s): <br>
- [Gmail Secretary on ClawHub](https://clawhub.ai/OfficialDelta/gmail-secretary) <br>
- [Voice reference](references/voice.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown digests and draft queues, JSON classification files, and shell command workflows] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Never auto-sends email; label application requires generated label data and an explicit script run.] <br>

## Skill Version(s): <br>
1.0.27 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
