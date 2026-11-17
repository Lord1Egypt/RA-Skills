## Description:

Helps agents turn complex LLM and technical material into audience-appropriate explanations using controlled prose, diagrams, standalone HTML, narrated video, or small interactive demos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lizhengbo95](https://clawhub.ai/user/lizhengbo95)

### License/Terms of Use:

MIT

## Use Case:

Writers, educators, developers, and teams use this skill to explain technical topics to a specific audience through layered prose, diagrams, shareable pages, videos, or disposable interactive examples.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Narration text may expose sensitive content to a selected text-to-speech provider.

Mitigation: Exclude secrets, personal, regulated, or proprietary text unless the provider and its handling are acceptable.

Risk: Demo artifacts may retain sensitive inputs at their storage location.

Mitigation: Use non-sensitive example data or confirm the storage location is appropriate before generating demos.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/lizhengbo95/skills/llm-output-explainer)
- [Audience and format decision matrix](references/decision-matrix.md)
- [Controlled-language guidance](references/module-a-ste100.md)
- [Diagram guidance](references/module-b-diagram.md)
- [Standalone HTML guidance](references/module-c-html.md)
- [Narrated video guidance](references/module-d-video.md)
- [Disposable demo guidance](references/module-e-disposable.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Diagrams, HTML, Code, Video, Guidance]

**Output Format:** [Audience-adapted prose, Mermaid diagrams, single-file HTML, demo code, or narrated video, depending on the request]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Video production requires optional Manim, text-to-speech, and ffmpeg tooling.]

## Skill Version(s):

1.0.0 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
