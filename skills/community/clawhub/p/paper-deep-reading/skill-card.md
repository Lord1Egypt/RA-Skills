## Description:

Deep-read research papers into source-aware reports, traceable claim evidence, and research-direction seeds.

This skill is ready for commercial/non-commercial use.

## Publisher:

[c-narcissus](https://clawhub.ai/user/c-narcissus)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, developers, and technical reviewers use this skill to analyze computer-science papers or small paper batches from PDFs, LaTeX sources, appendices, code notes, review material, or citation-like identifiers. It produces source-grounded reading reports, traceability artifacts, and testable research-direction seeds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads user-provided papers, source files, appendices, code notes, and review material.

Mitigation: Run it only on documents you are permitted to process, and avoid placing unrelated sensitive files in the working folder.

Risk: The workflow can create multiple report and traceability files in the active workspace.

Mitigation: Run it in a project-specific workspace and review generated artifacts before sharing or committing them.

Risk: Optional dependency installation may pull packages listed in requirements.txt.

Mitigation: Pin, review, or omit unused dependencies if the host automatically installs requirements.txt.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/c-narcissus/skills/paper-deep-reading)
- [Artifact Contract](references/artifact_contract.md)
- [Research-Generative Methodology](references/research-generative-methodology.md)
- [Research-Direction Mining Best Practices](references/research-direction-mining-best-practices.md)
- [SyncTeX Locator Notes](references/synctex_locator_notes.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Markdown report plus structured JSON artifacts and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces report.md, traceability_manifest.json, latex_paragraphs.json, artifact_index.json, research_lens.json, and direction_board.json when the workflow is completed.]

## Skill Version(s):

1.2.0 (source: frontmatter, artifact metadata, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
