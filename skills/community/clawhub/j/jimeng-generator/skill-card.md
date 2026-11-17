## Description:

Generates images with VolcEngine Jimeng AI 4.0 from text prompts, reference images, and image-editing requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[felixhsp](https://clawhub.ai/user/felixhsp)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to generate or edit images through VolcEngine Jimeng AI 4.0, returning saved PNG files and task metadata from a command-line workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Long-lived VolcEngine credentials or unsafe local .env handling could expose cloud access.

Mitigation: Use short-lived, least-privilege VolcEngine credentials where possible, add a .gitignore before creating secrets, and review credential handling before installation.

Risk: Private reference image URLs may be sent to VolcEngine or downloaded by the script.

Mitigation: Avoid private image URLs and provide only references approved for external processing.

Risk: Dependency and lockfile supply-chain issues may affect installation.

Mitigation: Review or update the npm dependency lockfile before running npm install.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/felixhsp/skills/jimeng-generator)
- [VolcEngine Jimeng 4.0 API reference](docs/jimengv4.md)
- [VolcEngine authorization reference](docs/authorization.md)
- [VolcEngine signing method documentation](https://www.volcengine.com/docs/6369/67269)
- [VolcEngine common response fields and error codes](https://www.volcengine.com/docs/6444/69728)

## Skill Output:

**Output Type(s):** [files, JSON, shell commands, configuration]

**Output Format:** [JSON status object with optional local PNG file paths and image URLs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires VolcEngine credentials; can save PNG files to an output directory or return URLs only.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
