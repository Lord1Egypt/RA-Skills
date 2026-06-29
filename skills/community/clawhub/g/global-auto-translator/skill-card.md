## Description: <br>
Global Auto Translator translates copied text and PDF/Word documents across 50+ languages with cross-border commerce terminology support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guo123dong](https://clawhub.ai/user/guo123dong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and operators can use this skill to translate clipboard text and PDF/Word documents for cross-border commerce workflows while preserving trade terminology. Developers and agent users can also run its CLI commands for setup, daemon control, manual translation, document translation, and optional Premium activation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Clipboard text and translated documents may be sent to third-party translation services. <br>
Mitigation: Avoid passwords, API keys, customer data, legal or financial documents, and regulated information; stop the daemon when it is not needed. <br>
Risk: Continuous clipboard monitoring may capture text from unrelated applications. <br>
Mitigation: Configure excluded applications, keep the prompt cooldown enabled, and use manual translation for sensitive workflows. <br>
Risk: The AppleScript display handling has an injection risk when showing untrusted text. <br>
Mitigation: Fix the display escaping before using the skill on untrusted or attacker-controlled text. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/guo123dong/skills/global-auto-translator) <br>
- [DeepL API](https://www.deepl.com/pro-api) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Files, Shell commands, Configuration] <br>
**Output Format:** [Plain text translations, TXT output for PDFs, DOCX output for Word documents, JSON configuration, and CLI status messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May append a trade-term glossary to translated output and may copy translated text back to the clipboard when enabled.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
