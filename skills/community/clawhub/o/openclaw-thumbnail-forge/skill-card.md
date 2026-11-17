## Description:

Local thumbnail generator for videos. Picks the best candidate frames using brightness, sharpness, and scene-change scores, composes professional thumbnails with text overlays, gradient bars, and watermarks, and ranks A/B variants on objective click-likelihood metrics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gopendrasharma89-tech](https://clawhub.ai/user/gopendrasharma89-tech)

### License/Terms of Use:

MIT

## Use Case:

Creators, marketers, and developers use this skill to turn local video frames into platform-ready thumbnails, generate A/B variants, and choose a heuristic winner without remote services or AI APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow invokes local media tools and writes generated PNG or JSON files to output paths.

Mitigation: Run scripts as a normal user, keep PATH limited to trusted directories, and choose output directories where overwriting generated files is acceptable.

Risk: Pillow is required for image processing.

Mitigation: Install Pillow in a virtual environment from a trusted package index.

Risk: Frame and click-likelihood scores are deterministic heuristics, not semantic review or real CTR prediction.

Mitigation: Treat rankings as a tie-breaker and review selected thumbnails before publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gopendrasharma89-tech/skills/openclaw-thumbnail-forge)
- [OpenClaw homepage](https://clawhub.ai/gopendrasharma89-tech/openclaw-thumbnail-forge)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration, text]

**Output Format:** [Markdown guidance with CLI commands and generated PNG or JSON file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local image assets, frame reports, variant rankings, and winner metadata in user-specified output directories.]

## Skill Version(s):

0.3.0 (source: server release metadata and SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
