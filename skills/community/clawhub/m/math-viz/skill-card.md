## Description:

Math Viz turns abstract math problems into interactive HTML visualizations for 2D geometry, 3D geometry, function graphs, moving-point loci, and live numeric exploration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abill6688](https://clawhub.ai/user/abill6688)

### License/Terms of Use:

MIT-0

## Use Case:

Teachers, students, and education-focused agents use this skill to generate Chinese-language interactive math visualizations that support exploration through dragging, sliders, animation, and real-time values.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local verification script can mishandle untrusted filenames or temporary files, which could run unintended commands or alter files.

Mitigation: Run the verifier only on trusted generated HTML paths, avoid filenames containing quotes or shell metacharacters, and prefer a fixed verifier that passes paths as arguments and uses private temporary files.

## Reference(s):

- [Math Viz on ClawHub](https://clawhub.ai/abill6688/skills/math-viz)
- [JSXGraph Patterns](artifact/references/jsxgraph-patterns.md)
- [Three.js Patterns](artifact/references/threejs-patterns.md)
- [Output Verification Script](artifact/scripts/verify_output.sh)

## Skill Output:

**Output Type(s):** [Code, Files, Shell commands, Guidance]

**Output Format:** [HTML files with embedded JavaScript and CSS, plus concise validation guidance and shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated pages are intended to be verified with the bundled output checker before delivery.]

## Skill Version(s):

1.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
