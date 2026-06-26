## Description: <br>
Paste text, Markdown, or HTML snippets to https://paste.rs and return a shareable URL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[banghasan](https://clawhub.ai/user/banghasan) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and support users use this skill to turn selected text, command output, logs, or configuration snippets into a paste.rs URL for sharing after reviewing the content for sensitive data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Uploaded content is shared through a public paste service. <br>
Mitigation: Review content before upload, keep redaction enabled, and avoid uploading sensitive, proprietary, or regulated data. <br>
Risk: The script saves a local .md copy before uploading. <br>
Mitigation: Choose an appropriate output directory and delete the saved file when a retained local copy is not desired. <br>
Risk: Automatic redaction is heuristic and may miss sensitive values. <br>
Mitigation: Manually inspect logs and configuration snippets before upload, and use --no-redact only for content confirmed to be safe to share. <br>


## Reference(s): <br>
- [paste.rs API quick reference](references/paste-rs-api.md) <br>
- [paste.rs](https://paste.rs) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Plain text URL with Markdown and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled script saves a local .md copy before upload and applies best-effort redaction by default.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
