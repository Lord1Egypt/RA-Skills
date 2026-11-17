## Description:

Read academic papers from local PDF files, arXiv URLs, or paper titles and generate structured reading notes in Chinese.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fourierer](https://clawhub.ai/user/fourierer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and students use this skill to fetch or load academic PDFs, extract paper text, and produce structured Chinese reading notes for paper review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The PDF downloader can reach non-arXiv network locations despite presenting itself as arXiv-scoped.

Mitigation: Prefer local PDFs or trusted arXiv URLs, and run the skill in an environment without private-network access when reviewing unfamiliar inputs.

Risk: The workflow writes downloaded PDFs, extracted text, and notes to user-specified paths.

Mitigation: Use a constrained workspace, avoid sensitive writable paths, and avoid privileged execution.

Risk: The PDF extraction workflow depends on runtime Python dependencies such as pdfplumber.

Mitigation: Pin dependencies before adopting the skill in a repeatable environment.

## Reference(s):

- [Paper note template](references/note-template.md)
- [mHC example note](references/mHC.md)
- [arXiv API](http://export.arxiv.org/api/query)
- [ClawHub skill page](https://clawhub.ai/fourierer/skills/paper-reading-fourier)

## Skill Output:

**Output Type(s):** [Markdown, Text, Shell commands, Code, Guidance]

**Output Format:** [Markdown notes in Chinese with LaTeX formulas, image links, info blocks, and optional Python code blocks.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save notes or extracted paper text to user-specified output paths.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
