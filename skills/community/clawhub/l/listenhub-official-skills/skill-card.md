## Description:

Explain anything by turning ideas, URLs, text, and image prompts into podcasts, explainer videos, voice narration, or generated images through ListenHub scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xfango](https://clawhub.ai/user/0xfango)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to create podcasts, explainer videos, text-to-speech audio, multi-speaker speech, and images from topics, URLs, plain text, scripts, or prompts. The agent selects the appropriate bundled shell script, prepares arguments, submits generation, and reports status or output locations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, source text, URLs, and image-reference URLs are sent to ListenHub, Marswave, or Labnana APIs for processing.

Mitigation: Use only content and URLs that are acceptable to send to those services, and avoid sensitive or confidential inputs.

Risk: Image generation first-run setup can modify shell startup files, store an API key insecurely, and auto-install packages.

Mitigation: Provide LISTENHUB_API_KEY and LISTENHUB_OUTPUT_DIR through the environment, install jq and curl manually, and avoid the first-run setup path.

Risk: Local reference images must be uploaded to public image hosts before image generation can use them.

Mitigation: Do not upload private local images; use only reference image URLs that are acceptable to share externally.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/0xfango/skills/listenhub-official-skills)
- [ListenHub API Key Settings](https://listenhub.ai/settings/api-keys)
- [Labnana OpenAPI Documentation](https://docs.marswave.ai/openapi-labnana.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON response handling, status summaries, and local file paths or product links for generated media.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated media jobs can be asynchronous; podcast, explainer, and text-to-speech status is checked with bundled scripts, while image generation saves files locally.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
