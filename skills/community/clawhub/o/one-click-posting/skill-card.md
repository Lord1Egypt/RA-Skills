## Description: <br>
One Click Posting packages a post for Xiaohongshu, X, and Zhihu, runs preflight and approval gates, and records publication evidence and follow-up metrics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lanyasheng](https://clawhub.ai/user/lanyasheng) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and operators use this skill to turn prepared content into approval-gated publishing packets for Xiaohongshu, X, and Zhihu, then track publication status, screenshots, links, and first-hour metrics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow prepares public posts and could publish or update content before the user has approved it. <br>
Mitigation: Require a fresh explicit confirmation before any platform publish or update action, and keep approval gates enabled in preflight. <br>
Risk: Unverified or misleading claims could be packaged into public content. <br>
Mitigation: Keep sources traceable, mark unverified information clearly, and complete content and risk review before publication. <br>
Risk: Publication records could become unreliable if screenshots, links, or platform receipts are missing or fabricated. <br>
Mitigation: Retain local publishing packets, screenshots, links or IDs, and follow-up metrics, and do not report a publication result without evidence. <br>


## Reference(s): <br>
- [One Click Posting on ClawHub](https://clawhub.ai/lanyasheng/one-click-posting) <br>
- [Publish Checklist](references/publish-checklist.md) <br>
- [Xiaohongshu Cover SOP](references/xiaohongshu-cover-sop.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown status summaries, shell command guidance, and JSON publishing packet files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit user approval before live posting and retains local packet, screenshot, and archive paths.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
