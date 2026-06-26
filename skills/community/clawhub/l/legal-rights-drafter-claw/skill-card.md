## Description: <br>
法律维权草拟虾 helps users identify breach, payment, infringement, and related rights-protection scenarios and draft standardized legal notice letters from natural-language or structured case details. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tujinsama](https://clawhub.ai/user/tujinsama) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, legal operations teams, and business staff use this skill to turn dispute facts into draft notice letters such as demand letters, payment reminders, termination notices, quality objection letters, intellectual-property warnings, and confidentiality-breach notices. Outputs are drafts for legal review before formal use. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: Generated legal letters may misstate facts, omit required evidence, or apply legal provisions incorrectly. <br>
Mitigation: Treat every output as a draft and have legal counsel or an appropriate legal reviewer check it before sending. <br>
Risk: Case descriptions can include sensitive contract, personal, or dispute information. <br>
Mitigation: Provide only the details needed to draft the letter and avoid unnecessary sensitive information. <br>
Risk: The optional document export script runs local file conversion tools on Markdown input. <br>
Mitigation: Run conversion only on trusted Markdown files and with trusted local converter binaries. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/tujinsama/legal-rights-drafter-claw) <br>
- [legal-clauses.md](references/legal-clauses.md) <br>
- [letter-templates.md](references/letter-templates.md) <br>
- [case-references.md](references/case-references.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown legal-letter drafts with optional shell-command guidance for local PDF or Word conversion] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default output is Markdown in the agent response; optional local conversion can produce PDF or DOCX when trusted converter tools are available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
