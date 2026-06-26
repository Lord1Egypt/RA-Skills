## Description: <br>
Manage Grocy inventory, shopping lists, batteries, and barcode-based stock operations against a local Grocy instance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[septianw](https://clawhub.ai/user/septianw) <br>

### License/Terms of Use: <br>


## Use Case: <br>
People who run a local Grocy instance use this skill to check pantry or fridge stock, inspect expiring products, update stock by barcode, and track rechargeable batteries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes an embedded Grocy API key in its configuration examples. <br>
Mitigation: Replace it with a securely supplied Grocy key before use and rotate the exposed key if it was ever valid. <br>
Risk: The documented commands can consume, open, and transfer inventory items or record battery charging. <br>
Mitigation: Confirm the barcode, amount, source and destination locations, and battery ID before running write commands. <br>


## Reference(s): <br>
- [Grocy API Reference](references/grocy-api.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash command examples and JSON API payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Grocy base URL and API key; write commands can modify inventory and battery records.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
