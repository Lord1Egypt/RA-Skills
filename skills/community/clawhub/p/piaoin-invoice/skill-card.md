## Description: <br>
Connects agents to the 票IN/Piaoin PAT invoice API to download and sync collected invoices, save invoice records and files locally, and upload local invoice images or PDFs to Piaoin. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[workopilot](https://clawhub.ai/user/workopilot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, finance operators, and authorized tenant administrators use this skill to retrieve, synchronize, summarize, and upload Piaoin invoice records and files through an agent. It supports personal invoice workflows by default and tenant-wide downloads only when the user is authorized as a tenant administrator. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may handle a Piaoin API key and financial invoice records, and evidence.security notes that these can be stored locally in plaintext. <br>
Mitigation: Prefer a local environment variable or secure secret store for the API key, avoid pasting the key into chat, and add .piaoin_evn and piaoin_invoice/ to .gitignore. <br>
Risk: Tenant-wide downloads can expose invoices beyond the current user's own records. <br>
Mitigation: Use tenant-wide scope only after confirming the user is an authorized tenant administrator; default to current-user downloads when role or scope is unclear. <br>


## Reference(s): <br>
- [票IN PAT API Reference](artifact/references/pat-api.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/workopilot/skills/piaoin-invoice) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files, API calls] <br>
**Output Format:** [Markdown summaries and tables, shell commands, API request guidance, JSONL invoice records, downloaded invoice files, and local configuration entries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local Python mode may create or update .piaoin_evn and piaoin_invoice/ in the user's project directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
