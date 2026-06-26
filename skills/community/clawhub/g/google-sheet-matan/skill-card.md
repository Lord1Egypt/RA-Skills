## Description: <br>
Interact with Google Sheets through Maton Gateway to read, write, append, clear, format, and manage spreadsheet data using authenticated curl requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[otman-ai](https://clawhub.ai/user/otman-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to prepare Google Sheets API requests through Maton Gateway for spreadsheet reads, edits, appends, clearing, formatting, sheet management, formulas, and protected ranges. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Maton API keys and OAuth authorization headers can expose access to spreadsheets if copied into logs, prompts, or shared output. <br>
Mitigation: Keep MATON_API_KEY secret, avoid printing populated Authorization headers, and use the narrowest available permissions. <br>
Risk: Write, clear, delete, and batchUpdate examples can make destructive or unintended spreadsheet changes. <br>
Mitigation: Manually verify spreadsheet IDs, ranges, clear and delete commands, and batchUpdate payloads before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/otman-ai/google-sheet-matan) <br>
- [Maton Google Sheets Gateway endpoint](https://gateway.maton.ai/google-sheets/v4/spreadsheets/{SPREADSHEET_ID}/{native-api-path}) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with curl command examples and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses placeholders for spreadsheet IDs, sheet names, ranges, values, sheet IDs, formulas, and Maton API authentication.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
