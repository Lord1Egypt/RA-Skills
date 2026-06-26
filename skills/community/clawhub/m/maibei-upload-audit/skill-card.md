## Description: <br>
Uploads local or inbound product media to Maibei/MaybeAI, runs the upload audit workflow, generates a visual HTML report, and can share the report through a trycloudflare URL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ojbkxiongdei](https://clawhub.ai/user/ojbkxiongdei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to upload product images or videos to MaybeAI, continue or replay an audit batch, run analysis and audit steps, and return spreadsheet, report, and sharing links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Public report sharing can expose audit reports and nearby local files through an unauthenticated trycloudflare URL. <br>
Mitigation: Run --share only when a public URL is intended, generate the report in a dedicated empty directory, stop the tunnel immediately after use, and avoid production or customer media for testing. <br>
Risk: MaybeAI bearer tokens and user IDs are required and could be exposed through shell history or shared logs. <br>
Mitigation: Use short-lived, least-privileged credentials and avoid placing tokens in commands or logs that may be shared. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ojbkxiongdei/maibei-upload-audit) <br>
- [Maibei Upload Audit Page](https://maibei.maybe.ai/e-commerce/upload-audit-file) <br>
- [MaybeAI Source Audit Spreadsheet](https://www.maybe.ai/docs/spreadsheets/d/69c2400ea25ba20198828d73?gid=0) <br>
- [Protocol Notes](references/protocol-notes.md) <br>
- [Live Run Notes](references/live-run-notes.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Code, Configuration, Files] <br>
**Output Format:** [Markdown progress summaries, optional JSON CLI output, spreadsheet URLs, uploaded media URLs, and self-contained HTML report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a MaybeAI bearer token and user-id; public sharing is optional and uses trycloudflare when requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
