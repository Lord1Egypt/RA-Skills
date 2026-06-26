## Description: <br>
Parses bank statements from all major Greek banks (Alpha, NBG, Eurobank, Piraeus). File-based CSV/Excel import with transaction reconciliation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[satoshistackalotto](https://clawhub.ai/user/satoshistackalotto) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and accounting operators use this skill to guide OpenClaw through file-based import, reconciliation, VAT analysis, duplicate detection, and accounting exports for Greek bank statements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive bank statement and transaction data. <br>
Mitigation: Use a protected data directory, avoid shared or backed-up folders for raw statements, and restrict access to exported reconciliation and accounting files. <br>
Risk: Optional accounting-system updates and Xero API push can change or transmit accounting records. <br>
Mitigation: Configure XERO_API_KEY only when direct posting is required, and review export or auto-update commands before running them. <br>
Risk: The server security summary flags insufficient scoping and safety guidance around financial workflows. <br>
Mitigation: Review parsed transactions, VAT treatment, duplicate detection, and reconciliation results before relying on them for accounting or compliance decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/satoshistackalotto/greek-banking-integration) <br>
- [Publisher profile](https://clawhub.ai/user/satoshistackalotto) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce file-processing guidance, reconciliation report instructions, and export workflow guidance for CSV, JSON, QuickBooks-compatible files, or Xero-compatible output.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
