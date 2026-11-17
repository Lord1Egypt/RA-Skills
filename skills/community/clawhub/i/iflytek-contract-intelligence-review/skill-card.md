## Description:

Reviews contracts by coordinating document extraction, clause analysis, risk detection, compliance checks, bilingual consistency checks, and Markdown or JSON report generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iflytek.skills](https://clawhub.ai/user/iflytek.skills)

### License/Terms of Use:

MIT-0

## Use Case:

Legal, procurement, and compliance teams use this skill to review scanned, image, text, Word, and bilingual contracts for clause structure, common risk categories, consistency issues, and human review needs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive contracts may be processed by OCR, translation, or LLM providers configured through environment variables.

Mitigation: Use only approved providers and credentials for confidential contracts, and confirm data handling terms before sending contract content to external services.

Risk: Generated Markdown reports may contain sensitive contract text and could be unsafe in viewers that permit raw HTML or remote resources.

Mitigation: Review generated reports before sharing and open them in Markdown viewers that disable raw HTML and remote image loading.

Risk: The packaged OCR, image, translation, and LLM clients are abstract interfaces that require injected implementations.

Mitigation: Configure and test the required provider backends before relying on end-to-end contract review results.

Risk: Contract risk findings are review aids and may not reflect enforceable legal advice for a specific jurisdiction.

Mitigation: Route high-risk items, low-confidence extraction results, and jurisdiction-specific questions to qualified human reviewers.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/iflytek.skills/skills/iflytek-contract-intelligence-review)
- [Publisher Profile](https://clawhub.ai/user/iflytek.skills)
- [Skill Definition](artifact/SKILL.md)
- [README](artifact/README.md)
- [Review Output Template](artifact/templates/review_output.json)
- [Sample Review Report](artifact/examples/sample_review_report.md)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Text, Guidance, Shell commands, Configuration]

**Output Format:** [Markdown and JSON contract review reports, plus command-line status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include extracted document metadata, extraction quality, clauses, risks, compliance issues, bilingual issues, translation summary, uncertain items, human review flags, and a final summary.]

## Skill Version(s):

1.0.1 (source: release metadata; artifact _meta.json lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
