## Description: <br>
ASIN Data API helps agents read, create, update, and delete ASIN Data API data through the OOMOL connector instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and operators use this skill to inspect live ASIN Data API action schemas and run account actions for collections, collection requests, and destinations. It supports read operations, destination updates, and destructive cleanup actions with explicit confirmation for state-changing requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Write and destructive actions can update destinations or delete collection request data in the connected ASIN Data API account. <br>
Mitigation: Confirm the exact action, target identifiers, payload, and expected effect with the user before running actions marked write or destructive. <br>
Risk: The skill requires a connected OOMOL account and ASIN Data API credentials, so expired scopes or missing connections can prevent successful execution. <br>
Mitigation: Use the documented first-time setup only after an auth, scope, or connection error, and avoid handling raw API tokens directly. <br>


## Reference(s): <br>
- [ASIN Data API homepage](https://www.asindataapi.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-asin-data-api) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before actions; write and destructive actions require explicit user confirmation.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence and SKILL.md metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
