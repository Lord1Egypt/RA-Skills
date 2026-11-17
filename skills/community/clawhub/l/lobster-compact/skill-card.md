## Description:

Summarize long conversations to preserve context. Automatically triggered when context window approaches limits, or manually with /compact.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangxiaofei860208-source](https://clawhub.ai/user/wangxiaofei860208-source)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to compact long agent conversations into structured summaries so work can continue with preserved context. It can also save selected long-term context into memory files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conversation summaries may include sensitive, secret, or personal information from broad chat history.

Mitigation: Require explicit approval before saving memory and redact secrets and personal data from summaries.

Risk: Persistent memory entries can retain context longer than users expect.

Mitigation: Provide a clear way to review and delete saved memory entries and limit what is stored to necessary long-term context.

Risk: Untrusted instructions from prior conversation content may be preserved as actionable context.

Mitigation: Quote or label untrusted instructions in summaries so future agents treat them as evidence, not commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangxiaofei860208-source/skills/lobster-compact)
- [Publisher profile](https://clawhub.ai/user/wangxiaofei860208-source)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Markdown summary with optional memory file updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summary sections cover requests, technical context, files, errors, feedback, tasks, current work, and next steps.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
