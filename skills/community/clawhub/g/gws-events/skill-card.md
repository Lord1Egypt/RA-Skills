## Description:

Subscribe to Google Workspace events.

This skill is ready for commercial/non-commercial use.

## Publisher:

[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and workspace administrators use this skill to inspect and run Google Workspace Events commands, including subscription creation, deletion, listing, renewal, and reactivation workflows through the gws CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Subscription-management operations can create, delete, update, renew, or reactivate persistent Google Workspace event subscriptions.

Mitigation: Review the shared gws authentication and security guidance, confirm the Google account and scopes, and inspect gws schema output before running state-changing operations.

## Reference(s):

- [Gws Events skill page](https://clawhub.ai/googleworkspace-bot/skills/gws-events)
- [Create a Google Workspace subscription](https://developers.google.com/workspace/events/guides/create-subscription)
- [Delete a Google Workspace subscription](https://developers.google.com/workspace/events/guides/delete-subscription)
- [Get details about a Google Workspace subscription](https://developers.google.com/workspace/events/guides/get-subscription)
- [List Google Workspace subscriptions](https://developers.google.com/workspace/events/guides/list-subscriptions)
- [Update or renew a Google Workspace subscription](https://developers.google.com/workspace/events/guides/update-subscription)
- [Reactivate a Google Workspace subscription](https://developers.google.com/workspace/events/guides/reactivate-subscription)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and command-reference tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the gws CLI and shared gws authentication guidance.]

## Skill Version(s):

1.0.12 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
