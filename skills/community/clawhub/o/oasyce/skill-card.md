## Description:

Interact with the Oasyce decentralized AI data marketplace. Register data assets, trade via bonding curves, invoke AI capabilities, and settle payments between agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shangri-la-0428](https://clawhub.ai/user/shangri-la-0428)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agents use this skill to discover, register, trade, and inspect data assets and AI capabilities in the Oasyce marketplace through the oas CLI and Python SDK examples.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill describes marketplace actions that can spend funds, change asset state, or affect disputes and settlements.

Mitigation: Require explicit human approval before buy, sell, dispute, resolve, onboarding, or other value-changing commands.

Risk: The skill recommends installing and invoking external packages and endpoints.

Mitigation: Install only in an isolated environment, verify the package source and version before use, and review any data sent to remote endpoints.

## Reference(s):

- [Oasyce Skill Page](https://clawhub.ai/shangri-la-0428/skills/oasyce)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration]

**Output Format:** [Markdown with inline bash and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands generally request JSON output from the oas CLI.]

## Skill Version(s):

3.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
