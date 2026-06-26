## Description: <br>
Invoice Agent helps freelancers, agencies, and small businesses create, track, export, and manage invoices, payment reminders, overdue balances, and revenue summaries from local command-line workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[atum246](https://clawhub.ai/user/atum246) <br>

### License/Terms of Use: <br>
Proprietary single-user license via ClawHub <br>


## Use Case: <br>
External users such as freelancers, agencies, and small businesses use this skill to manage local client billing workflows, including invoice creation, status tracking, HTML invoice generation, overdue checks, payment reminder drafts, and revenue summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local invoice data directory can contain client names, emails, addresses, invoice amounts, and payment status. <br>
Mitigation: Keep ~/.invoice-agent protected with appropriate local filesystem permissions and device security controls. <br>
Risk: Generated reminder text, especially final notices, can affect customer relationships or imply legal collection steps. <br>
Mitigation: Treat reminders as drafts and manually review wording, amounts, dates, and escalation level before sending. <br>


## Reference(s): <br>
- [Invoice Agent Reference Guide](artifact/references/guide.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/atum246/invoice-agent) <br>
- [Publisher Profile](https://clawhub.ai/user/atum246) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with shell commands plus local JSON, HTML, and reminder text outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores invoice data locally under ~/.invoice-agent and can export invoice JSON and HTML files.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
