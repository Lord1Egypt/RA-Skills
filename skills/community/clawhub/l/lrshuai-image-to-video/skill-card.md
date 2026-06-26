## Description: <br>
Generates videos from an image and text prompt using supported remote video-generation models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lrshu](https://clawhub.ai/user/lrshu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users can invoke this skill to submit image-to-video generation requests with a prompt, optional first or last frame media, and a selected supported model. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, selected image or video files, and an API token are sent to a configurable remote service. <br>
Mitigation: Verify the provider and TEAM_BASE_URL before use, avoid sensitive or proprietary media, and run with a scoped API key. <br>
Risk: Remote data handling and execution scoping are weakly disclosed in the available evidence. <br>
Mitigation: Review the provider's data-handling terms and prefer deployment only in environments where external media processing is approved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lrshu/lrshuai-image-to-video) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, JSON] <br>
**Output Format:** [Command-line output with status messages and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TEAM_API_KEY and prompt/media inputs; may poll for asynchronous generation results.] <br>

## Skill Version(s): <br>
1.0.2 (source: evidence release and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
