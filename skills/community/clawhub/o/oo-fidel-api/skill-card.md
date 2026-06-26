## Description: <br>
Fidel API (fidel.uk). Use this skill for ANY Fidel API request - searching and reading data through the OOMOL Fidel API connector instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to inspect Fidel API action schemas and run read-only brand, card, and transaction lookup actions through an OOMOL-connected account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires OOMOL-managed credentials that can read Fidel API data such as brands, cards, and transactions. <br>
Mitigation: Confirm the connected Fidel API key has only the intended scopes before use. <br>
Risk: Future connector actions may include write or destructive behavior even though the current release is described as read-only. <br>
Mitigation: Review any connector action tagged write or destructive and get explicit user approval before running it. <br>
Risk: Incorrect request payloads can lead to failed or unintended API calls. <br>
Mitigation: Inspect the live action schema with `oo connector schema` before building each payload. <br>


## Reference(s): <br>
- [Fidel API homepage](https://fidel.uk) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-fidel-api) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schema inspection before constructing request payloads; responses are returned as JSON from the oo CLI.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
