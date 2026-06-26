## Description: <br>
Google BigQuery (cloud.google.com). Use this skill for ANY Google BigQuery request - reading, creating, updating, and deleting data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data teams use this skill to let an agent inspect BigQuery schemas, run queries, and manage datasets, tables, routines, models, jobs, and table data through an OOMOL-connected account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and change BigQuery resources using the connected OOMOL account. <br>
Mitigation: Review the Google account and project permissions before installation, and confirm the exact payload and effect before write actions. <br>
Risk: Destructive actions can remove datasets, tables, routines, or models. <br>
Mitigation: Require explicit approval for destructive actions and verify the target project, dataset, and resource before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-google-bigquery) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>
- [Google BigQuery homepage](https://cloud.google.com/bigquery) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connector responses are JSON when actions are run with the documented --json flag.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
