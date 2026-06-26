## Description: <br>
Enhances user-provided photos with a Canon IXUS 130-style CCD effect and an optional custom bottom watermark. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[x0cd](https://clawhub.ai/user/x0cd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
People and creative-tool agents use this skill to apply a classic compact-camera photo treatment, normalize the image to a vertical 9:16 frame, and optionally add a user-supplied watermark. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Photos are cropped or padded to a 9:16 frame, which can change composition or add black bars. <br>
Mitigation: Review the output against the original image before using it in publication workflows. <br>
Risk: User photos are processed by the skill runtime and may contain sensitive personal or business content. <br>
Mitigation: Avoid submitting sensitive images unless the runtime and platform handling meet the user's data-handling requirements. <br>
Risk: The artifact depends on the sharp package with a semver range rather than an exact version pin. <br>
Mitigation: Pin and rescan the dependency before deployment in controlled production environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/x0cd/pixcakeai) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Image] <br>
**Output Format:** [Base64-encoded JPEG response] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [JPEG quality 95%, progressive encoding, optional bottom watermark, and 9:16 crop or padding.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
