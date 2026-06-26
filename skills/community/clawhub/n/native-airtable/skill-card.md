## Description: <br>
Read Airtable bases, tables, and records directly via the Airtable API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codeninja23](https://clawhub.ai/user/codeninja23) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to inspect Airtable bases, table schemas, and records from an agent workflow. It supports read-only lookup, filtering, field selection, view selection, and record search through Airtable's official API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A broadly scoped Airtable Personal Access Token could expose more bases or records than the workflow needs. <br>
Mitigation: Use a dedicated token with only the documented read scopes and grant access only to the required bases. <br>
Risk: The security evidence notes a search escaping bug when untrusted text is used in search queries or field names. <br>
Mitigation: Avoid untrusted search input until formula escaping is fixed, or use explicit filters controlled by the user. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/codeninja23/native-airtable) <br>
- [Airtable token creation](https://airtable.com/create/tokens) <br>
- [Airtable REST API endpoint](https://api.airtable.com/v0) <br>
- [Airtable metadata API endpoint](https://api.airtable.com/v0/meta) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown instructions with shell command examples; command output is text, tab-separated summaries, or JSON records.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AIRTABLE_PAT and python3; reads data from Airtable using the official API.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
