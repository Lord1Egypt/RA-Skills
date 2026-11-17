## Description:

On explicit invocation, creates evidence-backed visual artifacts from article text or local data, with optional run review, spec validation, and consent-gated image or video generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[miaoshou.dev](https://clawhub.ai/user/miaoshou.dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use Miao Vision to turn article text and local data into evidence-backed infographics, reports, data posters, and browser decks. They can also review runs, validate report or deck specifications, and request optional image or video generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation may use an optional unpinned npx route, and downloaded dependencies were not audited.

Mitigation: Review dependency versions before approving installation and use the documented fixed-version install path where appropriate.

Risk: Export setup may move an existing ~/.miao-vision/playwright directory to a timestamped backup.

Mitigation: Back up the directory before running export setup.

Risk: Optional image and video generation sends the confirmed prompt and selected images to external providers and incurs charges.

Mitigation: Proceed only after reviewing and confirming the exact prompt, selected references, and expected charges.

Risk: Installed tools and caches remain after plugin removal.

Mitigation: Remove the global CLI and associated caches separately when they are no longer needed.

## Reference(s):

- [Article infographic workflow](references/article.md)
- [Report workflow](references/report.md)
- [Browser deck workflow](references/deck.md)
- [Review Viewer workflow](references/review-viewer.md)
- [Data-story video workflow](references/media-video.md)
- [Miao Vision plugin release bundle](https://github.com/miaoshou-dev/miao-vision/releases/latest/download/miao-vision-plugin.zip)

## Skill Output:

**Output Type(s):** [HTML reports, PDFs, PNG exports, Data posters, Browser decks, Article infographics, Optional images and videos, Markdown guidance]

**Output Format:** [Self-contained visual artifacts and Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The selected workflow determines the artifact format. Optional image and video generation uses external providers after confirmation.]

## Skill Version(s):

0.10.8 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
