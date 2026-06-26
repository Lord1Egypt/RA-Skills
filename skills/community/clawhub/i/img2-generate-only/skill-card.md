## Description: <br>
Generates one image from an explicitly supplied prompt, OpenAI-compatible image endpoint, API key, model, size, task name, and timeout, then saves the image locally and returns structured status JSON. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jerryxn](https://clawhub.ai/user/jerryxn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and workflow authors use this skill to run a single-image generation step against a trusted OpenAI-compatible image service and receive a local image path plus structured success or failure details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill passes an API key to a hard-coded local Python script that is not included in the package for review. <br>
Mitigation: Review or obtain the referenced script before use, and only provide a real API key after confirming the script and execution environment are trusted. <br>
Risk: The base URL and API key are supplied by the user or workflow, so an untrusted endpoint or exposed command-line secret could leak credentials. <br>
Mitigation: Use only trusted image-generation endpoints and prefer environment variables or a secret store over command-line API-key arguments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jerryxn/img2-generate-only) <br>


## Skill Output: <br>
**Output Type(s):** [Files, JSON, Shell commands, Guidance] <br>
**Output Format:** [Structured JSON status with a local image file path, and optional base64 image data when requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates exactly one image per invocation; n must be 1.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release evidence and artifact/_meta.json; SKILL.md frontmatter says 3.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
