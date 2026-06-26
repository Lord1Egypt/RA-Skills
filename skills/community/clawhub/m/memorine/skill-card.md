## Description: <br>
Human-like memory for AI agents. Facts, events, procedures, contradiction detection, forgetting curve, and cross-agent sharing. Pure Python + SQLite. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[osvfelices](https://clawhub.ai/user/osvfelices) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use Memorine to give OpenClaw agents persistent local memory for facts, events, procedures, contradiction checks, and shared team knowledge. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stored and shared memories can contain long-lived sensitive data. <br>
Mitigation: Avoid storing secrets, credentials, regulated data, or private customer information unless filesystem protections, backups, deletion procedures, and access boundaries are in place. <br>
Risk: Team or cross-agent memory sharing can expose information to agents that should not receive it. <br>
Mitigation: Use separate databases or namespaces for users, teams, tenants, or agents that require isolation. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/osvfelices/memorine) <br>
- [Project Homepage](https://github.com/osvfelices/memorine) <br>
- [PyPI Project](https://pypi.org/project/memorine/) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, guidance] <br>
**Output Format:** [MCP tool responses and OpenClaw configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Persists agent memories in a local SQLite database; optional extras can add semantic search or a terminal dashboard.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata; artifact frontmatter declares 0.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
