## Description:

A multi-agent pipeline for translating and reconstructing complex, image-heavy, scanned, or formula-heavy PDF documents while preserving layout and source figures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lingqing](https://clawhub.ai/user/lingqing)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to translate complex technical PDFs into reconstructed output PDFs when page layout, diagrams, tables, and mathematical notation need to be retained.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends PDF page images, text, and formulas to external Google GenAI and math.vercel.app services.

Mitigation: Use only with documents approved for those external services, and restrict outbound network access to approved endpoints.

Risk: The skill renders untrusted model output through the PDF rendering path with broad local and network access.

Mitigation: Run in a low-privilege sandbox and patch the renderer to sanitize model output and restrict WeasyPrint resource fetching before production use.

Risk: The server security verdict is suspicious and requires review before deployment.

Mitigation: Complete a manual security and data-flow review before installing or using the skill in a production environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lingqing/skills/pdf-master-translator)
- [math.vercel.app formula rendering service](https://math.vercel.app/)

## Skill Output:

**Output Type(s):** [Files, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown guidance and shell commands; generated PDF output file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a source PDF path, explicit start and end pages, GEMINI_API_KEY, and outbound access to Google GenAI and math.vercel.app.]

## Skill Version(s):

1.0.0 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
