## Description:

Creates self-contained HTML artwork using SVG, Canvas, CSS, and inline JavaScript to render paintings, style studies, and code-based illustrations from a reference image or text description.

This skill is ready for commercial/non-commercial use.

## Publisher:

[erich1566](https://clawhub.ai/user/erich1566)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creative agents use this skill to plan, generate, and visually check single-file HTML artwork that can be opened offline without image-generation APIs. It is suited to code-art tasks such as recreating paintings, producing SVG or Canvas illustrations, and building comparison previews for refinement.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The comparison workbench accepts pasted artwork HTML, and active HTML can execute in the browser.

Mitigation: Only load artwork HTML from trusted sources and review the generated code before opening it in the workbench.

Risk: Optional preview and analysis workflows may require local Python packages such as Pillow or NumPy.

Mitigation: Install optional dependencies in a virtual environment before running the local helper scripts.

## Reference(s):

- [Analysis workflow](references/analysis-workflow.md)
- [Canvas techniques](references/canvas-techniques.md)
- [Python preview workflow](references/python-preview.md)
- [Style playbooks](references/style-playbooks.md)
- [SVG techniques](references/svg-techniques.md)
- [Artwork comparison workbench](assets/artwork-studio.html)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline HTML, SVG, Canvas, CSS, JavaScript, Python, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Primary deliverable is typically a self-contained .html file; optional local scripts can produce reference-image analysis reports or PNG previews.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
