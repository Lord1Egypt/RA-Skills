## Description:

AI-powered fashion model pose transfer tool. Generate pose variations of a model/product image using reference pose images while keeping clothing and background consistent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[3cpj](https://clawhub.ai/user/3cpj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content production teams use this skill to generate fashion model pose variations from an original model or product image and one to four reference pose images. It can keep the original background or request a white studio background while preserving clothing and accessories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated image downloads disable TLS certificate verification, which can expose outputs to tampering in transit.

Mitigation: Run only in a constrained virtual environment and prefer a fixed release that restores standard TLS verification before production use.

Risk: Input model and pose images are sent to fal.ai for remote image generation.

Mitigation: Use only images approved for third-party processing and avoid confidential or sensitive imagery unless the external service terms and controls are acceptable.

Risk: The dependency requirement is unpinned beyond a minimum fal-client version.

Mitigation: Pin and review dependencies in the deployment environment before installing or running the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/3cpj/skills/pose-transfer)
- [fal.ai API key dashboard](https://www.fal.ai/dashboard/keys)

## Skill Output:

**Output Type(s):** [Images, JSON, Shell commands, Guidance]

**Output Format:** [Generated JPEG files, generation_results.json, and command-line status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires FAL_KEY and sends source and reference images to fal.ai for generation.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
