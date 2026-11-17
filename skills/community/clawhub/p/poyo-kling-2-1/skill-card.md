## Description:

Kling 2.1 image-to-video generation on PoYo via its async API, helping agents prepare Standard or Pro payloads, submit tasks, and plan polling or webhook follow-up.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolhackboy](https://clawhub.ai/user/coolhackboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to build PoYo Kling 2.1 image-to-video requests, choose Standard or Pro model options, submit trusted payloads, and guide follow-up through polling or webhooks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: POYO_API_KEY or request details could be exposed through client-side code, logs, screenshots, repositories, or chat output.

Mitigation: Keep POYO_API_KEY server-side in an environment variable or secret manager, and avoid echoing keys or sensitive request details.

Risk: Private prompts, image URLs, callback URLs, task identifiers, or generated media URLs may be shared with PoYo or webhook receivers during task submission and follow-up.

Mitigation: Review each payload before submission and avoid confidential inputs unless the user accepts the external-service and webhook data-sharing risk.

## Reference(s):

- [PoYo Kling 2.1 API Reference](references/api.md)
- [PoYo Kling 2.1 Model Page](https://poyo.ai/models/kling-2-1)
- [PoYo Kling 2.1 API Docs](https://docs.poyo.ai/api-manual/video-series/kling-2-1)
- [ClawHub Skill Page](https://clawhub.ai/coolhackboy/skills/poyo-kling-2-1)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON payloads and bash or curl examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May submit a prepared JSON payload when POYO_API_KEY is available in a trusted shell and the user explicitly requests a live API call.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
