## Description:

Helps agents generate PoYo music cover versions by preparing request payloads, curl commands, and retrieval guidance for the generate-music-cover API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolhackboy](https://clawhub.ai/user/coolhackboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to prepare and optionally submit PoYo generate-music-cover workflows from completed music task IDs, including callback setup and follow-up status retrieval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends selected request payload data to PoYo's external API.

Mitigation: Review the JSON payload before submission and only submit data intended for PoYo processing.

Risk: POYO_API_KEY is required for live submissions.

Mitigation: Keep POYO_API_KEY server-side in an environment variable or secret manager and do not expose it in browser code, logs, screenshots, repositories, or chat output.

Risk: Arbitrary local files passed to the submit script are transmitted as request payloads.

Mitigation: Use trusted payload files only and avoid passing arbitrary local files to the submit script.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/coolhackboy/skills/poyo-generate-music-cover)
- [PoYo Generate Music Cover model page](https://poyo.ai/models/generate-music-cover)
- [PoYo Generate Music Cover API docs](https://docs.poyo.ai/api-manual/music-series/generate-music-cover)
- [PoYo Generate Music Cover OpenAPI JSON](https://docs.poyo.ai/api-manual/music-series/generate-music-cover.json)
- [PoYo API key page](https://poyo.ai/dashboard/api-key)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON payloads and bash/curl code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a returned task_id after an explicit PoYo submission.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
