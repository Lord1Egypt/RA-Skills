## Description:

Generate technical engineering mechanics sketches, including beams, supports, forces, moments, dimensions, and coordinate systems, as PDF, PNG, or SVG using the MechanicsSketches Python library.

This skill is ready for commercial/non-commercial use.

## Publisher:

[matthiashbusch](https://clawhub.ai/user/matthiashbusch)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineering practitioners use this skill to create free-body diagrams, structural sketches, and mechanical engineering figures from Python or JSON-based workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing MechanicsSketches directly from a remote repository can introduce supply-chain risk if the dependency changes unexpectedly.

Mitigation: Install in an isolated virtual environment without administrator privileges, and prefer a pinned commit or reviewed release.

Risk: The helper's import-path behavior can load unintended local code in shared or world-writable directory layouts.

Mitigation: Run the helper from controlled project directories and avoid shared or world-writable paths until the import-path behavior is fixed.

## Reference(s):

- [MechanicsSketches API Reference](references/api_reference.md)
- [MechanicsSketches Project Homepage](https://github.com/MatthiasHBusch/MechanicsSketches)

## Skill Output:

**Output Type(s):** [Text, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown with Python, JSON, and bash snippets; rendered PDF, PNG, SVG, or JPG files when the helper script is run.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The render function requires an output filename and does not display sketches interactively.]

## Skill Version(s):

1.0.0 (source: frontmatter, changelog, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
