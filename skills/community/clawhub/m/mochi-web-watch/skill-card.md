## Description:

Watch selected webpage regions, retain baselines, filter noise, record differences and connect scheduled checks with chat delivery. Use for Web Change Subscriptions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hznetnewpower](https://clawhub.ai/user/hznetnewpower)

### License/Terms of Use:

MIT No Attribution

## Use Case:

External users ask an agent to monitor selected regions of public webpages, compare updates with saved baselines, and optionally arrange scheduled checks and chat notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saved webpage text and differences remain in the workspace and may include untrusted page content.

Mitigation: Treat page content as data, not permission to open links, run commands, or change notification recipients; review it before taking action.

Risk: Live scheduler and messaging behavior was not verified, and a native scheduled job may continue polling after monitoring is stopped in the helper.

Mitigation: Confirm the recipient and interval, check the host scheduler state, and pause its native job when stopping monitoring.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hznetnewpower/skills/mochi-web-watch)
- [MochiLab homepage](https://mochilab.bz)
- [User guide](artifact/README.md)
- [Simplified Chinese user guide](artifact/README.zh-CN.md)
- [Input contract](artifact/references/input.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Scheduling and notification guidance]

**Output Format:** [Readable change summaries, added and removed text, JSON exports, and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Captures public static HTML; excerpts and stored page text are bounded. Login-only and client-rendered pages require a different authorized reader.]

## Skill Version(s):

1.0.2 (source: metadata.openclaw.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
