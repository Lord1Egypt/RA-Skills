## Description: <br>
Use when discovering and screening China-mainland AI recruitment candidates from accepted conference or journal papers, matching authors to multiple job descriptions, investigating public professional evidence, preparing individually approved outreach, or classifying recruitment email replies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[debtvc2022](https://clawhub.ai/user/debtvc2022) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Recruiting teams and HR operators use this skill to discover AI research candidates, screen public professional evidence against configured jobs, prepare approval-gated outreach drafts, and classify recruitment replies. It is designed for human-in-the-loop workflows where final candidate, contact, and send decisions remain with an operator. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow uses mainland-China affiliation as a candidate eligibility signal, which may require legal and policy review. <br>
Mitigation: Install only after the organization approves this exact recruiting scope and confirms a lawful basis for the geography-based screening criteria. <br>
Risk: Publication metadata, job descriptions, professional evidence, and complete recruitment email threads may be sent to DeepSeek. <br>
Mitigation: Confirm DeepSeek is an approved processor for this data before use, configure credentials only in the runtime environment, and limit operation to approved jobs and mailboxes. <br>
Risk: Recruiting recommendations or outreach could affect candidates if used without human oversight. <br>
Mitigation: Use the built-in approval gates for candidate approval, outreach preparation, sends, replies, stop-processing, and deletion; do not treat model output as a final hiring or contact decision. <br>
Risk: Candidate evidence and mail content can contain sensitive personal data. <br>
Mitigation: Use the configured retention review workflow, keep SQLite and generated runtime data out of the skill package, and require exact approval before deleting or suppressing records. <br>


## Reference(s): <br>
- [Data Sources](artifact/references/data-sources.md) <br>
- [Screening Policy](artifact/references/screening-policy.md) <br>
- [Outreach Guidelines](artifact/references/outreach-guidelines.md) <br>
- [Reply Classification](artifact/references/reply-classification.md) <br>
- [ClawHub skill page](https://clawhub.ai/debtvc2022/hr-candidate-discovery-screening) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown, JSON] <br>
**Output Format:** [Markdown guidance with shell commands, configuration edits, and JSON/script output summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires runtime job, mailbox, and DeepSeek credential configuration; creates approval-gated candidate and outreach records during operation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
