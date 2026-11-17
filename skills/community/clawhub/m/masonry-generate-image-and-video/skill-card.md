## Description:

AI-powered image and video generation. Generate images, videos, manage jobs, and explore models via the masonry CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[junaid1460](https://clawhub.ai/user/junaid1460)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to generate AI images and videos, inspect available Masonry models, track generation jobs, and download completed media outputs through the Masonry CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Masonry account token and can initiate login flows for access to a Masonry workspace.

Mitigation: Avoid pasting tokens into chat; enter credentials only in a local terminal or secure secret mechanism and use MASONRY_TOKEN from a managed secret store when available.

Risk: The skill depends on the Masonry npm CLI package to generate and download media.

Mitigation: Install only if you trust the Masonry CLI package; prefer a pinned or reviewed CLI version where possible.

Risk: Incorrect job IDs, model keys, or guessed CLI responses can lead to failed or misleading generation workflows.

Mitigation: Use only job IDs, model keys, wait intervals, and status values returned by Masonry CLI JSON output.

## Reference(s):

- [Masonry homepage](https://masonry.so)
- [Masonry pricing](https://masonry.so/pricing)
- [Masonry skills feedback](https://github.com/masonry-so/skills/issues)
- [ClawHub skill page](https://clawhub.ai/junaid1460/skills/masonry-generate-image-and-video)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance, Files]

**Output Format:** [Markdown guidance with bash command examples, JSON CLI responses, and downloaded media file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May emit MEDIA: file path lines after successful downloads; relies on Masonry CLI JSON responses.]

## Skill Version(s):

1.1.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
