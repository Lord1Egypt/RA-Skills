## Description:

Measures finished AI-made video, image, and audio for defects, then ranks takes using timestamped evidence and targeted visual review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vargai](https://clawhub.ai/user/vargai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use the skill to inspect completed AI-generated media, review measured defects with visual evidence, compare it with references, and rank candidate takes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Network downloads and unpinned installation sources may introduce unexpected or changing dependencies and model files.

Mitigation: Review download locations and installation sources, and pin the sources and versions before installing or running the skill.

Risk: Analysis output can contain face crops that may identify people in the media.

Mitigation: Limit access to generated evidence folders and remove face crops when they are no longer needed.

## Reference(s):

- [ClawHub media-judge release](https://clawhub.ai/vargai/skills/media-judge)
- [Homepage listed in skill metadata](https://github.com/vargHQ/skills/tree/main/media-judge)
- [Guide to judging an AI video without bias](https://varg.ai/how-to/judge-an-ai-video-without-bias)
- [TempGlitch paper](https://arxiv.org/abs/2605.21443)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON, Evidence files]

**Output Format:** [Markdown reports with JSON findings and timestamped evidence images]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings include measured evidence and timestamps; results are not reduced to a single quality score.]

## Skill Version(s):

1.0.8 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
