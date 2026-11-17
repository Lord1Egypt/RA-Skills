## Description:

Sync recordings from Omi AI wearables (Omi, Limitless, etc.) via API and webhooks. Auto-sync transcripts, process recordings, and organize by device/date.

This skill is ready for commercial/non-commercial use.

## Publisher:

[drkavner](https://clawhub.ai/user/drkavner)

### License/Terms of Use:


## Use Case:

Developers and end users use this skill to sync and organize Omi-compatible wearable recordings, transcripts, summaries, and metadata from the Omi API and optional webhooks into local storage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private transcripts, summaries, metadata, and webhook logs are stored locally.

Mitigation: Use the skill only on machines approved for storing sensitive voice data and restrict permissions on recording and configuration directories.

Risk: The webhook endpoint can be exposed publicly and may run without an authentication secret.

Mitigation: Set a strong OMI_WEBHOOK_SECRET before exposing the webhook and avoid public ngrok exposure unless it is required.

Risk: The Omi API key is read from a local file and should be treated as plaintext.

Mitigation: Store the key with owner-only file permissions, rotate it if exposed, and avoid sharing logs or configuration files.

Risk: A configurable self-hosted backend URL can direct sync requests to an unintended service.

Mitigation: Validate any backend URL before use and prefer trusted Omi or organization-controlled endpoints.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/drkavner/skills/omi-integration)
- [Omi developer portal](https://omi.me/developer)
- [Omi project homepage](https://github.com/BasedHardware/omi)
- [ngrok download and setup](https://ngrok.com/download)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local recording files, metadata JSON, transcript text, summary Markdown, logs, and webhook configuration.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
