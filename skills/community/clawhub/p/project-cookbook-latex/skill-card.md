## Description:

Creates source-level 80k+ word project CookBooks as LaTeX, PDF, and EPUB.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samonysh](https://clawhub.ai/user/samonysh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, architects, and advanced technical readers use this skill to turn websites, documentation, repositories, APIs, papers, or local project material into deep project CookBooks with source-level analysis, diagrams, LaTeX source, PDF, and EPUB outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote fetching or image upload can create network side effects.

Mitigation: Keep the workflow offline by default and confirm remote URLs, image upload, and network fetching before use.

Risk: LaTeX shell escape can execute commands if enabled for untrusted content.

Mitigation: Keep shell escape disabled unless the content is trusted, the user consents, and the run is sandboxed.

Risk: Long-form generated documentation can be misdirected if source paths, output paths, or linked skills are unclear.

Mitigation: Confirm exact source paths, remote URLs, output directory, and linked skills before running the workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/samonysh/skills/project-cookbook-latex)
- [Pixabay example cover image source](https://pixabay.com/en/tea-time-poetry-coffee-reading-3240766/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Guidance and generated project artifacts, including LaTeX source, PDF, EPUB, diagram sources and images, references, word-count data, build instructions, and validation reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Offline by default; remote fetching, image upload, dependency installation, and LaTeX shell escape require explicit user approval.]

## Skill Version(s):

1.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
