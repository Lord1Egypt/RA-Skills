## Description: <br>
SiteSpeakAI helps an agent operate SiteSpeakAI through the OOMOL oo CLI for reading, creating, updating, querying, and deleting SiteSpeakAI data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run SiteSpeakAI account, chatbot, conversation, lead, source, suggested-message, and updated-answer actions through an OOMOL-connected SiteSpeakAI account. It can also query a chatbot and manage updated-answer entries when the user confirms write or destructive actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a connected SiteSpeakAI account and server-side managed credentials, so actions may access account, chatbot, conversation, lead, source, and answer data. <br>
Mitigation: Install only after reviewing the skill text and publisher, and use the connected account scopes appropriate for the intended SiteSpeakAI tasks. <br>
Risk: Write and destructive actions can create, update, or delete SiteSpeakAI updated-answer entries. <br>
Mitigation: Confirm the exact payload, target chatbot, and expected effect with the user before running write actions, and obtain explicit approval before destructive deletion. <br>
Risk: The security scan is a low-confidence clean pass because scanner evidence says artifact contents were not available for direct review. <br>
Mitigation: Review the installed skill text and metadata before use, especially commands involving credentials, network access, file access, or account-changing actions. <br>


## Reference(s): <br>
- [SiteSpeakAI skill page](https://clawhub.ai/oomol/oo-sitespeakai) <br>
- [SiteSpeakAI homepage](https://sitespeak.ai) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with oo CLI commands and JSON payloads or responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses server-side managed credentials through OOMOL; write and destructive actions require user confirmation.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
