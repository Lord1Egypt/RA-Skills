## Description:

This skill guides an agent through a Kujiale interior design workflow for floor-plan confirmation, style selection, automated layout, rendering, and panorama output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users, designers, and real-estate teams use this skill to turn a floor-plan search or uploaded floor-plan image into Kujiale room layouts, renderings, panorama links, and design highlights.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow requires a Kujiale access token stored in local configuration.

Mitigation: Keep .kjlconfig.json private, do not commit tokens, and review local Node scripts before running them.

Risk: Uploaded floor-plan images are sent to Kujiale for recognition and design processing.

Mitigation: Upload only floor-plan images that the user intends to send to Kujiale.

Risk: Automated layout actions may consume Kujiale account quota or credits.

Mitigation: Confirm quota-consuming layout actions with the user before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/kujiale-design)
- [Kujiale skills token page](https://www.kujiale.com/skills)
- [Kujiale design detail URL template](https://www.kujiale.com/pcenter/design/{designId}/setting?from=skills)
- [Publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands, image links, panorama links, and design highlights]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Final output is expected in ./outputs/result.md with render images prioritized by room type.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
