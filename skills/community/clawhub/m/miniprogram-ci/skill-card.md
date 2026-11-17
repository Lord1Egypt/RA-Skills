## Description:

Automate WeChat Mini Program code upload, preview, npm build, and cloud deployments with CI/CD support using Node.js or CLI without opening DevTools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlark](https://clawhub.ai/user/openlark)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release engineers use this skill to prepare WeChat Mini Program and mini game CI/CD workflows for upload, preview, npm build, cloud function deployment, cloud storage upload, and cloud container deployment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill guides users through upload and cloud deployment actions that can affect live WeChat Mini Program resources.

Mitigation: Require explicit review of appid, robot, version, cloud environment, and deployment target before any upload or cloud deploy command runs.

Risk: The workflow uses upload private keys and app identifiers that are sensitive deployment credentials.

Mitigation: Keep private keys out of source control, restrict keys and IP allowlists, and use project-local credential handling.

Risk: Some documented cloud storage and cloud container operations require mutable alpha package installs.

Mitigation: Use a pinned, reviewed package version and avoid alpha tags for production deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/openlark/skills/miniprogram-ci)
- [CLI Command Reference](references/cli.md)
- [Cloud Development API Reference](references/cloud.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with JavaScript and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes CI/CD setup guidance that may affect upload, preview, and cloud deployment targets.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
