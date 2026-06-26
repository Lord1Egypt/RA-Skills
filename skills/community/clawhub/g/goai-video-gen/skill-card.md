## Description: <br>
Generates text-to-video and image-to-video clips through the GoAI API while preserving the user's prompt language. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[goai](https://clawhub.ai/user/goai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate videos from text prompts or reference images through GoAI, including Chinese-language requests. The skill returns both a saved local MP4 path and a public media URL after successful generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and local reference images are sent to GoAI for video generation. <br>
Mitigation: Avoid using private or sensitive prompts and images unless the user is comfortable uploading them to GoAI. <br>
Risk: The generated media URL may be externally shareable. <br>
Mitigation: Treat returned URLs as public or shareable and avoid generating content that should remain confidential. <br>
Risk: An exposed GOAI_API_KEY could allow unauthorized API use. <br>
Mitigation: Keep GOAI_API_KEY private and configure it only in the intended skill environment. <br>
Risk: Changing GOAI_BASE_URL sends requests to a different endpoint. <br>
Mitigation: Leave GOAI_BASE_URL at the default production endpoint unless the user intentionally trusts another GoAI-compatible endpoint. <br>


## Reference(s): <br>
- [GoAI homepage](https://mustgoai.com) <br>
- [ClawHub skill page](https://clawhub.ai/goai/goai-video-gen) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/goai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Files, Shell commands, Configuration guidance] <br>
**Output Format:** [Plain text result lines containing local file paths and public media URLs, with concise error guidance on failure.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a local MP4 file and an externally shareable media URL; requires uv and GOAI_API_KEY.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and target metadata; artifact frontmatter and pyproject.toml report 0.3.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
