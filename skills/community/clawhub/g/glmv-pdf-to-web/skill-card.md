## Description:

Convert a PDF (research paper, technical report, or project document) into a beautiful single-page academic/project website with a structured outline JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zai-org](https://clawhub.ai/user/zai-org)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and researchers use this skill to turn a local or trusted remote research paper, technical report, or project document PDF into a single-page academic project website with a structured outline and local image crops.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote PDF URLs may be downloaded before conversion, which can expose the workspace to untrusted or unexpected input.

Mitigation: Prefer local PDFs or trusted URLs only, and run the skill in a restricted workspace.

Risk: The security review calls out under-scoped crop output handling and temporary-file handling for untrusted PDFs or shared machines.

Mitigation: Patch crop filename sanitization and temporary-file handling before using the skill with untrusted PDFs or in shared environments.

Risk: The skill depends on PDF and image-processing packages for local file conversion.

Mitigation: Install dependencies in a virtual environment with pinned versions before use.

## Reference(s):

- [GLM-V PDF-to-Web homepage](https://github.com/zai-org/GLM-V/tree/main/skills/glmv-pdf-to-web)

## Skill Output:

**Output Type(s):** [Code, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON outline files, PNG crops, and a single-page HTML website.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates web/<pdf_stem>_<timestamp>/ containing outline.json, crops/, and index.html; HTML references crop assets by relative path.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
