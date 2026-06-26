## Description: <br>
Generate professional PDF invoices from simple text commands. Supports multiple currencies, tax calculation, CJK text, and customizable templates. No external service needed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zacjiang](https://clawhub.ai/user/zacjiang) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, freelancers, and business operators use this skill to create itemized PDF invoices from simple commands or structured billing details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Invoice PDFs can contain client, business, payment, and tax details. <br>
Mitigation: Review invoice fields before generation and store generated PDFs according to the user's data-handling requirements. <br>
Risk: The selected output filename can overwrite an existing file. <br>
Mitigation: Confirm the output path before running the generation command. <br>
Risk: The script requires the local reportlab dependency and optional CJK fonts. <br>
Mitigation: Install dependencies deliberately, preferably in a virtual environment, and add CJK fonts only when needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zacjiang/invoice-gen) <br>
- [Publisher profile](https://clawhub.ai/user/zacjiang) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, files, guidance] <br>
**Output Format:** [Markdown guidance and shell commands that generate a PDF invoice file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local PDF invoice files and may include client, business, payment, and tax details.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
