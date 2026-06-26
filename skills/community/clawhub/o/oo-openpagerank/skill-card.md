## Description: <br>
OpenPageRank helps an agent look up OpenPageRank scores for one or more domains through OOMOL's connected `openpagerank` connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, SEO analysts, and domain researchers use this skill to retrieve normalized OpenPageRank rank metadata for one or more domains through an OOMOL-connected OpenPageRank account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an OOMOL-connected OpenPageRank account and may rely on sensitive credentials managed outside the agent. <br>
Mitigation: Use it only for intended OpenPageRank lookups, connect credentials only when you trust OOMOL and the OpenPageRank integration, and avoid exposing raw API keys in prompts or files. <br>
Risk: First-time setup may require installing the third-party `oo` CLI from a remote installer. <br>
Mitigation: Review the installer or use the official install guide before running setup, and run setup only after an `oo` command fails because the CLI is missing. <br>
Risk: Connector schemas and available actions can change over time. <br>
Mitigation: Inspect the live action schema with `oo connector schema` before constructing payloads, and require explicit user approval before running any action tagged as write or destructive. <br>


## Reference(s): <br>
- [OpenPageRank homepage](https://openpagerank.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OpenPageRank skill page](https://clawhub.ai/oomol/oo-openpagerank) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, JSON, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON connector responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses include connector data and `meta.executionId` when actions are run with `--json`.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
