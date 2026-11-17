## Description:

Extracts candidate key takeaways from provided text by selecting sentences that contain conclusion, result, significance, or similar evidence indicators.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and developers can use this skill to extract concise candidate takeaways from documents, meeting notes, articles, reports, or other text. It is best suited for bounded evidence-insight workflows where outputs are reviewed against the source text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documentation describes broader summarization, action-item, export, and batch-processing behavior than the simple local extractor demonstrates.

Mitigation: Use it as a lightweight key-sentence helper and review outputs against the original source before relying on them.

Risk: Some audited stress inputs reached only partial status because of scope-control or fallback-boundary gaps.

Mitigation: Confirm input scope, required parameters, and fallback behavior before running the skill on larger or ambiguous tasks.

## Reference(s):

- [Key Takeaways Reference Guidelines](artifact/references/guidelines.md)
- [ClawHub Skill Page](https://clawhub.ai/aipoch-ai/skills/key-takeaways)

## Skill Output:

**Output Type(s):** [text, markdown, json, guidance]

**Output Format:** [Markdown or JSON-style summaries containing extracted takeaways and source-review notes when relevant]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local text processing; outputs should be checked against the source text before use.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
