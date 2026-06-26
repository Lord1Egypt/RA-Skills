## Description: <br>
Credit card rewards optimizer that helps agents query 150+ US cards, compare benefits, track a card portfolio, check Chase 5/24 status, and find sign-up bonuses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[troyt-666](https://clawhub.ai/user/troyt-666) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to answer credit-card rewards questions, compare card benefits and offers, maintain a local card portfolio, and check issuer application rules such as Chase 5/24. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup installs and runs the third-party luca-assistant package and initializes card data from external sources. <br>
Mitigation: Install only after trusting the publisher and package source, and run setup in an environment where uv-based tool installation is permitted. <br>
Risk: Portfolio records are stored locally and may include personal card history used for recommendations and 5/24 checks. <br>
Mitigation: Enter only portfolio details needed for the task and manage the local database at ~/.local/share/luca/luca.db according to the user's privacy requirements. <br>
Risk: Credit-card offers, benefits, fees, and issuer rules can become stale or incomplete. <br>
Mitigation: Refresh data with luca_import_cards when needed and avoid fabricating card details when the database has no matching record. <br>


## Reference(s): <br>
- [Luca Assistant GitHub homepage](https://github.com/troyt-666/luca-assistant) <br>
- [Luca Assistant on ClawHub](https://clawhub.ai/troyt-666/luca-assistant) <br>
- [Nitan companion skill on ClawHub](https://clawhub.ai/nitansde/nitan) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON-formatted MCP tool results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a local MCP server and local SQLite database for card data and portfolio records.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
