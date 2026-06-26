## Description: <br>
Processes and organizes invoice PDFs by fixing extensions, removing duplicates and invalid files, checking for required keywords, and calculating total amounts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jie](https://clawhub.ai/user/jie) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and operators use this skill to organize a local directory of invoice PDFs, separate keyword-matching invoices from unknown invoices, and summarize the invoice total. It is best suited for controlled invoice folders where the user can provide the required invoice keyword. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can permanently delete duplicate and invalid files while processing the selected invoice directory. <br>
Mitigation: Run it only on a copy or backup of a specific invoice folder, avoid broad paths such as a home directory or project root, and review results before relying on them. <br>
Risk: The skill moves many PDF files without a dry run or explicit confirmation. <br>
Mitigation: Use a tightly scoped directory and confirm the requested keyword and target path before execution. <br>
Risk: The dependency declaration does not pin PyMuPDF to a fixed release. <br>
Mitigation: Prefer an environment with a reviewed PyMuPDF version at or above the fixed release recommended by security review. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jie/invoice-processing) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/jie) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, Files] <br>
**Output Format:** [Terminal command and plain-text processing summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Moves matching PDFs into an invoices folder, moves unmatched PDFs into invoices/unknown, deletes duplicates and files matching the configured invalid filename pattern, and prints the grand total amount.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
