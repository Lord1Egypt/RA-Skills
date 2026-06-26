## Description: <br>
Professional invoice generation for freelancers and small businesses, with local client management, payment tracking, tax and discount calculations, recurring templates, and revenue reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TheShadowRose](https://clawhub.ai/user/TheShadowRose) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Freelancers, consultants, indie creators, small agencies, and service providers use this skill to create invoices, manage client records, track payment status, and produce basic revenue and aging reports from local files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Client names, emails, addresses, invoice amounts, and payment status are stored in local plaintext files. <br>
Mitigation: Keep data/ and output/ private, exclude real records from public repositories, restrict local file access, and back up sensitive business records securely. <br>
Risk: The included test script creates demo records and changes invoice status. <br>
Mitigation: Run test_basic.sh only in a clean copy or disposable workspace, not against production invoice data. <br>


## Reference(s): <br>
- [Invoice Forge README](artifact/README.md) <br>
- [Invoice Forge Limitations](artifact/LIMITATIONS.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/TheShadowRose/invoice-forge) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Configuration, Markdown, Text] <br>
**Output Format:** [HTML, Markdown, and plain text invoices; text reports; JSONL client and invoice records; shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores generated invoices under output/ and local client and invoice records under data/.] <br>

## Skill Version(s): <br>
1.0.1 (source: evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
