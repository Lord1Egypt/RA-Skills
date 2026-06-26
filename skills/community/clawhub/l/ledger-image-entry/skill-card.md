## Description: <br>
Ledger Image Entry extracts merchant, date, amount, and line-item details from receipt, order, or invoice images and converts them into structured ledger records. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shing19](https://clawhub.ai/user/shing19) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to turn receipt, order, or invoice images into ledger-ready expense rows with merchant, date, category, amount, and notes. It is suited for personal or operational expense-entry workflows where the user reviews the extracted table before recording it. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Receipt, order, or invoice images may be blurry, incomplete, or ambiguous, which can lead to incorrect merchant, date, category, item, or amount extraction. <br>
Mitigation: Ask the user to confirm unclear fields and review the generated confirmation table before treating the rows as final ledger entries. <br>
Risk: When the image does not include a clear date, the skill defaults to the current date, which may not match the transaction date. <br>
Mitigation: Expose the defaulted date in the confirmation table and let the user correct it before recording the entry. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shing19/ledger-image-entry) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown] <br>
**Output Format:** [Markdown confirmation table with a total amount summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Amounts are formatted to two decimal places; unclear image content should be confirmed with the user.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
