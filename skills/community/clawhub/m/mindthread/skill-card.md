## Description:

Schedule, publish and manage Threads (threads.net) posts through MindThread. Draft posts in the account's voice, publish now or at a set time, queue posts, review cloud-patrol reply drafts, and read views and engagement. Use when the user asks to post, schedule, queue or analyze Threads content, or to review replies waiting for approval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ppcvote](https://clawhub.ai/user/ppcvote)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to help Threads account owners draft, schedule, publish, and manage posts and replies, then review views and engagement. The workflow asks for approval of exact post or reply text before publishing unless the user delegated that decision.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A live API key can authorize publishing, while queued posts and cloud patrol may continue after key revocation.

Mitigation: Start with a test key, restrict live-key permissions, and stop queued posts or cloud patrol separately when needed.

Risk: Publishing with the wrong account, text, or time could send unintended content.

Mitigation: Review the exact text, target account, and publishing time before approving or publishing.

## Reference(s):

- [MindThread CLI project](https://github.com/ppcvote/mindthread-cli)
- [MindThread developer documentation](https://mindthread.tw/developers)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Text, JSON]

**Output Format:** [Markdown instructions, CLI commands, and JSON results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include draft post or reply text for user review before publishing.]

## Skill Version(s):

0.3.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
