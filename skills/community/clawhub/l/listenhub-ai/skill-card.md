## Description:

ListenHub turns ideas, text, URLs, and prompts into podcasts, explainer videos, voice narration, multi-speaker speech, and AI images through provided ListenHub scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kkaticld](https://clawhub.ai/user/kkaticld)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to generate audio, video, and image assets from topics, article URLs, YouTube links, plain text, or image prompts. It is intended for agent-assisted media creation through the packaged shell scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated media requests may send sensitive text, private URLs, prompts, or reference images to external cloud services.

Mitigation: Avoid submitting confidential material unless the user has approved sending it to the disclosed services.

Risk: The image workflow is flagged as higher risk because it can make persistent shell changes, attempt elevated package installation, and use a differently branded provider than the main ListenHub description.

Mitigation: Review the image script before use, preinstall dependencies manually, configure LISTENHUB_API_KEY through the agent environment, and treat image generation as higher risk until provider and credential-handling concerns are resolved.

Risk: Long-running media generation can remain pending, fail, or hit rate limits.

Mitigation: Use the packaged status checker with bounded polling and retry only after short waits when timeout or rate-limit responses occur.

## Reference(s):

- [ListenHub skill page](https://clawhub.ai/kkaticld/skills/listenhub-ai)
- [ListenHub podcast library](https://listenhub.ai/app/podcast)
- [ListenHub explainer library](https://listenhub.ai/app/explainer)
- [ListenHub text-to-speech library](https://listenhub.ai/app/text-to-speech)
- [Marswave OpenAPI documentation](https://docs.marswave.ai/openapi-labnana.html)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return ListenHub job identifiers, status JSON, hosted result links, and local image files saved to the configured output directory.]

## Skill Version(s):

0.6.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
