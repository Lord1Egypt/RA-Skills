## Description: <br>
Edit and enhance images and videos with AI via muapi.ai, including prompt-based editing, upscaling, background removal, face swap, lipsync, video effects, and more. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Anil-matcha](https://clawhub.ai/user/Anil-matcha) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creative operators use this skill to run muapi.ai media-editing workflows from shell scripts for image edits, enhancements, lipsync, and video effects. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected media and prompts are sent to muapi.ai and may be processed by downstream providers. <br>
Mitigation: Use only media the user is authorized to upload and avoid sensitive, regulated, confidential, or private personal content. <br>
Risk: The scripts require a muapi.ai API key and some helper paths can save it to a local .env file. <br>
Mitigation: Prefer MUAPI_KEY from the shell or a secret manager; if .env is used, keep it private, out of source control, and permission-restricted. <br>
Risk: Face swap, lipsync, and voice or likeness workflows can create misleading impersonation or unauthorized identity edits. <br>
Mitigation: Use only authorized face, voice, and likeness inputs, and review outputs for consent, disclosure, and policy requirements before sharing. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Anil-matcha/muapi-edit) <br>
- [muapi.ai API endpoint](https://api.muapi.ai/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, JSON, guidance] <br>
**Output Format:** [Shell command output and JSON API result payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can return asynchronous request IDs or completed media result URLs depending on flags and operation.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact frontmatter reports 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
