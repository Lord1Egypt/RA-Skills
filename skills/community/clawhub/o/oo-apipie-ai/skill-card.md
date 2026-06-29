## Description: <br>
APIpie AI (apipie.ai). Use this skill for ANY APIpie AI request: reading, creating, and updating data through the OOMOL `oo` CLI connector instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to operate APIpie AI through an OOMOL-connected account, including non-streaming chat completions, embedding generation, model listing, and detailed model metadata lookup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Chat completion and embedding payloads can transmit user-provided text to APIpie AI through OOMOL. <br>
Mitigation: Review and redact payloads before approval, especially when they may contain sensitive, confidential, or regulated information. <br>
Risk: API calls may consume APIpie or OOMOL credits. <br>
Mitigation: Confirm the intended action and payload before running write-tagged actions, and check billing or credit errors before retrying. <br>
Risk: Connector inputs can drift from remembered examples. <br>
Mitigation: Inspect the live action schema with `oo connector schema` before constructing each JSON payload. <br>


## Reference(s): <br>
- [APIpie AI homepage](https://apipie.ai) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-apipie-ai) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before constructing action payloads.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md metadata and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
