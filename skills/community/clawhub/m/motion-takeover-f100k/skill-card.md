## Description:

Plans full-screen motion-graphics takeovers for horizontal YouTube videos from a pre-cut SRT and face reference, then delivers timed assets and a montage sheet for external editing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[formula100k](https://clawhub.ai/user/formula100k)

### License/Terms of Use:

MIT-0

## Use Case:

Video creators and production teams use this skill to plan and generate full-screen 16:9 takeover assets, lightweight face-mode overlays, and exact timing instructions for a YouTube edit without composing over the source video inside the skill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional global installs and external rendering dependencies may be unsuitable for sensitive production environments.

Mitigation: Review install commands before use and vendor or pin rendering dependencies where environment control matters.

Risk: Paid or external media generation can produce unusable motion if text becomes distorted or timing is wrong.

Mitigation: Approve the motion board before generation, review legibility after animation, and fall back to the rendered PNG when motion deforms text.

Risk: Departing from the stated asset-delivery workflow can create audio-sync or timeline mistakes during final editing.

Mitigation: Use the montage sheet against the pre-cut video, place takeovers as opaque overlays at the listed times, and verify sync in the editor.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/formula100k/skills/motion-takeover-f100k)
- [Publisher profile](https://clawhub.ai/user/formula100k)
- [takeover-template.html](artifact/templates/takeover-template.html)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with JSON planning data, HTML scene templates, PNG or MP4 assets, and montage-sheet files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs target 1920x1080 16:9 video workflows and are intended to be reviewed before paid media generation or external editing.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
