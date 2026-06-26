## Description: <br>
Contract Review + Contract Ops Copilot for solo entrepreneurs that analyzes contracts, flags risks, generates redline suggestions and negotiation emails, tracks deadlines, and maintains a structured contract archive with cross-contract portfolio insights. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LeonFJR](https://clawhub.ai/user/LeonFJR) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Solo entrepreneurs and one-person company CEOs use this skill to perform first-pass commercial contract review, prepare negotiation asks, draft counterparty emails, archive signed contracts, track deadlines, and search portfolio-level contract risks. It is a practical risk-review aid and not a substitute for qualified legal advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Archived contracts and generated analyses may contain confidential terms, signatures, payment details, and personal data. <br>
Mitigation: Install and run the skill only in a private workspace, and keep the contracts directory out of public repositories and shared sync folders. <br>
Risk: Generated metadata, dashboards, and portfolio insights may be incomplete or incorrect if source contracts are ambiguous or extraction confidence is low. <br>
Mitigation: Review generated metadata and reports before relying on them for business decisions, and consult a qualified attorney before making binding legal decisions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/LeonFJR/opc-contract-manager) <br>
- [Red Flags Checklist](references/red-flags-checklist.md) <br>
- [Standard Clauses](references/standard-clauses.md) <br>
- [Solo Entrepreneur Concerns Guide](references/solo-entrepreneur-concerns.md) <br>
- [Termination for Convenience Guide](references/termination-for-convenience.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, JSON metadata, generated contract archive files, and shell commands for local archive scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses ISO 8601 dates, preserves contract currency amounts as stated, and stores archive metadata in structured JSON.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
