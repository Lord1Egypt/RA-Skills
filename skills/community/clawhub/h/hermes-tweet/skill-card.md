## Description: <br>
Use Xquik from Hermes Agent for X search, posting, replies, likes, retweets, follows, DMs, monitors, extraction jobs, draws, media, and trends. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xquik](https://clawhub.ai/user/xquik) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill in Hermes Agent sessions to inspect X/Twitter data and perform controlled Xquik actions such as posting, replies, follows, DMs, monitors, extraction jobs, draws, media operations, and trend checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can support externally visible X/Twitter actions such as posts, replies, likes, retweets, follows, DMs, deletes, monitors, webhooks, extraction jobs, draws, and media operations. <br>
Mitigation: Keep action tools disabled until needed and review the exact endpoint, payload, and user intent before approving any write, private-read, or account-changing operation. <br>
Risk: The skill depends on sensitive Xquik credentials for authenticated reads and actions. <br>
Mitigation: Set XQUIK_API_KEY only in the Hermes runtime environment and never ask for, paste, reveal, log, or pass credentials in chat or tool arguments. <br>
Risk: Runtime permissions depend on the separate Hermes Tweet plugin rather than this skill file alone. <br>
Mitigation: Review the plugin separately for actual runtime permissions before deployment. <br>


## Reference(s): <br>
- [Hermes Tweet on ClawHub](https://clawhub.ai/xquik/hermes-tweet) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON payload examples and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require XQUIK_API_KEY in the Hermes runtime environment; write and private-account actions are gated by HERMES_TWEET_ENABLE_ACTIONS and user approval.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter version 0.1.6) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
