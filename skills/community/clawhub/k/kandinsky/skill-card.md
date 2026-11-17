## Description:

Kandinsky helps agents generate and edit images, create or animate video, upscale images, and create talking avatars through the Kandinsky API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nikolay-gerasimenko](https://clawhub.ai/user/nikolay-gerasimenko)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content-creation agents use this skill to turn user requests for images, video, animation, upscaling, and talking avatars into Kandinsky API calls, then poll tasks and save the generated media.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The default public plain-HTTP API endpoint can expose API keys and uploaded media.

Mitigation: Configure a trusted HTTPS, private, or loopback endpoint before using real API keys, photos, or voice recordings.

Risk: Uploaded images and audio are sent to the configured remote Kandinsky service.

Mitigation: Use scoped, revocable API keys and avoid sending sensitive media unless the endpoint and operator are trusted.

## Reference(s):

- [Kandinsky API documentation](http://87.242.117.37:5051/docs)
- [Kandinsky API cheatsheet](references/api-cheatsheet.md)
- [Kandinsky prompting guide](references/prompting.md)
- [ClawHub skill page](https://clawhub.ai/nikolay-gerasimenko/skills/kandinsky)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with Python and shell command snippets; generated media is saved as image, video, or binary files by the API client.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires KANDINSKY_API_KEY and optionally KANDINSKY_API_BASE; outputs depend on the selected Kandinsky task type.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
