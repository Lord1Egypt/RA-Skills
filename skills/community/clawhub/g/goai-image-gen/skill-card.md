## Description: <br>
Generates GoAI images from user prompts, with optional reference images, via the GoAI API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[goai](https://clawhub.ai/user/goai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate or edit images from prompts or reference images through GoAI while preserving the user's original prompt language. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and reference images are sent to mustgoai.com or a configured GoAI endpoint. <br>
Mitigation: Avoid submitting sensitive photos, documents, proprietary artwork, or confidential prompts unless that endpoint is approved for the intended data. <br>
Risk: Generated media URLs may be externally accessible. <br>
Mitigation: Treat result URLs as shareable links and avoid generating or distributing sensitive content through this workflow. <br>
Risk: The skill requires a GoAI API key. <br>
Mitigation: Use a dedicated API key where possible and rotate or revoke it according to the user's credential-management policy. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/goai/goai-image-gen) <br>
- [GoAI Homepage](https://mustgoai.com) <br>
- [Publisher Profile](https://clawhub.ai/user/goai) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files, configuration, guidance] <br>
**Output Format:** [Plain text result lines with local file paths and public media URLs; agent-facing guidance may be rendered as Markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires uv and GOAI_API_KEY; generated media is saved locally and returned with externally accessible media URLs when the GoAI API succeeds.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence; artifact frontmatter and pyproject.toml remain 0.3.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
