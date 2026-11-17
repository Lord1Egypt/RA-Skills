## Description:

Manage Miniflux - Modern minimalist feed reader via REST API. Use for listing feeds and entries, creating/removing subscriptions, searching articles, managing categories, and marking entries as read/unread.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dorogoy](https://clawhub.ai/user/dorogoy)

### License/Terms of Use:


## Use Case:

Developers and feed-reader operators use this skill to manage Miniflux feeds, categories, subscriptions, and entries from an agent through the Miniflux REST API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The README includes a fixed third-party Miniflux URL example that could receive a real API token if copied unchanged.

Mitigation: Set MINIFLUX_URL only to a Miniflux instance you control or explicitly trust, and rotate any token that may have been sent to the wrong host.

Risk: Delete and bulk mark-read commands can change account state without built-in confirmation safeguards.

Mitigation: Confirm feed, category, and entry IDs before invoking account-changing commands, especially delete-feed and bulk mark-read operations.

Risk: The Python dependency is installed separately and may vary by environment.

Mitigation: Install the miniflux Python client in an isolated, pinned environment before using the skill.

## Reference(s):

- [Miniflux API Documentation](https://miniflux.app/docs/api.html)
- [ClawHub Miniflux Skill](https://clawhub.ai/dorogoy/skills/miniflux-skill)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration guidance, API calls]

**Output Format:** [Markdown or plain text responses with shell command examples and Miniflux API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3, MINIFLUX_URL, MINIFLUX_TOKEN, and the Python miniflux client.]

## Skill Version(s):

0.2.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
