## Description: <br>
Review and manage German tax reports including VAT (Umsatzsteuer), income tax prepayments, and Finanzamt submissions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stanlee000](https://clawhub.ai/user/stanlee000) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to review German tax reports, inspect VAT deadlines and tax settings, preview Finanzamt submissions, and submit tax reports only after explicit confirmation. <br>

### Deployment Geography for Use: <br>
Germany <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide irreversible Finanzamt submissions through the Norman Finance integration. <br>
Mitigation: Show a Finanzamt preview first, require explicit user confirmation, and confirm the tax period and figures before filing. <br>
Risk: The skill depends on the Norman Finance MCP connection and the account configured for it. <br>
Mitigation: Install and use the skill only when the user trusts that MCP connection and the linked Norman Finance account. <br>
Risk: Incorrect tax report periods, figures, or tax settings could lead to filing errors. <br>
Mitigation: Review report details, VAT registration, filing frequency, deadlines, and tax numbers before submission. <br>


## Reference(s): <br>
- [Norman Finance](https://norman.finance) <br>
- [ClawHub skill page](https://clawhub.ai/stanlee000/norman-tax-report) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API Calls, guidance] <br>
**Output Format:** [Markdown or text responses with tax report details, deadlines, previews, and confirmation prompts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the norman-finance MCP integration; Finanzamt submission requires explicit user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
