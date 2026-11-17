## Description:

Generates short vertical comic-video clips from storyboard keyframes using Volcengine Ark Seedance 2.0, with 5-second scenes, up to 3 concurrent jobs, and returned last frames for continuity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaobod1](https://clawhub.ai/user/zhaobod1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content automation agents use this skill to turn storyboard JSON and matching keyframe images into short vertical comic-video clips. It is intended for ClawHub users who can provide a Volcengine Ark API key and review generated media outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scene IDs and paths may cause reads, uploads, or writes outside the intended project folders.

Mitigation: Review script JSON and storyboard filenames before running, and use a dedicated project directory containing only intended input frames and output paths.

Risk: Frames and prompts are sent to Volcengine Ark using ARK_API_KEY.

Mitigation: Use only content approved for that provider, protect the API key, and avoid sensitive or regulated inputs unless provider terms allow it.

Risk: The bundled cost cap should not be treated as a hard spending guard.

Mitigation: Set provider-side budgets or quotas and check scene count, duration, resolution, and fast-mode settings before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhaobod1/skills/huo15-comic-video)
- [Volcengine Seedance video generation documentation](https://www.volcengine.com/docs/82379/1520757)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown instructions with command-line examples; generated MP4 clips and last-frame PNG files when executed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses storyboard JSON, keyframe images, ARK_API_KEY, scene duration, resolution, and fast-mode settings.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
