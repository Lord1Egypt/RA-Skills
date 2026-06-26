## Description: <br>
Elasticsearch (elastic.co). Use this skill for ANY Elasticsearch request: searching and reading data through the OOMOL Elasticsearch connector instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect Elasticsearch connectivity, list accessible indices, inspect index schemas, and search index data from an OOMOL-connected account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The first-time setup path documents running a remote installer directly in the shell. <br>
Mitigation: Review OOMOL's official install guide or installer contents before running the installer. <br>
Risk: The connector can read or search Elasticsearch data visible to the connected account. <br>
Mitigation: Connect only Elasticsearch credentials and scopes appropriate for the data the agent is allowed to inspect. <br>


## Reference(s): <br>
- [ClawHub Elasticsearch Skill](https://clawhub.ai/oomol/oo-elasticsearch) <br>
- [OOMOL Publisher Profile](https://clawhub.ai/user/oomol) <br>
- [Elasticsearch Homepage](https://www.elastic.co/elasticsearch) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL CLI Install Guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON connector responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs depend on the connected Elasticsearch account and may include index metadata, field statistics, health status, and search results visible to that account.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
