## Description: <br>
Generates short and promotional videos from text prompts, images, first/last frames, or reference images through IMA Studio video-generation services. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[allenfancy-gan](https://clawhub.ai/user/allenfancy-gan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, marketers, and developers use this skill to create video clips from prompts or source images, including text-to-video, image-to-video, first/last-frame interpolation, and reference-image guided video generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends prompts, selected media, and the IMA API key to IMA Studio services. <br>
Mitigation: Use a scoped or test API key for evaluation, avoid sharing logs or screenshots that contain credentials or local paths, and run only when external IMA service use is intended. <br>
Risk: Local media and derived cover frames may be uploaded through an upload-token flow to a pre-signed HTTPS storage URL. <br>
Mitigation: Review media before upload and avoid sensitive content unless the operator has approved use of IMA Studio upload services. <br>
Risk: Remote media URLs may be downloaded temporarily for probing, validation, or video-cover extraction. <br>
Mitigation: Use direct public HTTPS media URLs only and rely on the skill's documented rejection of credentialed, redirected, private, loopback, and oversized remote media. <br>
Risk: Video generation can consume account credits and poll for long-running tasks. <br>
Mitigation: Run the low-cost doctor check first, start with lower-cost model and resolution settings, and increase duration or quality only after a small validation run succeeds. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/allenfancy-gan/ima-video-ai) <br>
- [IMA homepage](https://www.imaclaw.ai) <br>
- [References map](artifact/references/README.md) <br>
- [Security and network behavior](artifact/references/shared/security-and-network.md) <br>
- [Model selection policy](artifact/references/shared/model-selection-policy.md) <br>
- [API contract and errors](artifact/references/operations/api-contract-and-errors.md) <br>
- [Video capability](artifact/capabilities/video/CAPABILITY.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance and CLI output JSON containing remote HTTPS video result URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns remote HTTPS video result URLs; generated videos are not converted into local file attachments by the skill.] <br>

## Skill Version(s): <br>
1.0.13 (source: server release metadata; artifact frontmatter reports 1.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
