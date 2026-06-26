## Description: <br>
Operates Wolfram|Alpha through OOMOL's wolfram_alpha_api connector for short-answer lookup, spoken-style single-sentence results, and query validation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to route Wolfram|Alpha questions through an OOMOL-connected account, inspect the connector schema, and run read-oriented answer or validation actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill documents remote shell installers for the oo CLI, which can be unsafe if executed automatically or without source verification. <br>
Mitigation: Do not let an agent run the remote installer automatically. Install the oo CLI from a trusted official source with version pinning or verification where possible. <br>
Risk: The connector requires a connected Wolfram|Alpha account and sensitive credentials managed through OOMOL. <br>
Mitigation: Connect only the intended Wolfram|Alpha account and avoid exposing raw API keys or unrelated credentials to the agent session. <br>
Risk: Queries and connector responses may be concise and read-oriented but can still be incorrect, incomplete, or costly depending on account state and billing. <br>
Mitigation: Inspect the live connector schema before building payloads, review important answers before relying on them, and stop on billing or connection errors until the user resolves account state. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-wolfram-alpha-api) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>
- [oo CLI repository](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [Wolfram|Alpha API homepage](https://products.wolframalpha.com/api/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON connector payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connector responses are JSON objects with data and meta.executionId fields.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
