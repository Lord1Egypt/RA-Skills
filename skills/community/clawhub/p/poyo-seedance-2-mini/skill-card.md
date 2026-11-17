## Description:

Helps agents prepare and optionally submit PoYo Seedance 2.0 Mini video-generation requests for text-to-video, image-to-video, first/last-frame, reference-media, polling, and webhook workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolhackboy](https://clawhub.ai/user/coolhackboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content automation teams use this skill to prepare PoYo Seedance 2.0 Mini text-to-video, image-to-video, and reference-to-video payloads, submit trusted prepared requests when explicitly requested, and plan polling or webhook follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, media URLs, callback URLs, and generation parameters may be sent to PoYo during video generation.

Mitigation: Submit only data the user is comfortable sharing with PoYo, and avoid confidential prompts, private media URLs, private reference files, or private callback URLs unless the user has accepted that exposure.

Risk: The helper script uploads whichever local JSON payload path it is given.

Mitigation: Use the script only with a trusted, prepared JSON payload file and avoid files influenced by untrusted instructions.

Risk: PoYo API keys can be exposed if placed in browser code, logs, screenshots, repositories, or chat output.

Mitigation: Keep POYO_API_KEY in a server-side environment variable or secret manager and never echo or embed the key in generated examples.

## Reference(s):

- [PoYo Seedance 2.0 Mini model page](https://poyo.ai/models/seedance-2-mini)
- [PoYo Seedance 2.0 Mini API documentation](https://docs.poyo.ai/api-manual/video-series/seedance-2-mini)
- [Local PoYo Seedance 2.0 Mini API reference](references/api.md)
- [PoYo API key page](https://poyo.ai/dashboard/api-key)
- [ClawHub skill page](https://clawhub.ai/coolhackboy/skills/poyo-seedance-2-mini)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON payloads and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include PoYo request parameters, trusted payload examples, task IDs from submitted jobs, and polling or webhook next steps.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
