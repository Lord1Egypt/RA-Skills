## Description:

Uses the Pexels API to search for and download high-quality free images, with resizing, format validation, and metadata capture.

This skill is ready for commercial/non-commercial use.

## Publisher:

[glittering](https://clawhub.ai/user/glittering)

### License/Terms of Use:

MIT

## Use Case:

Developers, content creators, and agents use this skill to retrieve Pexels images for social media and visual-content workflows, resize them for target platforms, and save source metadata for later review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Pexels API key and performs remote API calls and image downloads.

Mitigation: Use a dedicated API key, keep it out of source control, and run the downloader in a controlled environment.

Risk: Downloaded images and metadata are written to a local directory selected by the user.

Mitigation: Use a dedicated output folder and review downloaded files and saved metadata before reuse or publication.

Risk: Dependencies are declared with minimum versions rather than exact pins.

Mitigation: Install in a virtual environment and pin or regularly update dependencies according to local security policy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/glittering/skills/pexels-image-downloader)
- [Pexels API documentation](https://www.pexels.com/api/documentation/)
- [Pexels API](https://www.pexels.com/api/)
- [Pillow documentation](https://pillow.readthedocs.io/)
- [Optimize Images guidance](https://developers.google.com/speed/docs/insights/OptimizeImages)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration, files, JSON]

**Output Format:** [Markdown guidance with bash and Python examples; generated local image files and JSON metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Pexels API key, makes network requests to Pexels, and writes downloaded images plus metadata to a chosen local output directory.]

## Skill Version(s):

1.0.0 (source: package.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
