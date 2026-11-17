## Description:

Generate professional LaTeX documents from templates, including IEEE and ACM academic papers, CTeX Chinese thesis formats, moderncv resumes, and custom templates with optional PDF compilation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alicepub](https://clawhub.ai/user/alicepub)

### License/Terms of Use:


## Use Case:

Developers, researchers, students, and technical writers use this skill to turn structured content into publication-ready LaTeX source and PDFs for academic papers, Chinese thesis documents, reports, and resumes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill compiles user-controlled document content locally without enough escaping or sandboxing.

Mitigation: Use trusted content unless compilation is isolated, require explicit confirmation before PDF compilation, validate metadata and bibliography fields, and compile in a restricted sandbox without access to secrets, home directories, or unrelated workspace files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alicepub/skills/latex-writer)
- [Publisher profile](https://clawhub.ai/user/alicepub)

## Skill Output:

**Output Type(s):** [Guidance, Code, Files, Shell commands, Configuration instructions]

**Output Format:** [Markdown guidance with LaTeX source, JSON content structures, and generated .tex/.pdf files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3.10+ and a local TeX distribution such as TeX Live or MiKTeX with xelatex; PDF compilation should be confirmed and sandboxed.]

## Skill Version(s):

1.0.0 (source: release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
