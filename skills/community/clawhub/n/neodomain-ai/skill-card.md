## Description: <br>
Generate images and videos via Neodomain AI API. Supports text-to-image, image-to-video, text-to-video, and motion control video generation. Use when user wants to create AI-generated images or videos using the Neodomain platform. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BandWhite](https://clawhub.ai/user/BandWhite) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creators use this skill to call Neodomain AI from an agent workflow for image generation, video generation, reference-image generation, motion-control video, and model listing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends prompts, reference media URLs, uploaded storyboard or media files, and generated outputs to the Neodomain cloud service. <br>
Mitigation: Use it only with content the user intends to send to Neodomain, and avoid sensitive prompts or media unless the user has approved that transfer. <br>
Risk: Access tokens can be exposed through shared shell startup files, terminal history, or logs. <br>
Mitigation: Prefer a temporary or protected token store, avoid committing shell configuration changes, and do not paste token output into logs. <br>
Risk: The login flow can involve a phone number or email address and a verification code. <br>
Mitigation: Use only an approved account contact and handle verification codes and returned tokens privately. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/BandWhite/neodomain-ai) <br>
- [Neodomain service endpoint](https://story.neodomain.cn) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Files, JSON, Guidance] <br>
**Output Format:** [CLI output, generated media files, and JSON metadata] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates JPEG, PNG, or WebP images, MP4 videos and thumbnails, and metadata.json files in the configured output directory; requires python3 and NEODOMAIN_ACCESS_TOKEN.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
