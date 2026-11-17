## Description:

Monitor web pages for content changes and get alerts. Track URLs, detect updates, view diffs. Use when asked to watch a website, track changes on a page, monitor for new posts/content, set up page change alerts, or check if a site has been updated. Supports CSS selectors for targeted monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[corbin-breton](https://clawhub.ai/user/corbin-breton)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and operations teams use this skill to watch web pages for content changes, narrow checks with CSS selectors, and review diffs or snapshots for updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch arbitrary monitored URLs, including local or internal network targets.

Mitigation: Only monitor URLs that are intentionally in scope, and avoid file:, localhost, private-network, cloud-metadata, authenticated, confidential, or proprietary pages.

Risk: Fetched page text and diffs are persisted on disk.

Mitigation: Set and protect WEB_MONITOR_DIR appropriately, and avoid monitoring pages whose stored content should not be retained.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/corbin-breton/skills/keats-web-monitor)
- [Publisher profile](https://clawhub.ai/user/corbin-breton)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can store watch configuration, page snapshots, and diffs on disk.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
