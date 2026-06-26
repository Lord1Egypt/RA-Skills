## Description: <br>
Skill for interacting with OurGroceries.com to manage shopping lists. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[poedenon](https://clawhub.ai/user/poedenon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and automation agents use this skill to add, retrieve, remove, and synchronize items in an OurGroceries account through text or voice-driven workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires credentials for a live OurGroceries account. <br>
Mitigation: Store OURGROCERIES_EMAIL and OURGROCERIES_PASSWORD in a secure secret store or host environment, and do not commit credential files. <br>
Risk: Shopping-list data and session information may be exposed during debugging. <br>
Mitigation: Avoid enabling debug logs and use the DevTools monitor only in trusted browser sessions with private output handling. <br>
Risk: Remove and delete operations can modify private shopping-list data. <br>
Mitigation: Review target list and item names before executing removal actions, especially when commands are generated from natural language. <br>


## Reference(s): <br>
- [OurGroceries Integration on ClawHub](https://clawhub.ai/poedenon/ourgroceries) <br>
- [poedenon Publisher Profile](https://clawhub.ai/user/poedenon) <br>
- [OurGroceries Website](https://www.ourgroceries.com) <br>
- [OurGroceries API Reference](references/api_reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration guidance] <br>
**Output Format:** [Plain text status messages, optional JSON list output, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OURGROCERIES_EMAIL and OURGROCERIES_PASSWORD credentials at runtime.] <br>

## Skill Version(s): <br>
1.0.2 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
