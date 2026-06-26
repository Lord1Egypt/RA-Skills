## Description: <br>
Personal AI assistant that monitors online privacy, calculates exposure scores, automates data broker opt-outs, tracks breaches, and offers privacy advice. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlielila](https://clawhub.ai/user/charlielila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to monitor personal data exposure, track privacy scores, prepare data broker opt-outs and DSAR requests, receive breach alerts, and get privacy guidance for social media, ad tracking, and data removal workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may process sensitive personal data and service credentials. <br>
Mitigation: Use only in an environment where local file access and credential scope can be restricted, and avoid entering real PII or credentials until data review and deletion controls are confirmed. <br>
Risk: The skill describes outbound opt-out, DSAR, email, and messaging actions on the user's behalf. <br>
Mitigation: Require user preview and approval for every outbound submission or message, and verify each recipient before sending. <br>
Risk: The artifact includes a file-read tool and the security summary flags broad local file access. <br>
Mitigation: Limit the tool to approved user-owned paths and deny reads of secrets, configuration files, and unrelated local data. <br>
Risk: Privacy-sensitive content could be exposed to external services or logs. <br>
Mitigation: Confirm how Supabase, LLM, Telegram, email, and logging data can be reviewed, deleted, minimized, and kept out of third-party logs before installation. <br>


## Reference(s): <br>
- [Privacy Concierge ClawHub page](https://clawhub.ai/charlielila/privacy-concierge) <br>
- [Publisher profile](https://clawhub.ai/user/charlielila) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Conversational text and Markdown with optional command and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include privacy scores, scan summaries, opt-out or DSAR drafts, alerts, and source-backed privacy advice.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
