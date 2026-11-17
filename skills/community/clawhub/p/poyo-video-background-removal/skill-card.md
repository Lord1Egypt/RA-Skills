## Description:

Helps agents prepare and submit PoYo video background-removal jobs for hosted videos, including payloads, curl commands, status polling, callbacks, and server-side integration guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolhackboy](https://clawhub.ai/user/coolhackboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to integrate PoYo's hosted video background removal API into server-side workflows, prepare request payloads or curl commands, and understand polling or webhook handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PoYo API keys and media URLs may be exposed if copied into browser code, logs, screenshots, public repositories, or chat output.

Mitigation: Keep POYO_API_KEY server-side, use a backend secret manager or environment variable, and avoid logging API keys, private video URLs, callback URLs, generated outputs, task ids, or authorization headers.

Risk: Submitting unauthorized source video URLs or callback URLs can disclose media or endpoint details to PoYo.

Mitigation: Review the JSON payload before submission and use only video URLs and callback URLs the user is authorized to share with PoYo.

Risk: Live submission sends data to an external hosted API.

Mitigation: Make live API calls only after explicit user confirmation and from a trusted server-side shell with POYO_API_KEY configured.

## Reference(s):

- [PoYo Video Background Removal API Reference](references/api.md)
- [PoYo Video Background Removal model page](https://poyo.ai/models/video-background-removal)
- [Poyo Video Background Removal on ClawHub](https://clawhub.ai/coolhackboy/skills/poyo-video-background-removal)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON payloads and inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include PoYo model id, source video URL handling notes, output container or codec choices, audio preservation settings, background settings, task ids, and polling or webhook next steps.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
