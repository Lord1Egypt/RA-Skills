## Description: <br>
Manage a HelloFresh subscription, discover and select recipes, convert cooking instructions to audio, track shipments, and receive delivery notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guillaumemaka](https://clawhub.ai/user/guillaumemaka) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
HelloFresh subscribers use this skill to manage meal planning workflows from an agent: setup, subscription status, recipe discovery, meal selection, order history, recommendations, instruction audio, shipment tracking, and notification settings. <br>

### Deployment Geography for Use: <br>
Canada <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles private HelloFresh account, subscription, delivery, and preference data. <br>
Mitigation: Install only in environments where that account data can be handled, and use the reset command or remove the local session file when access should be cleared. <br>
Risk: Cloud browser mode can expose loaded HelloFresh account pages to Kernel cloud infrastructure. <br>
Mitigation: Prefer local browser mode unless the user explicitly trusts Kernel for the account pages being loaded and has configured the Kernel API key intentionally. <br>
Risk: Meal-selection or subscription actions can affect upcoming deliveries. <br>
Mitigation: Review meal-selection changes in the browser before saving or confirming them. <br>
Risk: Shipment alerts can send delivery-status information through Telegram when notifications are enabled. <br>
Mitigation: Enable alerts only when the notification channel is acceptable for delivery details, and disable notifications when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub Hellofresh skill page](https://clawhub.ai/guillaumemaka/hellofresh) <br>
- [HelloFresh Canada](https://www.hellofresh.ca) <br>
- [Kernel dashboard](https://dashboard.onkernel.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Audio, Configuration, Files] <br>
**Output Format:** [Agent command responses, optional text-to-speech audio, and local JSON session or recipe state.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a logged-in browser session and may store subscription, preference, notification, and cached recipe data locally.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
