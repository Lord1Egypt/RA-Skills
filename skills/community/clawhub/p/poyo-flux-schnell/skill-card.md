## Description:

Generates prompt-based images with PoYo's FLUX Schnell API and helps agents prepare request payloads, submit approved jobs, and explain polling or webhook follow-up.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolhackboy](https://clawhub.ai/user/coolhackboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to create PoYo FLUX Schnell text-to-image payloads, submit reviewed jobs through the PoYo API, and plan polling or webhook follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: POYO_API_KEY could be exposed if copied into browser code, public files, logs, screenshots, or chat output.

Mitigation: Keep POYO_API_KEY server-side in the environment or a secret manager and send it only in the PoYo Authorization header.

Risk: Live API submission may send prompts, callback URLs, and selected request parameters to PoYo and any configured callback receiver.

Mitigation: Review payload JSON before submission, avoid confidential prompts or private callback URLs unless the user trusts those services, and require explicit approval before any live request.

## Reference(s):

- [PoYo FLUX Schnell API Reference](references/api.md)
- [PoYo FLUX Schnell model page](https://poyo.ai/models/flux-schnell)
- [PoYo FLUX Schnell API docs](https://docs.poyo.ai/api-manual/image-series/flux-schnell)
- [ClawHub skill page](https://clawhub.ai/coolhackboy/skills/poyo-flux-schnell)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, API Calls]

**Output Format:** [Markdown with JSON payloads and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include the flux-schnell model id, text-to-image confirmation, selected size, output count, output format, returned task_id, and polling or webhook next steps.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
