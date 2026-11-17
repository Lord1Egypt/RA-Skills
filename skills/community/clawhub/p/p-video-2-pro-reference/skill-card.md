## Description:

Guides creation of one cinematic video clip conditioned on image or video references, with optional audio guidance or a retained soundtrack.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pruna-ai](https://clawhub.ai/user/pruna-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and developers use this skill to plan and generate one short cinematic clip from approved image or video references through Pruna, optionally using audio for guidance or retaining an uploaded soundtrack.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reference media is sent to Pruna for generation.

Mitigation: Upload only media the user has approved and intentionally wants shared with Pruna.

Risk: API credentials could be exposed during upload or generation.

Mitigation: Keep PRUNA_API_KEY private and never include it in shared output.

Risk: Installing unreviewed companion skills may introduce untrusted instructions.

Mitigation: Trust and review companion skill sources; use a pinned or preapproved skills CLI before running installation examples.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/pruna-ai/skills/p-video-2-pro-reference)

## Skill Output:

**Output Type(s):** [Video, Shell commands, Guidance]

**Output Format:** [MP4 video; text guidance with inline curl commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One 5–15-second clip at 480p or 768p and 24 fps, with generated sound or an approved uploaded soundtrack.]

## Skill Version(s):

1.0.15 (source: ClawHub release metadata and skill frontmatter metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
