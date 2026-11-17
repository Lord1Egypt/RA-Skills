## Description:

Intelligently translates 50+ languages with trade term recognition and preserves formatting in complex PDF and Word files for cross-border e-commerce.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guo123dong](https://clawhub.ai/user/guo123dong)

### License/Terms of Use:

MIT-0

## Use Case:

Cross-border e-commerce and international trade users use this skill to translate copied text and PDF or Word documents, with support for trade terminology and formatting preservation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Clipboard text and document contents may be sent to third-party translation services.

Mitigation: Avoid passwords, API keys, private chats, legal documents, customer data, and confidential business files unless external translation is acceptable.

Risk: The daemon monitors clipboard content and retains snippets in local state.

Mitigation: Run the daemon only when needed, configure excluded apps, stop it after use, and review local state files under ~/.openclaw/global-auto-translator.

Risk: macOS dialog scripting is identified as unsafe in the security evidence.

Mitigation: Fix the AppleScript handling before routine macOS use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/guo123dong/skills/global-auto-translator)
- [DeepL Pro API](https://www.deepl.com/pro-api)

## Skill Output:

**Output Type(s):** [Text, Files, Shell commands, Configuration guidance]

**Output Format:** [Plain text translations, TXT or DOCX document outputs, and Markdown command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write translated document outputs and local configuration or state under ~/.openclaw/global-auto-translator.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
