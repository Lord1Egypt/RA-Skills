## Description: <br>
Pocketbook records, queries, completes, corrects, and undoes personal bookkeeping entries through short natural-language conversation with local JSONL and Markdown persistence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SuRu711](https://clawhub.ai/user/SuRu711) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to maintain a personal ledger by capturing expenses, income, refunds, and transfers, then reviewing summaries or correcting recent entries. It is intended for explicit ledger operations, not accounting, tax, investment, invoice, OCR, or reimbursement advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Personal transaction history is stored in local ledger files. <br>
Mitigation: Choose and protect the data directory, and avoid putting secrets or sensitive notes into ledger entries. <br>
Risk: Short transaction messages can be ambiguous or duplicate an existing entry. <br>
Mitigation: Review entries flagged as ambiguous or possible duplicates before relying on summaries or applying corrections. <br>
Risk: Dates default to the skill's configured timezone when the user does not specify one. <br>
Mitigation: Set the correct timezone for the user's ledger before recording time-sensitive entries. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/SuRu711/pocket-book) <br>
- [Publisher Profile](https://clawhub.ai/user/SuRu711) <br>
- [Homepage](https://github.com/SuRu711/pocketbook) <br>
- [Pocketbook Schema](references/schema.md) <br>
- [Trigger Examples](references/intent-examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Concise ledger confirmations, query summaries, structured script payloads, and Markdown ledger views] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local ledger files and concise confirmations; duplicate and ambiguity warnings may be returned for user review.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
