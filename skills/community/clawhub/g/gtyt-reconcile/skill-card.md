## Description:

共同赢（GTYT）供应商账单与到货单的三阶段对账流程，用于按月核对「共同赢X月账单-上海-共同赢.xls」与「到货单明细表」在每店每产品上的「单价」「数量」「金额」是否一致，并输出差异对比 Excel 和标黄差异账单 Excel。

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlesoyoung](https://clawhub.ai/user/charlesoyoung)

### License/Terms of Use:

MIT-0

## Use Case:

Operations, finance, and reconciliation users can use this skill to compare monthly GTYT supplier bills against arrival-order spreadsheets by store and SKU. It produces a full difference report and a copy of the original bill with quantity, price, and amount discrepancies highlighted for manual review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive billing spreadsheets and writes generated reports and intermediate files to predictable temporary paths by default.

Mitigation: Run it in a trusted environment, provide a private output directory, restrict access to generated files, and remove intermediate files after review.

Risk: Generated reconciliation reports may be sent through Feishu delivery and could reach the wrong recipient if the target is not checked.

Mitigation: Confirm the Feishu recipient and attached file paths before sending reports.

Risk: Store-name mappings and spreadsheet input assumptions can affect which rows are marked as differences.

Mitigation: Review unmatched stores, merged-store notes, and highlighted cells before using the output for financial decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/charlesoyoung/skills/gtyt-reconcile)

## Skill Output:

**Output Type(s):** [Files, JSON, Shell commands, Guidance]

**Output Format:** [Excel .xls reports, JSON summary, and concise agent-facing status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes a parsed intermediate JSON file and two reconciliation spreadsheets; generated files may contain sensitive billing data.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
