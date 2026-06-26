## Description: <br>
AgentQL (agentql.com) supports reading, creating, and updating AgentQL data through the OOMOL-connected oo CLI instead of direct API calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to operate AgentQL through an OOMOL-connected account, inspect live connector schemas, query webpages for structured data, create remote browser sessions, and review usage telemetry. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: First-time setup includes remote installer commands, including pipe-to-shell and PowerShell execution patterns. <br>
Mitigation: Use verified OOMOL CLI documentation, review the installer before execution, and require explicit approval before running installer commands. <br>
Risk: The skill operates through an OOMOL-connected AgentQL account and may use sensitive credentials supplied server-side. <br>
Mitigation: Install only for intended OOMOL and AgentQL use, keep account access scoped appropriately, and confirm payloads before running write actions. <br>


## Reference(s): <br>
- [AgentQL homepage](https://www.agentql.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [ClawHub AgentQL release page](https://clawhub.ai/oomol/oo-agentql) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API calls, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON connector responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the oo CLI, an OOMOL sign-in, and an AgentQL connection for live actions.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
