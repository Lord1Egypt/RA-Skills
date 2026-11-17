## Description:

End-to-end Xiaohongshu operations including positioning, topic research, content production, publish execution, and post-incident recovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zarflan](https://clawhub.ai/user/zarflan)

### License/Terms of Use:

MIT-0

## Use Case:

External users, creators, and operations teams use this skill to plan, draft, publish, and review Xiaohongshu content across reusable account workflows. It also supports creator-platform login recovery, comment handling, visibility controls, scheduled publishing, and failure recovery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish content to a live Xiaohongshu creator account.

Mitigation: Use dry-run or private visibility first, require explicit user intent before publishing, and confirm publication through the note manager rather than relying on a single success flag.

Risk: Reusable Xiaohongshu login state is saved in plaintext.

Mitigation: Treat ~/.openclaw/workspace/xhs_user_info.json as a credential, restrict file sharing, and avoid exposing logs or screenshots that include session paths, account state, or tokens.

Risk: OpenClaw gateway setup may expose local tokens or broaden local automation access.

Mitigation: Use the gateway only on trusted machines, protect gateway tokens, and review device or pairing prompts before approving access.

Risk: Fallback publishing scripts may behave differently from the primary validated flow.

Mitigation: Prefer the primary saved-session publish scripts and review the current creator-platform page state before using hard or draft fallback publishers.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zarflan/skills/luan-xhs-skill)
- [XHS Publish Flows](artifact/references/xhs-publish-flows.md)
- [XHS Comment Ops](artifact/references/xhs-comment-ops.md)
- [XHS Runtime Rules](artifact/references/xhs-runtime-rules.md)
- [XHS Evaluation Patterns](artifact/references/xhs-eval-patterns.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with publish-ready copy, reply text, command examples, and script usage.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Xiaohongshu titles, body copy, comment replies, operational SOPs, browser automation commands, visibility settings, schedule settings, and generated cover image paths.]

## Skill Version(s):

0.2.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
