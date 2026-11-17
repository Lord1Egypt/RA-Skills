## Description:

Guides users through selecting JFTech open-platform AI detection algorithms, configuring authorized credentials, calling image or camera-capture analysis workflows, and producing structured detection reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jftech](https://clawhub.ai/user/jftech)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and operations teams use this skill to match safety, retail, perimeter, vehicle, sanitation, and image-quality scenarios to supported JFTech detection algorithms, then run authorized analyses on supplied images or device captures.

### Deployment Geography for Use:

Global; the primary algorithm endpoint is global, while the optional device-capture dependency documents CN, AS, EU, and NA regional endpoints.

## Known Risks and Mitigations:

Risk: The skill handles JFTech credentials and stores appSecret-derived configuration locally.

Mitigation: Protect and rotate any appSecret used with the skill, do not commit config.json, and avoid exposing secrets in conversation or logs.

Risk: The skill can process media and camera-capture workflows that may involve sensitive or unauthorized images.

Mitigation: Install and run it only in an authorized JFTech environment with approved images, devices, and account permissions.

Risk: The optional camera workflow can install or rely on an unpinned remote jf-open-pro-capture dependency.

Mitigation: Review and pin the jf-open-pro-capture dependency before enabling automatic installation or camera capture.

Risk: Custom API endpoints could redirect credentialed requests away from the expected JFTech service.

Mitigation: Use the documented JFTech endpoints and avoid custom endpoints unless they have been explicitly approved.

## Reference(s):

- [JFTech Open Algorithm Reference](artifact/reference.md)
- [Algorithm Metadata](artifact/algorithms.json)
- [ClawHub Skill Page](https://clawhub.ai/jftech/skills/jf-open-algo-assistant)
- [JFTech Device Capture Dependency](https://clawhub.ai/jftech/jf-open-pro-capture)

## Skill Output:

**Output Type(s):** [guidance, markdown, text, code, shell commands, configuration]

**Output Format:** [Markdown guidance with shell commands, configuration instructions, JSON result summaries, and optional evidence image paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local result JSON files and rendered evidence images when the user supplies authorized credentials and media inputs.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter metadata reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
