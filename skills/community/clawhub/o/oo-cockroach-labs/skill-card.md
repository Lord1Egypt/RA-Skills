## Description: <br>
Cockroach Labs lets agents search and read CockroachDB Cloud organization, cluster, node, database, SQL user, and region data through an OOMOL-connected account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect CockroachDB Cloud account resources and run read-only connector actions through the oo CLI when live account data is needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an OOMOL-connected Cockroach Labs account and sensitive credentials. <br>
Mitigation: Install it only for agents that need live CockroachDB Cloud account data, review the OOMOL CLI setup and credential connection flow, and avoid using it for unrelated Cockroach Labs questions. <br>
Risk: Connector calls depend on live action schemas and account permissions. <br>
Mitigation: Inspect each action schema with oo connector schema before building payloads, and handle authentication, scope, connection, or billing errors through the documented setup path. <br>
Risk: Outputs can include organization, cluster, node, database, region, or SQL user metadata from the connected account. <br>
Mitigation: Limit use to authorized contexts and review returned data before sharing it outside the intended workflow. <br>


## Reference(s): <br>
- [ClawHub Cockroach Labs Skill](https://clawhub.ai/oomol/oo-cockroach-labs) <br>
- [Cockroach Labs Homepage](https://www.cockroachlabs.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL CLI Install Guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connector actions return JSON data with execution metadata when invoked.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence release version and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
