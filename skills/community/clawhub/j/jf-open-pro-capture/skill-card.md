## Description:

Captures real-time or thumbnail images from one or more JFTech devices, manages device tokens, and can optionally download captured images locally.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jftech](https://clawhub.ai/user/jftech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and camera operations teams use this skill to request single-device or batch cloud snapshots from JFTech-connected devices, then consume returned image URLs or saved image files for operational review.

### Deployment Geography for Use:

China, Asia, Europe, and North America

## Known Risks and Mitigations:

Risk: Camera credentials, app secrets, device tokens, and returned image URLs may be exposed through command-line arguments, shell history, logs, or shared output.

Mitigation: Prefer environment variables or a secrets manager, avoid passing real device passwords on the command line, and treat token values, image URLs, and captured files as sensitive.

Risk: A weakly scoped API endpoint setting could send requests outside the intended JFTech service region.

Mitigation: Set JF_ENDPOINT only to the documented JFTech API domains: api-cn.jftechws.com, api-as.jftechws.com, api-eu.jftechws.com, or api-na.jftechws.com.

Risk: Downloaded images may be written unexpectedly on shared or privileged machines.

Mitigation: Avoid --download on shared or privileged machines until endpoint, URL, size, and filename validation are improved; when downloading, use a controlled output directory and review retention requirements.

## Reference(s):

- [JFTech Open Platform documentation](https://docs.jftech.com)
- [JFTech cloud snapshot pricing](https://aops.jftech.com/#/pricing?lang=zh&tab=MEDIA_PROCESSING)
- [ClawHub skill page](https://clawhub.ai/jftech/skills/jf-open-pro-capture)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, files]

**Output Format:** [Plain text status messages or JSON objects; optional downloaded image files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JFTech API credentials and online, bound devices; returned image URLs and device tokens are documented as valid for 24 hours.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
