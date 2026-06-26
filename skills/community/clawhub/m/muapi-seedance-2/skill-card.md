## Description: <br>
Expert Cinema Director skill for Seedance 2.0 (ByteDance): high-fidelity video generation using technical camera grammar and multimodal references for text-to-video, image-to-video, and video extension. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Anil-matcha](https://clawhub.ai/user/Anil-matcha) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, developers, and agents use this skill to convert creative video intent into structured Director Brief prompts and shell commands for Seedance 2.0 text-to-video, image-to-video, and video extension workflows via MuAPI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, image URLs, uploaded images, and video-generation requests are sent to an external generation provider. <br>
Mitigation: Avoid secrets, confidential prompts, private media, and internal image URLs unless the operator is comfortable sharing them with the provider. <br>
Risk: The MuAPI key is required for API access and could be exposed if placed in shared files or logs. <br>
Mitigation: Use a limited API key, store it in a controlled environment or secret manager, avoid committing .env files, and rotate the key if exposure is suspected. <br>
Risk: The shell script can upload local image files and download generated video outputs into the workspace. <br>
Mitigation: Review shell commands before running them, confirm selected input files, and run the skill from an appropriate workspace before downloading generated media. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Anil-matcha/muapi-seedance-2) <br>
- [MuAPI API base](https://api.muapi.ai/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, api calls, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with Director Brief prompt structure, bash command examples, request IDs, JSON responses, video URLs, and optional downloaded media files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MUAPI_KEY for MuAPI calls; supports asynchronous jobs, local image uploads, up to 9 image references for image-to-video, and optional download of generated videos.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence; artifact frontmatter says 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
