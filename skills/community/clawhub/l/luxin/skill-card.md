## Description:

Generate or edit images, video, audio, and 3D assets through Luxin, with hosted media links and job and cost details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danielgwilson](https://clawhub.ai/user/danielgwilson)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to generate or edit images, video, audio, or 3D assets, then retrieve hosted results and job or cost details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Refresh instructions may update unrelated skills.

Mitigation: Use a Luxin-only refresh after reviewing the changes, and avoid the unfiltered all-skills updater.

Risk: The per-image spending estimate is not a guaranteed final charge ceiling.

Mitigation: Set an explicit payment budget and treat the estimate as guidance rather than a hard cap.

Risk: Uploaded and generated media are available at public, non-expiring URLs.

Mitigation: Avoid uploading sensitive media and handle returned URLs as publicly accessible.

Risk: The external CLI implementation is outside this artifact review.

Mitigation: Pin the executable version and review current Luxin guidance before use.

## Reference(s):

- [Luxin homepage](https://luxin.sh)
- [Luxin skill guide](https://luxin.sh/skill.md)
- [Luxin full skill guidance](https://luxin.sh/skill-core.md)
- [Luxin API contract](https://luxin.sh/llms.txt)
- [Luxin hosted API](https://api.luxin.sh)
- [CLI contract](artifact/references/cli.md)
- [Command reference](artifact/references/commands.json)

## Skill Output:

**Output Type(s):** [Images, Video, Audio, 3D assets, JSON job and cost details, Hosted media URLs]

**Output Format:** [Hosted media assets with JSON job, asset, trace, and cost details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Media URLs are public and non-expiring; jobs can be re-fetched using their identifiers.]

## Skill Version(s):

1.0.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
