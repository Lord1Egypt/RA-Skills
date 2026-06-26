## Description: <br>
Automatically records and saves user-assistant text conversations as daily Markdown memory files and OpenClaw memory entries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tao-articism](https://clawhub.ai/user/tao-articism) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to persist text conversations automatically for later recall. It listens to inbound and outbound text messages, appends timestamped entries to daily Markdown files, and stores text memory records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill automatically saves every text conversation to disk and memory with limited user controls. <br>
Mitigation: Install only when this behavior is explicitly desired, and add opt-in, redaction, retention, and deletion controls before using it with sensitive conversations. <br>
Risk: Conversation content may include passwords, tokens, personal data, or confidential business information. <br>
Mitigation: Avoid using the skill around sensitive content unless storage is controlled and sensitive text is redacted before persistence. <br>
Risk: The artifact writes Markdown memory files to a fixed local path, which may not match every deployment environment. <br>
Mitigation: Review and configure the storage location before deployment, and restrict filesystem permissions to the intended memory directory. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tao-articism/memory-auto-sync) <br>
- [Publisher profile](https://clawhub.ai/user/tao-articism) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration] <br>
**Output Format:** [Daily Markdown files and OpenClaw memory-store text entries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Appends timestamped conversation entries and stores sender/date metadata for later recall.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact package.json lists 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
