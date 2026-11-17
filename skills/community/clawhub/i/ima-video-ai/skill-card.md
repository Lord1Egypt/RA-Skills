## Description:

Helps agents generate AI videos from text prompts, images, first/last frames, or reference images using IMA Studio video models such as Wan, Kling, Veo, Sora, Pixverse, Hailuo, SeeDance, and Vidu.

This skill is ready for commercial/non-commercial use.

## Publisher:

[allenfancy-gan](https://clawhub.ai/user/allenfancy-gan)

### License/Terms of Use:

MIT-0

## Use Case:

External users, creators, marketers, and developers use this skill to route video-generation requests, validate parameters, and create text-to-video, image-to-video, first-last-frame, or reference-image outputs through IMA APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys or sensitive request details may be exposed through unsafe endpoint configuration, troubleshooting output, or local failure logs.

Mitigation: Use a scoped or test IMA key, keep IMA_BASE_URL, IMA_IM_BASE_URL, and --base-url pointed only at trusted IMA HTTPS endpoints, avoid commands that print the full key, and inspect or delete ~/.openclaw/logs/ima_skills/ after failures.

Risk: Prompts, task parameters, and uploaded media are processed by third-party IMA services during video generation.

Mitigation: Review media and prompt sensitivity before use, provide only direct public HTTPS media URLs when using remote references, and validate the workflow with low-cost test runs before broader use.

## Reference(s):

- [IMA homepage](https://www.imaclaw.ai)
- [ClawHub skill page](https://clawhub.ai/allenfancy-gan/skills/ima-video-ai)
- [Reference map](artifact/references/README.md)
- [Security and network](artifact/references/shared/security-and-network.md)
- [Model selection policy](artifact/references/shared/model-selection-policy.md)
- [Product list and create parameters](artifact/references/models/product-list-and-create-params.md)
- [Video capability](artifact/capabilities/video/CAPABILITY.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance, Remote video URLs]

**Output Format:** [Markdown guidance with CLI commands and optional JSON task results containing remote HTTPS video URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires IMA_API_KEY; video results are returned as remote HTTPS URLs rather than local file attachments.]

## Skill Version(s):

1.0.13 (source: server release metadata; artifact SKILL.md frontmatter reports 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
