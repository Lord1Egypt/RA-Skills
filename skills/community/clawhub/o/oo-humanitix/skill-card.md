## Description: <br>
Humanitix lets an agent read Humanitix event data and account tags through an OOMOL-connected Humanitix account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and operators use this skill to retrieve Humanitix event details, list accessible events, and list account tags from a connected Humanitix account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a connected Humanitix account and sensitive credentials managed through OOMOL. <br>
Mitigation: Review the requested account access in ClawHub and connect only the Humanitix account needed for the intended use. <br>
Risk: Connector schemas and available account data can vary by connection state, scope, or credential expiry. <br>
Mitigation: Inspect the live connector schema before running an action and reconnect or refresh credentials only when an authentication or scope error occurs. <br>


## Reference(s): <br>
- [Humanitix ClawHub listing](https://clawhub.ai/oomol/oo-humanitix) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>
- [Humanitix homepage](https://humanitix.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses may include Humanitix connector command output returned as JSON.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
