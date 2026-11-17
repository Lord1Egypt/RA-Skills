## Description:

Jiuma Free Image2Video uses the Jiuma AI API to generate videos from a first-frame image, optional end-frame image, and text prompt.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dddcn1](https://clawhub.ai/user/dddcn1)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to submit image-to-video jobs to Jiuma AI, check generation status, and retrieve the resulting video URL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Images and prompts are sent to the Jiuma API for video generation.

Mitigation: Use only images and prompts that are appropriate to share with Jiuma, and avoid private or sensitive content.

Risk: A Jiuma API key is stored in a predictable plaintext local file.

Mitigation: Run the skill in a private workspace, restrict permissions on the credential file, and delete or rotate the key if the workspace is shared, backed up, or exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dddcn1/skills/jiuma-free-image2video)
- [Login documentation](artifact/LOGIN.md)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Configuration guidance]

**Output Format:** [JSON returned by Python command-line scripts, with video URLs and task status fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Submits prompts and images to Jiuma API endpoints; generated video links are returned after polling by task ID.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
