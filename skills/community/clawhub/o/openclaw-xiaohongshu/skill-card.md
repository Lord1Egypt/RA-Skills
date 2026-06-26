## Description: <br>
A Xiaohongshu content and account management skill for publishing and editing notes, reviewing analytics, managing interactions, and updating account settings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaobingan](https://clawhub.ai/user/xiaobingan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, operators, and account managers use this skill to draft, publish, edit, analyze, and manage Xiaohongshu notes and account interactions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can help perform broad account-changing actions such as posting, deleting, replying, blacklisting, profile edits, and account linking. <br>
Mitigation: Require per-action confirmation and review the affected note, comment, user, profile, or linked-account identifiers before execution. <br>
Risk: The skill may access private messages and linked-account data while managing interactions and account settings. <br>
Mitigation: Treat private messages, credentials, and linked-account details as sensitive and avoid exposing them outside the intended workflow. <br>
Risk: Bulk publishing or bulk moderation can affect multiple notes, comments, or users at once. <br>
Mitigation: Preview the full batch, keep default behavior to drafts when possible, and confirm scope before any irreversible or public action. <br>


## Reference(s): <br>
- [Xiaohongshu API Reference](references/API.md) <br>
- [Xiaohongshu Content Guidelines](references/content_guidelines.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with optional shell commands, Python helper code, and JSON-like API payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose account-changing actions that require valid Xiaohongshu credentials and user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
