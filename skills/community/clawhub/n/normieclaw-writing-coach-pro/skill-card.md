## Description: <br>
Writing Coach Pro helps an OpenClaw agent review, rewrite, and coach writing for grammar, style, tone, readability, consistency, and user-specific preferences. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nollio](https://clawhub.ai/user/nollio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Writers, editors, and teams use this skill inside OpenClaw to check grammar, polish drafts, analyze readability, enforce a style profile, and learn from recurring writing feedback. It is suited to emails, reports, blog posts, technical prose, academic writing, and other documents where consistency and tone matter. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Saved writing history, preferences, issue descriptions, and text excerpts can include personal or sensitive information. <br>
Mitigation: Protect the local data directory like personal files, delete stored analysis data when it is no longer needed, and use a local LLM for sensitive documents. <br>
Risk: Submitted text is processed by whichever LLM backend the user's OpenClaw agent is configured to use. <br>
Mitigation: Review the selected LLM provider's data handling policies before processing sensitive text, or configure a local model. <br>
Risk: Optional dashboard reporting may sync derived writing stats and issue data if installed. <br>
Mitigation: Review dashboard settings before relying on sync, and disable dashboard reporting when local-only use is required. <br>
Risk: Cleanup commands can remove locally stored writing analysis data. <br>
Mitigation: Verify the target data path carefully before running cleanup commands. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/nollio/normieclaw-writing-coach-pro) <br>
- [README](artifact/README.md) <br>
- [Security notes](artifact/SECURITY.md) <br>
- [Setup guide](artifact/SETUP-PROMPT.md) <br>
- [Dashboard specification](artifact/dashboard-kit/DASHBOARD-SPEC.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, inline corrections, rewritten prose, coaching explanations, and setup or export commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local style profiles, learning logs, session summaries, exported reports, and optional dashboard records when installed.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
