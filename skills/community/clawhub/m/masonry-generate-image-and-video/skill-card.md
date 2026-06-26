## Description: <br>
Masonry helps agents generate images and videos, manage jobs, and explore models through the Masonry CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[junaid1460](https://clawhub.ai/user/junaid1460) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external users use this skill when they want an agent to generate images or videos, inspect available models, track generation jobs, and download completed media through Masonry. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Masonry account credentials and may process private prompts or reference images through an external service. <br>
Mitigation: Use an appropriately scoped Masonry token, prefer environment-variable setup, and submit only content that is acceptable for Masonry processing. <br>
Risk: The skill depends on the Masonry CLI package and external Masonry service availability. <br>
Mitigation: Install only trusted versions of @masonryai/cli and verify command output, job IDs, and model keys from Masonry responses before acting on them. <br>


## Reference(s): <br>
- [Masonry homepage](https://masonry.so) <br>
- [Masonry pricing](https://masonry.so/pricing) <br>
- [ClawHub skill page](https://clawhub.ai/junaid1460/masonry-generate-image-and-video) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, JSON, Files, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, JSON command responses, and downloaded media file paths.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated media is downloaded through Masonry job commands and surfaced to the user with MEDIA path lines.] <br>

## Skill Version(s): <br>
1.1.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
