## Description:

Helps agents prepare and submit Kling 1.6 video generation requests through PoYo, including text-to-video, image-to-video, element reference workflows, polling guidance, and webhook guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolhackboy](https://clawhub.ai/user/coolhackboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to build PoYo Kling 1.6 video-generation payloads, submit trusted requests with a server-side API key, and plan polling or webhook follow-up for asynchronous video jobs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, image URLs, and callback URLs are submitted to PoYo as part of video-generation requests.

Mitigation: Submit only data the user trusts PoYo to process, and avoid confidential prompts, private source images, private reference images, or private callback URLs unless that trust decision is explicit.

Risk: The helper script reads POYO_API_KEY from the environment and sends it to the PoYo API.

Mitigation: Keep POYO_API_KEY server-side, avoid logging or exposing it in browser code, shared shells, screenshots, or chat output, and rotate the key if exposure is suspected.

Risk: Using the helper on shared machines can expose payload details or secrets through local process inspection or monitoring tools.

Mitigation: Run submissions only from trusted shell environments and prefer backend secret management for production workflows.

## Reference(s):

- [PoYo Kling 1.6 Model Page](https://poyo.ai/models/kling-1-6)
- [PoYo Kling 1.6 API Documentation](https://docs.poyo.ai/api-manual/video-series/kling-1-6)
- [PoYo API Key Page](https://poyo.ai/dashboard/api-key)
- [Local API Reference](references/api.md)
- [ClawHub Skill Page](https://clawhub.ai/coolhackboy/skills/poyo-kling-1-6)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance]

**Output Format:** [Markdown with JSON payload examples and bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include model selection, request parameters, a final payload, returned task_id, and polling or webhook next steps.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
