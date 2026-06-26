## Description: <br>
Automates Xiaohongshu browsing and engagement from a logged-in browser session, including likes, saves, follows, and AI-assisted comments under configurable rate limits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yujietech](https://clawhub.ai/user/yujietech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and operators use this skill to run configurable Xiaohongshu account-engagement workflows in an already logged-in Chrome session. The skill supports browsing, filtering targets, generating comments, scheduling runs, switching profiles, and reporting activity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform visible likes, saves, follows, and comments from the user's logged-in Xiaohongshu account. <br>
Mitigation: Require explicit user approval before running engagement workflows and review generated comments before posting when possible. <br>
Risk: Automated social-platform engagement can lead to account restrictions or other platform enforcement. <br>
Mitigation: Use conservative limits, stop on rate-limit or verification prompts, and avoid recurring automation unless the user accepts the account risk. <br>
Risk: Scheduled and multi-account operation can run engagement actions when the user is not actively watching. <br>
Mitigation: Keep scheduling and multi-account features disabled unless explicitly needed, and review configured profiles, quotas, and schedules before enabling them. <br>
Risk: Persistent local activity logs may record account activity details. <br>
Mitigation: Store logs only where the user expects them and periodically review or delete logs according to the user's retention needs. <br>
Risk: The skill includes anti-detection behavior intended to make automated activity appear more natural. <br>
Mitigation: Review the behavior before installation and do not deploy it where such automation violates platform rules or organizational policy. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yujietech/ops-comment) <br>
- [README](README.md) <br>
- [Interaction engine](references/interaction-engine.md) <br>
- [Rate control](references/rate-control.md) <br>
- [Content filters](references/filters.md) <br>
- [Comment generation](references/comment-generation.md) <br>
- [Scheduler](references/scheduler.md) <br>
- [Multi-account](references/multi-account.md) <br>
- [Dashboard](references/dashboard.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown status updates, configuration edits, and activity summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce public social-platform actions from the user's logged-in account and local activity logs.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
