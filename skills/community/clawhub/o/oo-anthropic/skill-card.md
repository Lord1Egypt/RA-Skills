## Description: <br>
Operate Anthropic through an OOMOL-connected account using the oo CLI connector for message creation, token counting, and model metadata actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to inspect Anthropic connector schemas, run supported Anthropic actions through OOMOL, count message tokens, create non-streaming messages, and retrieve model information. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Anthropic prompts and payloads may be sent through OOMOL and Anthropic when connector actions run. <br>
Mitigation: Install and use the skill only when that intermediary flow is acceptable, and review payload content before approving actions. <br>
Risk: The create_message action can consume account credits and send user-provided prompt content. <br>
Mitigation: Confirm the exact payload and intended effect with the user before running create_message. <br>
Risk: Broad Anthropic-related wording could cause general discussion or documentation requests to be treated as connector actions. <br>
Mitigation: Use the connector only for explicit Anthropic account actions and answer general Anthropic questions without running oo commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-anthropic) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [Anthropic homepage](https://www.anthropic.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON connector responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connector responses include data and meta.executionId fields when actions run successfully.] <br>

## Skill Version(s): <br>
1.0.2 (source: release evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
