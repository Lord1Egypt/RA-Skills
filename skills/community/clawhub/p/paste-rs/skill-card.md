## Description:

Paste text, Markdown, or HTML snippets to https://paste.rs and return a shareable URL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[banghasan](https://clawhub.ai/user/banghasan)

### License/Terms of Use:


## Use Case:

External users, developers, and agents use this skill to publish short text, Markdown, HTML, logs, configuration snippets, or command output to paste.rs as a shareable URL. It is appropriate only for content that may be public.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Pasted content is sent to a public third-party service.

Mitigation: Use the skill only for content that may be public; review snippets before upload and avoid secrets, private files, and sensitive logs.

Risk: The bundled script saves a local Markdown copy before uploading and defaults to shared /tmp with predictable filenames.

Mitigation: Use a private output directory with --outdir and remove saved paste files after use.

Risk: Automatic redaction is heuristic and can be disabled with --no-redact.

Mitigation: Manually inspect and redact content before upload, and avoid --no-redact for logs, configs, credentials, or other sensitive material.

## Reference(s):

- [paste.rs API quick reference](references/paste-rs-api.md)
- [paste.rs](https://paste.rs)
- [ClawHub skill page](https://clawhub.ai/banghasan/skills/paste-rs)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance with shell command examples; script output is a paste.rs URL on stdout and a saved local Markdown path on stderr.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uploads user-provided content to paste.rs, writes a local .md copy before upload, and applies best-effort redaction unless --no-redact is used.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
