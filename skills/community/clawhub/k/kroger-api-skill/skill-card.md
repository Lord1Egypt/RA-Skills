## Description: <br>
Search Kroger/QFC products, manage a local cart, check pickup availability, and create pickup orders through the official Kroger API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jasonahorn](https://clawhub.ai/user/jasonahorn) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to search Kroger/QFC catalog data, locate stores, manage grocery items, check pickup availability, and submit pickup orders after OAuth setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create real Kroger/QFC pickup orders. <br>
Mitigation: Require the agent to show the exact items, quantities, store, pickup time, and order impact before running any order-create command. <br>
Risk: OAuth credentials and reusable account tokens are stored in a local plaintext state file. <br>
Mitigation: Keep state.json private, exclude it from version control, and use the skill only when granting Kroger OAuth access is acceptable. <br>


## Reference(s): <br>
- [Kroger Developer Portal](https://developer.kroger.com) <br>
- [Kroger API Reference](https://developer.kroger.com/reference) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Configuration guidance, Text] <br>
**Output Format:** [Markdown instructions with shell commands; command results are JSON or short status text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Kroger OAuth credentials and a local state file for tokens, cart contents, and selected location.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
