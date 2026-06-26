## Description: <br>
Email Assistant triages inboxes, summarizes priority messages, prepares draft replies, manages VIP rules, and produces digest-style briefings without sending mail on the user's behalf. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nollio](https://clawhub.ai/user/nollio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
End users and professionals use this skill to review high-volume inboxes, identify urgent or actionable threads, generate draft replies for review, configure VIP senders, and receive daily or weekly email digests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires broad mailbox visibility to triage email and may read sensitive inbox content. <br>
Mitigation: Use a dedicated or least-privilege email profile where possible, confirm the exact account and folders before first use, and review mailbox scope before enabling routine checks. <br>
Risk: Writing-style analysis can create persistent email-derived profiling data. <br>
Mitigation: Disable historical style analysis unless it is needed, store any writing-style data with restricted permissions, and delete retained profile data when no longer needed. <br>
Risk: The optional dashboard/database path can persist email summaries, draft content, sender information, and digest history. <br>
Mitigation: Avoid enabling the dashboard/database path until privacy notices, retention and deletion controls, and row-level-security write checks are reviewed and tightened. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/nollio/normieclaw-email-assistant) <br>
- [README](artifact/README.md) <br>
- [Security Audit](artifact/SECURITY.md) <br>
- [Skill Instructions](artifact/SKILL.md) <br>
- [Default Email Configuration](artifact/config/email-config.json) <br>
- [Dashboard Specification](artifact/dashboard-kit/DASHBOARD-SPEC.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown briefings and draft replies, JSON configuration updates, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Draft-only email workflow; generated digests and writing-style data may be stored locally when configured] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
