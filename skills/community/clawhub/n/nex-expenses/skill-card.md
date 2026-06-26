## Description: <br>
Track and categorize business expenses with Belgian tax deduction rules, local OCR receipt scanning, BTW tracking, quarterly summaries, and CSV/JSON exports for accounting workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nexaiguy](https://clawhub.ai/user/nexaiguy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Freelancers, sole traders, small businesses, and their agents use this skill to add, scan, categorize, search, summarize, and export Belgian business expenses while keeping receipt and expense data local. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores sensitive receipts, OCR text, and business expense records locally under ~/.nex-expenses. <br>
Mitigation: Install only on trusted machines and manage local filesystem permissions, backups, and deletion of receipt images according to the user's data-handling needs. <br>
Risk: OCR extraction and automatic Belgian tax categorization can be incorrect or incomplete. <br>
Mitigation: Review extracted vendor, date, amount, BTW rate, and tax category values before using summaries or exports for accounting or tax filing. <br>
Risk: Expense add, edit, delete, and export actions can change local records or create files used in accounting workflows. <br>
Mitigation: Confirm the intended action and target expense IDs before running mutating commands, especially delete or bulk export operations. <br>
Risk: Evidence lists crypto and purchase-related capabilities even though the security guidance says the skill does not need that authority. <br>
Mitigation: Do not grant crypto or purchase authority when installing or running this skill. <br>


## Reference(s): <br>
- [Nex AI homepage](https://nex-ai.be) <br>
- [Tesseract OCR Windows installer reference](https://github.com/UB-Mannheim/tesseract/wiki) <br>
- [ClawHub skill page](https://clawhub.ai/nexaiguy/nex-expenses) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, code, files] <br>
**Output Format:** [Plain text and Markdown guidance with CLI commands; generated expense exports may be CSV or JSON files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Agent-facing output may include parsed expense details, summaries, file paths, command results, and local configuration guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, release metadata, README changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
