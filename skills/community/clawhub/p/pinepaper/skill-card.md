## Description:

PinePaper helps agents create, animate, query, transform, and export vector-based text, shapes, diagrams, maps, and visual effects on an infinite canvas.

This skill is ready for commercial/non-commercial use.

## Publisher:

[speaktoarpit](https://clawhub.ai/user/speaktoarpit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agents use this skill as a PinePaper API and MCP reference for building animated canvas content, diagrams, visualizations, and exportable graphics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Destructive canvas actions can clear, reset, or delete selected content.

Mitigation: Agents should ask for explicit confirmation before clearing, resetting, or deleting PinePaper canvas content.

Risk: The training-data export tool may expose canvas content without clear scope.

Mitigation: Agents should avoid training-data export unless the user explicitly requests it and understands what will be exported.

Risk: Using PinePaper with sensitive or valuable canvas content increases review requirements.

Mitigation: Review the skill before installation and limit use to appropriate canvas content and workflows.

## Reference(s):

- [PinePaper Studio](https://pinepaper.studio)
- [ClawHub PinePaper Skill Page](https://clawhub.ai/speaktoarpit/skills/pinepaper)
- [PinePaper Studio AI Agent Skills Reference](artifact/skills.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reference material with JavaScript examples, MCP tool names, and export workflow guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs guide agents toward PinePaper canvas operations, API calls, MCP tools, and export formats.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
