## Description: <br>
Captures current images or thumbnails from one or more JFTech devices, manages device tokens, and can download captures locally. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jftech](https://clawhub.ai/user/jftech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and device operators with JFTech Open Platform credentials use this skill to capture real-time images or thumbnails from single devices or batches of devices, including multi-channel devices. <br>

### Deployment Geography for Use: <br>
China Mainland, Asia, Europe, and North America through configured JFTech regional API endpoints. <br>

## Known Risks and Mitigations: <br>
Risk: JFTech app secrets, device tokens, or device passwords could expose device access if handled insecurely. <br>
Mitigation: Install only from the trusted publisher, store secrets in protected environment or secret-management systems, and avoid passing device passwords on the command line. <br>
Risk: Captured image URLs and downloaded files may contain sensitive visual data. <br>
Mitigation: Use restricted output directories, define a retention plan, and avoid sharing temporary capture URLs. <br>
Risk: Requests may be sent to an unintended API endpoint if the regional endpoint is misconfigured. <br>
Mitigation: Use only known JFTech regional endpoints and verify JF_ENDPOINT before running capture commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jftech/jf-open-pro-capture) <br>
- [JFTech Open Platform](https://developer.jftech.com) <br>
- [JFTech cloud capture pricing](https://aops.jftech.com/#/pricing?lang=zh&tab=MEDIA_PROCESSING) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with Python CLI commands; script execution can print text or JSON and optionally write image files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include 24-hour image URLs and downloaded camera images.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
