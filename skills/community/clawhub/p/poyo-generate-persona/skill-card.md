## Description:

Create a reusable music persona on PoYo from an eligible completed music track and guide agents through payload preparation, async submission, result polling, and persona_id reuse.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolhackboy](https://clawhub.ai/user/coolhackboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to create PoYo music personas from completed eligible tracks, prepare the required task and audio identifiers, submit or explain the Generate Persona request, and retrieve the resulting persona_id for follow-up music generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys, private task IDs, audio IDs, callback URLs, or returned persona IDs could be exposed in logs, screenshots, chat output, or client-side code.

Mitigation: Keep POYO_API_KEY server-side, review payloads before submission, and avoid logging or displaying sensitive identifiers and callback details.

Risk: A user could submit source audio or style descriptions they do not have rights to process or reuse.

Mitigation: Confirm the user has permission to process the source audio and create a reusable persona before submitting the request.

Risk: Repeated persona creation for the same audio track may return a conflict instead of creating a new persona.

Mitigation: Do not retry conflict responses blindly; retrieve or reuse the existing persona information when available.

## Reference(s):

- [PoYo Generate Persona model page](https://poyo.ai/models/generate-persona)
- [PoYo Generate Persona API docs](https://docs.poyo.ai/api-manual/music-series/generate-persona)
- [PoYo music detail API docs](https://docs.poyo.ai/api-manual/music-series/query-music-detail)
- [PoYo Generate Persona API reference](references/api.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional JSON payloads and curl commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include prerequisite checks, request payload summaries, returned task ids, polling or webhook next steps, and persona_id handling guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
