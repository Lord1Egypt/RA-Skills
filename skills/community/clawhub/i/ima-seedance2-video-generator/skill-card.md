## Description: <br>
Seedance 2.0 video generator for text-to-video, image-to-video, first-last-frame, and reference-media workflows with image, video, and audio references. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[allenfancy-gan](https://clawhub.ai/user/allenfancy-gan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content teams use this skill to generate short videos from prompts, images, first and last frames, or reference media. It supports cinematic clips, product demos, storyboard exploration, social media assets, and consistent-character workflows through the IMA Seedance 2.0 models. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, remote media URLs, and local media inputs may be sent to external IMA-related services. <br>
Mitigation: Use public or approved media for initial runs, avoid private prompts or proprietary assets unless the environment is approved, and use a scoped or test API key. <br>
Risk: Auto-consent can bypass interactive compliance confirmation for asset checks. <br>
Mitigation: Leave IMA_AUTO_CONSENT disabled unless the execution environment and input sources are controlled. <br>
Risk: User-provided remote media URLs may be fetched for validation or probing. <br>
Mitigation: Avoid internal URLs and require direct downloadable URLs from trusted sources. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/allenfancy-gan/ima-seedance2-video-generator) <br>
- [IMA Homepage](https://www.imaclaw.ai) <br>
- [Execution Protocol](references/protocols/execution.md) <br>
- [Event Stream Protocol](references/protocols/event-stream.md) <br>
- [Create Task Contract](references/contracts/create-task.md) <br>
- [Reference Media Rules](references/limits/reference-media-rules.md) <br>
- [Security Disclosure](SECURITY.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown-style status updates, shell invocations, event/status text, and generated video result links or file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires IMA_API_KEY; local and non-HTTPS media may be uploaded through IMA-related services, and local logs are auto-cleaned after 7 days.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
