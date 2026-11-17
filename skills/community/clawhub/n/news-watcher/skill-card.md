## Description:

OpenClaw News Watcher monitors CoinDesk or PANews for new cryptocurrency articles, summarizes article text in Chinese with an OpenClaw agent, and sends Telegram updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vvxer](https://clawhub.ai/user/vvxer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to monitor cryptocurrency news sources and receive concise Telegram alerts when a new article is detected.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A long-lived browser watcher invokes a local OpenClaw agent and sends Telegram messages.

Mitigation: Run it only in a trusted environment, verify OPENCLAW_MJS points to the intended OpenClaw file, and confirm the Telegram recipient before starting.

Risk: Untrusted web article text is routed through the main OpenClaw agent for summarization.

Mitigation: Prefer a constrained summarization agent and keep tool permissions limited for this workflow.

Risk: Fixed Telegram recipient examples can lead to messages being sent to the wrong account.

Mitigation: Replace examples with the user's own TELEGRAM_USER_ID and avoid committing personal recipient IDs.

Risk: Unpinned dependency ranges can make installs less reproducible.

Mitigation: Pin dependencies and verify the installed Playwright and browser versions before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vvxer/skills/news-watcher)
- [CoinDesk Chinese news](https://www.coindesk.com/zh)
- [PANews Chinese site](https://www.panewslab.com/zh)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text status output and Telegram-ready summary text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OPENCLAW_MJS and TELEGRAM_USER_ID; maintains a local article hash cache.]

## Skill Version(s):

1.0.3 (source: server release metadata and skill.json; package.json lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
