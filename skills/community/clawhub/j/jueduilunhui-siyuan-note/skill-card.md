## Description: <br>
思源笔记读写技能，提供与思源笔记（SiYuan Note）进行交互的能力，包括读取和写入笔记内容。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jueduilunhui](https://clawhub.ai/user/jueduilunhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to connect an agent to SiYuan Note, search notebooks and documents, create or append Markdown notes, sync conversations, and clip articles through a configured SiYuan API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Hardcoded-token debug or test scripts may expose credentials or encourage reuse of unsafe secrets. <br>
Mitigation: Remove those scripts before installation, rotate any exposed token that may be real, and configure credentials through SIYUAN_API_TOKEN. <br>
Risk: Write-capable sync and document-creation flows can modify a live SiYuan notebook. <br>
Mitigation: Review commands before execution, verify the target notebook and document, and test against a non-sensitive notebook first. <br>
Risk: Conversation sync can persist sensitive chat content into the note system. <br>
Mitigation: Review or redact conversations before syncing and avoid auto-sync for sensitive work. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/jueduilunhui/jueduilunhui-siyuan-note) <br>
- [SiYuan Chrome extension reference](https://github.com/siyuan-note/siyuan-chrome) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact changelog](artifact/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python code examples, shell commands, configuration snippets, and text status messages from SiYuan API operations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a running SiYuan Note instance, python3, requests, SIYUAN_API_TOKEN, and optionally SIYUAN_API_URL.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
