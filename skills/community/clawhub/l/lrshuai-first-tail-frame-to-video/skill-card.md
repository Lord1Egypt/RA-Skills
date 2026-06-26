## Description: <br>
Generates video from a text prompt plus first-frame and tail-frame image inputs using supported image-to-video models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lrshu](https://clawhub.ai/user/lrshu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to submit a prompt with first and final frame media to supported video generation models and inspect the returned generation result. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends the configured credential and selected prompt, image, or video inputs to a remote service endpoint. <br>
Mitigation: Use a scoped TEAM_API_KEY, confirm TEAM_BASE_URL is unset or points to the intended provider, and avoid sensitive media unless the provider's handling and retention are acceptable. <br>
Risk: The release requires direct Python execution and a configurable remote endpoint, which increases trust requirements for the local script and environment. <br>
Mitigation: Review the script before installation or execution and run it only in an environment where the credential and outbound network destination are acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lrshu/lrshuai-first-tail-frame-to-video) <br>
- [Default remote video-generation endpoint](https://dlazy.com/api/ai/tool) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API calls, Text, JSON] <br>
**Output Format:** [Console text with JSON responses from the remote video-generation API] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python, TEAM_API_KEY, a model ID, a prompt, and first-frame or tail-frame media inputs; may poll until generation completes.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
