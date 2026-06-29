## Description: <br>
Huo15 Furniture Mfg helps agents answer and act on furniture manufacturing operations for the HeySleep/和栖家居 system, including order tracking, production status, inventory, quality checks, purchasing, customer records, daily overviews, quotations, reminders, and document generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaobod1](https://clawhub.ai/user/zhaobod1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Furniture manufacturing employees and operations teams use this skill to query ERP status, summarize production and fulfillment risk, prepare customer and quotation workflows, and run confirmation-gated updates from a chat agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive ERP credentials. <br>
Mitigation: Use a revocable, low-privilege API key scoped to the intended test system. <br>
Risk: Write and delete capabilities may be broader than the documentation claims. <br>
Mitigation: Review every write/delete preview before approving execution and avoid production credentials unless environment allowlists are enforced. <br>
Risk: Ownership-sensitive actions such as deletes can affect ERP records. <br>
Mitigation: Verify tool ownership and record targets before approving destructive actions. <br>


## Reference(s): <br>
- [Complete Command Reference](references/commands.md) <br>
- [HeySleep Manufacturing API Notes](references/heysleep-mfg-api.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown summaries with inline shell commands and file attachments for generated PDFs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses confirmation-gated write previews and may require scoped ERP credentials.] <br>

## Skill Version(s): <br>
1.4.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
