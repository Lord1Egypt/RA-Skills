## Description: <br>
Searches Kroger products, finds nearby stores, and helps add selected items to a Kroger cart through the Kroger API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tongyanli-hash](https://clawhub.ai/user/tongyanli-hash) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to search for grocery products, look up Kroger store locations, and prepare cart additions after confirming product selections with the user. <br>

### Deployment Geography for Use: <br>
United States, where Kroger API and store services are available. <br>

## Known Risks and Mitigations: <br>
Risk: The release security summary reports an unsafe input-handling bug that could allow a crafted search term to run local code. <br>
Mitigation: Review scripts/kroger.sh before installation and avoid untrusted pasted grocery lists or unusual search strings until the input handling is fixed. <br>
Risk: The skill can add items to a Kroger cart after OAuth authentication. <br>
Mitigation: Confirm every selected product and quantity with the user before running cart-add commands. <br>
Risk: The skill stores Kroger OAuth tokens locally. <br>
Mitigation: Protect the configured token file and revoke or remove the token when finished. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tongyanli-hash/kroger) <br>
- [Kroger Developer Portal](https://developer.kroger.com) <br>
- [Kroger API base endpoint](https://api.kroger.com/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and CLI text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Kroger API credentials and OAuth authentication; cart additions should be confirmed before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
