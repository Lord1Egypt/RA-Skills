## Description: <br>
Imports CSV/XLSX accounting data into QuickBooks Online or Xero through the Synder Importer REST API, including field mapping, file upload, import execution, status polling, and result retrieval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MichaelAstreikoSynder](https://clawhub.ai/user/MichaelAstreikoSynder) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and finance operators use this skill to prepare and execute spreadsheet imports into connected QuickBooks Online or Xero companies through the Synder Importer API. It supports validating fields and mappings, dry-run previews, live imports, polling, and results review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can send accounting spreadsheets to Synder Importer and connected QuickBooks Online or Xero companies. <br>
Mitigation: Use the skill only for intended accounting imports, confirm the connected company before import, and use a revocable IMPORTER_API_TOKEN. <br>
Risk: Live import actions, settings changes, mapping deletion, cancellation, and revert operations can change accounting data or workflow state. <br>
Mitigation: Start with dryRun=true, review proposed mappings and target company details, and require explicit approval before dryRun=false or other state-changing operations. <br>
Risk: Incorrect date formats, required-field mappings, or medium-confidence auto-matches can cause failed or inaccurate imports. <br>
Mitigation: Check company settings and required entity fields, review medium-confidence matches, and inspect import results and errors after each run. <br>


## Reference(s): <br>
- [Synder Importer API full reference](references/api.md) <br>
- [Synder Importer API docs](https://importer.synder.com/apidocs) <br>
- [Synder Importer service](https://importer.synder.com) <br>
- [ClawHub skill page](https://clawhub.ai/MichaelAstreikoSynder/gl-importer) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces import workflow instructions, curl commands, mapping guidance, and result-checking steps; it does not export accounting data from QuickBooks Online or Xero.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
