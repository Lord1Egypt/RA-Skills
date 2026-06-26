## Description: <br>
Manage grocery shopping on Knuspr.de via knuspr-cli for product search, cart management, delivery slot reservations, shopping lists, order history, deals, favorites, and meal suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Lars147](https://clawhub.ai/user/Lars147) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and agent operators use this skill to search groceries, manage carts and shopping lists, reserve delivery slots, and review order history on Knuspr.de while leaving checkout to the user. <br>

### Deployment Geography for Use: <br>
Germany <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access a user's Knuspr account and modify carts, lists, favorites, and delivery reservations. <br>
Mitigation: Install only when account access is acceptable, require confirmation before destructive actions, and personally review the cart and checkout in Knuspr before buying. <br>
Risk: Account credentials or the local credential file could expose Knuspr account access if handled loosely. <br>
Mitigation: Prefer interactive login, avoid passing passwords on the command line, tightly protect ~/.knuspr_credentials.json if used, and log out when finished. <br>
Risk: The CLI is an unofficial Knuspr/Rohlik integration and may stop working or return unexpected results if the service changes. <br>
Mitigation: Verify prices, cart contents, delivery reservations, and checkout details directly in Knuspr before placing an order. <br>


## Reference(s): <br>
- [README](README.md) <br>
- [Full Command Reference](references/commands.md) <br>
- [Knuspr.de](https://www.knuspr.de) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with CLI commands and JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Use --json for programmatic parsing; destructive actions and checkout require user review.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata and pyproject.toml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
