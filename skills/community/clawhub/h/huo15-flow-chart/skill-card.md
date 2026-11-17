## Description:

Generates modern flowcharts, swimlane diagrams, architecture diagrams, C4 diagrams, sequence diagrams, state diagrams, ER diagrams, and Gantt charts from YAML, JSON, Mermaid, PlantUML, or DOT inputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaobod1](https://clawhub.ai/user/zhaobod1)

### License/Terms of Use:

MIT

## Use Case:

Developers, architects, and technical writers use this skill to turn structured diagram specifications or diagram source code into presentation-ready diagrams and editable diagram source files. It is useful for documenting software flows, systems, timelines, and architecture views.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review says the skill can automatically run unpinned external renderers and Docker or Chromium with weak sandboxing.

Mitigation: Use only trusted publisher releases, prefer preinstalled pinned renderer binaries, and avoid the automatic npx and Docker fallbacks.

Risk: Rendering untrusted diagram source or writing outputs to user-supplied paths can affect a sensitive machine or working directory.

Mitigation: Render only trusted diagram inputs and run the skill in a dedicated working directory with controlled output paths.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhaobod1/skills/huo15-flow-chart)
- [Mermaid Live Editor](https://mermaid.live)
- [Flowchart core implementation](scripts/flowchart_core.py)

## Skill Output:

**Output Type(s):** [Files, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with shell commands plus generated SVG, PNG, PDF, Mermaid, PlantUML, DOT, and draw.io files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [PNG output supports adjustable high-DPI scaling; PDF output defaults to a single fitted page.]

## Skill Version(s):

1.4.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
