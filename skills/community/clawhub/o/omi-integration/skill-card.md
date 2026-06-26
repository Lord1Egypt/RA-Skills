## Description: <br>
Sync recordings from Omi AI wearables (Omi, Limitless, etc.) via API and webhooks. Auto-sync transcripts, process recordings, and organize by device/date. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[drkavner](https://clawhub.ai/user/drkavner) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to sync, list, and process recordings and transcripts from Omi-compatible wearables through the Omi API or webhook events, storing outputs locally for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive Omi recordings and transcripts on the local machine. <br>
Mitigation: Install only where local storage is acceptable, protect or encrypt ~/omi_recordings, and restrict access to transcript, metadata, summary, and log files. <br>
Risk: Webhook exposure can receive voice transcript events over a public endpoint if ngrok or another tunnel is used. <br>
Mitigation: Set a strong OMI_WEBHOOK_SECRET before exposing the webhook and avoid public ngrok exposure unless needed. <br>
Risk: API keys or captured voice data may be exposed through local files or logs. <br>
Mitigation: Keep ~/.config/omi/api_key permission-restricted, rotate the API key if exposed, and review logs before sharing diagnostics. <br>
Risk: The documentation claims API key encryption, but security evidence says to treat that claim as inaccurate. <br>
Mitigation: Do not rely on built-in encryption; use OS-level secret storage or filesystem encryption if stronger credential protection is required. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/drkavner/omi-integration) <br>
- [Omi Developer Portal](https://omi.me/developer) <br>
- [Omi API Base Endpoint](https://api.omi.me/v1) <br>
- [ngrok](https://ngrok.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated local JSON, text, and Markdown files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores synced recordings, transcripts, summaries, metadata, logs, and indexes under ~/omi_recordings/.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
