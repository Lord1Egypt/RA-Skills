## Description: <br>
Generates videos from text prompts by invoking supported remote video-generation models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lrshu](https://clawhub.ai/user/lrshu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and users use this skill to generate videos from short text prompts with models such as Veo 3.1, Sora 2, and Doubao Seedance 1.5 Pro. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send API credentials, prompts, and optional local media to a remote service selected by environment configuration. <br>
Mitigation: Use a least-privilege TEAM_API_KEY, confirm TEAM_BASE_URL points to the intended trusted HTTPS service, and avoid private prompts or local media unless remote upload is acceptable. <br>
Risk: Video generation uses remote processing and may incur provider costs. <br>
Mitigation: Review prompts and model choices before execution, and monitor usage through the configured provider account. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lrshu/lrshuai-text-to-video) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/lrshu) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, JSON] <br>
**Output Format:** [Command-line output with JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TEAM_API_KEY and may use TEAM_BASE_URL to select the remote service endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
