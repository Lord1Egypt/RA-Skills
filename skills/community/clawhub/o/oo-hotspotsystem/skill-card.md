## Description: <br>
HotspotSystem helps an agent inspect a connected HotspotSystem operator account and retrieve location, customer, and subscriber records through the OOMOL `oo` CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External operators and support agents use this skill to verify a connected HotspotSystem account and look up locations, customers, and subscribers for operational support workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires connected HotspotSystem credentials and can surface account, location, customer, or subscriber records to the agent. <br>
Mitigation: Install only for intended HotspotSystem workflows and review the exact command target before approving account-access actions. <br>
Risk: Setup and billing recovery commands can affect local CLI authentication state or route users into external account-management flows. <br>
Mitigation: Run setup or recovery steps only after the matching authentication, connection, or billing error occurs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-hotspotsystem) <br>
- [Publisher profile](https://clawhub.ai/user/oomol) <br>
- [HotspotSystem homepage](https://www.hotspotsystem.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands can return JSON responses from the `oo` CLI when run with `--json`.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
