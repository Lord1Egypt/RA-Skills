## Description:

One Click Posting helps an agent package the same content for Xiaohongshu, X, and Zhihu, then follow a publishing workflow covering preflight checks, explicit user approval, posting, screenshot review, and metrics archival.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lanyasheng](https://clawhub.ai/user/lanyasheng)

### License/Terms of Use:


## Use Case:

Content operators and publishing agents use this skill to turn approved source material into platform-ready publishing packets and manage posting across Xiaohongshu, X, and Zhihu. It emphasizes quality checks, source traceability, explicit approval, screenshot evidence, and post-publication metrics capture.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Public-posting approval gates can be bypassed or fail as documented.

Mitigation: Review the approval workflow before installation, avoid production use of --allow-unapproved, and require downstream publishing steps to independently verify explicit user approval before posting publicly.

Risk: Preflight status may be advisory if the documented command or approval workflow is not enforced.

Mitigation: Treat preflight as a blocking control only after testing the documented command, and separately inspect packet approval and failed-check fields before publishing.

Risk: Unverified source material could be posted as confirmed fact.

Mitigation: Require traceable sources, preserve any pending-verification labels, and perform human review before public posting.

## Reference(s):

- [One Click Posting on ClawHub](https://clawhub.ai/lanyasheng/skills/one-click-posting)
- [发布前后检查清单](references/publish-checklist.md)
- [小红书封面替换 SOP](references/xiaohongshu-cover-sop.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell commands and JSON publishing-packet files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates publishing packets, preflight reports, approval status updates, screenshot and evidence paths, and post-publication metric fields.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
