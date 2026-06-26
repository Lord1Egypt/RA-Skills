## Description: <br>
Globalping handles Globalping requests through OOMOL, including reading, creating, and updating data instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to run Globalping connector actions through an OOMOL-connected account, including creating measurements, retrieving measurement status and results, checking account limits, and listing online probes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create Globalping measurements through an OOMOL-connected account. <br>
Mitigation: Confirm the exact create_measurement payload and expected effect with the user before execution. <br>
Risk: The skill depends on OOMOL as the broker for Globalping access and may use connected account credentials. <br>
Mitigation: Install it only when OOMOL brokerage is intended, review the OOMOL CLI install command, and connect only the expected Globalping account and scopes. <br>
Risk: Connector action schemas can change over time. <br>
Mitigation: Inspect the live connector schema before constructing or running an action payload. <br>


## Reference(s): <br>
- [Globalping homepage](https://globalping.io) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-globalping) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return connector JSON responses that include action data and an execution ID.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
