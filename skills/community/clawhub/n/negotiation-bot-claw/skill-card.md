## Description: <br>
A supplier negotiation agent that helps procurement teams send inquiry emails, parse supplier replies, conduct multi-round price negotiations, and summarize final quotes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tujinsama](https://clawhub.ai/user/tujinsama) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Procurement employees and operations teams use this skill to manage supplier outreach, compare quotes, and prepare negotiation emails for price and terms optimization. It is intended for mailbox-backed supplier negotiations where humans can review recipient lists, messages, and final purchasing decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read mailbox contents and parse supplier communications. <br>
Mitigation: Install it only for a dedicated procurement mailbox, restrict parsing to supplier folders or allowlisted senders, and protect or delete generated CSV reports that may contain confidential supplier information. <br>
Risk: The skill can send negotiation emails broadly through SMTP. <br>
Mitigation: Use scoped app passwords where possible, review recipient lists before sending, and require human review of drafted negotiation emails before delivery. <br>
Risk: Automated negotiation pressure may affect supplier relationships or communicate inaccurate leverage. <br>
Mitigation: Limit automated follow-up rounds, verify claims about competing quotes, and route complex purchases, legal terms, or high-value negotiations to human reviewers. <br>


## Reference(s): <br>
- [Negotiation scripts](references/negotiation-scripts.md) <br>
- [Price benchmarks](references/price-benchmarks.md) <br>
- [Supplier profiles](references/supplier-profiles.md) <br>
- [Inquiry email template](references/email-templates/inquiry.txt) <br>
- [Negotiation pressure email template](references/email-templates/negotiate-pressure.txt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash command examples, email templates, and CSV report outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate supplier outreach messages, parsed quote CSV files, and final quote comparison summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
