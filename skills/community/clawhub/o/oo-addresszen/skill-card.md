## Description: <br>
AddressZen helps agents search AddressZen address suggestions, retrieve USA-formatted address details, and check key availability through the OOMOL oo CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query AddressZen through an OOMOL-connected account for address autocomplete, USA address retrieval, and key availability checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an OOMOL-connected AddressZen account and may depend on sensitive credentials managed outside the agent. <br>
Mitigation: Use OOMOL server-side credential injection and do not expose raw AddressZen credentials in prompts, files, or command payloads. <br>
Risk: First-time setup can install or invoke the OOMOL CLI and connect external services. <br>
Mitigation: Verify the OOMOL CLI installer source before installation and run setup only when an auth or connection error requires it. <br>
Risk: Address queries, connection status, and billing or credit state are sent to external services. <br>
Mitigation: Use the skill only for intended AddressZen workflows and confirm that the user accepts external service and billing implications before retrying failed requests. <br>


## Reference(s): <br>
- [ClawHub AddressZen Skill](https://clawhub.ai/oomol/oo-addresszen) <br>
- [AddressZen](https://addresszen.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL CLI Install Guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connector responses are JSON wrappers that include data and meta.executionId.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
