## Description:

Convierte un video grabado con una toma hablando a cámara en un clip de pizarra para pantalla dividida, usando el .srt para mapear 8-12 beats, pedir aprobación de costo, generar un clip por beat y entregar un pizarra.mp4 con un LEEME de alineación.

This skill is ready for commercial/non-commercial use.

## Publisher:

[formula100k](https://clawhub.ai/user/formula100k)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, editors, and content teams use this skill to turn a local talking-head video and subtitle file into a timed hand-drawn whiteboard support clip for split-screen editing. It guides the agent through beat mapping, approval before paid generation, clip generation, concatenation, and delivery notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent reads local video and subtitle files supplied by the user.

Mitigation: Install and run only when you are comfortable granting access to those media files and transcripts.

Risk: External media-generation tools may incur cost.

Mitigation: Use the skill's approval checkpoint before paid Higgsfield generation and confirm the estimated cost before continuing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/formula100k/skills/pizarra-explicativa-f100k)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance, files]

**Output Format:** [Markdown guidance with shell commands and generated media-file deliverables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces beat maps, approval prompts, a pizarra.mp4 clip, separate beat clips, and a LEEME.md with alignment timestamps.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
