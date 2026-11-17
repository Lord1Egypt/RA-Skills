## Description:

Downloads arXiv PDFs or accepts local paper files, preprocesses and cleans extracted text, then guides summary, detailed summary, contribution extraction, and consistency review in the requested language.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crw0149](https://clawhub.ai/user/crw0149)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and researchers use this skill to summarize arXiv PDFs or local paper files after deterministic extraction and cleaning. It helps keep summaries, detailed notes, contribution extraction, and quality checks grounded in the extracted paper text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill downloads arXiv PDFs, reads user-provided files, and leaves PDFs, extracted text, and manifests in the selected output directory.

Mitigation: Use a controlled output directory, avoid sensitive private documents unless sandboxing or resource limits are in place, and review generated files before sharing them.

Risk: PDF, DOCX, or unsupported file extraction can fail or be partial, which can make summaries incomplete.

Mitigation: Check manifest status, errors, notes, and missing-or-uncertain sections before relying on the generated summary.

Risk: Generated summaries may become misleading if they include claims not supported by the extracted paper text.

Mitigation: Keep generation stages grounded in the cleaned text and use the final quality judgment stage to list consistency errors for each generated section.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/crw0149/skills/paper-summary-scripted)
- [Prompt mapping](references/prompts.md)
- [Output template](references/output-template.md)
- [Script usage](references/script-usage.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance, Files]

**Output Format:** [Markdown with manifest-aware status sections, paper summaries, contribution extraction, and quality scores]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local PDFs, extracted text files, combined extracted text, and manifest.json in the chosen output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
