## Description: <br>
Monitors a Gmail inbox, generates personalized AI-assisted follow-up replies, and saves them as Gmail drafts for human review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuliuyi717-ux](https://clawhub.ai/user/yuliuyi717-ux) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure a Gmail OAuth workflow that monitors selected inbox queries and drafts AI-generated replies for client, lead, or agency inbox review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read private Gmail messages and send selected email contents to the configured AI backend. <br>
Mitigation: Use a test mailbox first, narrow the Gmail query, confirm the AI backend, and review every generated draft before sending. <br>
Risk: The skill can modify mailbox state by creating drafts, adding processed labels, and optionally marking messages as read. <br>
Mitigation: Keep --mark-read disabled until behavior is validated and run with tightly scoped Gmail queries and low max-emails values. <br>
Risk: OAuth token files and API keys grant access to Gmail and the configured AI provider. <br>
Mitigation: Protect token.json, Google client secrets, and API keys with local file permissions and rotate credentials if exposed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/yuliuyi717-ux/gmail-auto-draft) <br>
- [Setup Guide](references/setup.md) <br>
- [Prompt Tuning](references/prompt-tuning.md) <br>
- [Upwork Demo Preset](references/upwork-demo.md) <br>
- [Gmail Auto Draft Script](scripts/gmail_auto_draft.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples; runtime execution prints JSON cycle summaries and creates Gmail draft messages.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates Gmail drafts for human review and can optionally mark processed messages as read.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
