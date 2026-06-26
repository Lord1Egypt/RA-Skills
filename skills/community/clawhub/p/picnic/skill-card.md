## Description: <br>
Order groceries from Picnic supermarket - search products, manage cart, schedule delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mpociot](https://clawhub.ai/user/mpociot) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agent operators use this skill to search Picnic products, inspect user and delivery information, manage a Picnic shopping cart, and choose available delivery slots through a JSON-emitting CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Picnic account access and stores an auth key in a local config file. <br>
Mitigation: Avoid exposing login commands in terminals or transcripts, protect ~/.config/picnic/config.json as a sensitive credential file, and remove the config when access is no longer needed. <br>
Risk: The CLI can modify the shopping cart and select delivery slots. <br>
Mitigation: Confirm with the user before adding or removing items, clearing the cart, or setting a delivery slot. <br>
Risk: Commands can return personal details, address, delivery history, and order contents. <br>
Mitigation: Limit command output shared in logs or transcripts and avoid running the bundled debug helper. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON] <br>
**Output Format:** [JSON responses from CLI commands, with setup and command guidance in Markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Picnic account credentials and stores local configuration under ~/.config/picnic/config.json.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
