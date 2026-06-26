## Description: <br>
Subscribe to Google Workspace events. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and workspace administrators use this skill to discover and run Google Workspace Events commands for creating, listing, updating, renewing, reactivating, deleting, and streaming event subscriptions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Commands can create, patch, reactivate, renew, or delete Google Workspace event subscriptions. <br>
Mitigation: Confirm the active Google account and scopes, inspect each method with gws schema, and require explicit approval before account-changing operations. <br>
Risk: The skill depends on a local gws CLI and shared authentication guidance that are not bundled in this artifact. <br>
Mitigation: Install gws from a trusted source and review the shared auth and security skill before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/gws-events) <br>
- [Publisher profile](https://clawhub.ai/user/googleworkspace-bot) <br>
- [Create a Google Workspace subscription](https://developers.google.com/workspace/events/guides/create-subscription) <br>
- [Delete a Google Workspace subscription](https://developers.google.com/workspace/events/guides/delete-subscription) <br>
- [Get details about a Google Workspace subscription](https://developers.google.com/workspace/events/guides/get-subscription) <br>
- [List Google Workspace subscriptions](https://developers.google.com/workspace/events/guides/list-subscriptions) <br>
- [Update or renew a Google Workspace subscription](https://developers.google.com/workspace/events/guides/update-subscription) <br>
- [Reactivate a Google Workspace subscription](https://developers.google.com/workspace/events/guides/reactivate-subscription) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the gws CLI and may produce or guide NDJSON event streams when subscription streaming commands are used.] <br>

## Skill Version(s): <br>
1.0.12 (source: server release metadata; artifact metadata version 0.22.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
