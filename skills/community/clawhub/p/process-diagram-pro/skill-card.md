## Description:

Process Diagram Pro helps agents generate chemical process PFD, P&ID, system architecture, and data-flow diagrams with temperature coloring and Chinese text support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xx235300](https://clawhub.ai/user/xx235300)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, process engineers, and technical teams use this skill to create presentation-oriented chemical process diagrams, piping and instrumentation diagrams, system architecture diagrams, and data-flow visuals from natural-language requests or Python generator calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser automation and global agent-browser installation guidance extend beyond the diagram generation purpose and can expose sensitive page content or perform unintended web actions.

Mitigation: Use the skill in an isolated environment, skip the global browser installation unless it is specifically needed, and avoid browser commands on sensitive pages or accounts.

Risk: Python dependencies are specified with lower bounds rather than exact pinned versions.

Mitigation: Pin and review matplotlib, Pillow, numpy, and any browser tooling before installation in production or shared environments.

Risk: Generated diagrams are presentation-oriented and may not satisfy engineering, safety, or CAD validation requirements.

Mitigation: Have qualified process or controls engineers review generated diagrams before operational, safety, procurement, or regulatory use.

## Reference(s):

- [Process Diagram Pro on ClawHub](https://clawhub.ai/xx235300/skills/process-diagram-pro)
- [User Guide](https://my.feishu.cn/wiki/XPOVwSB8CivVPkkdFBgcZaCunIf)
- [Matplotlib](https://matplotlib.org/)
- [Pillow](https://pillow.readthedocs.io/)
- [P&ID Reference](https://en.wikipedia.org/wiki/Piping_and_instrumentation_diagram)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with Python snippets and generated diagram image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated diagrams are typically saved as PNG files through the Python generators.]

## Skill Version(s):

2.0.0 (source: ClawHub release metadata; artifact package __version__ reports 3.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
