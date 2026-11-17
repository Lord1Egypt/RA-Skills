## Description:

Generates a single image through an OpenAI-compatible image API using explicitly supplied prompt, endpoint, API key, model, size, task name, and timeout, then saves the image locally and returns structured status JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jerryxn](https://clawhub.ai/user/jerryxn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and workflow builders use this skill as a single-image generation node that accepts explicit runtime parameters and returns a local image path plus structured success or failure details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports that the skill tells users to run an unbundled absolute-path Python script.

Mitigation: Use the skill only after verifying or bundling the referenced script with the release.

Risk: The security review reports that API keys may be passed through command-line inputs.

Mitigation: Avoid placing real API keys in commands or example files; prefer a protected environment variable, secret store, or stdin-style secret input.

Risk: The skill requires user-supplied API endpoints and output directories.

Mitigation: Restrict the endpoint and output directory to locations the operator trusts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jerryxn/skills/img2-generate-only)
- [Publisher profile](https://clawhub.ai/user/jerryxn)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON examples and shell command examples; the referenced runtime script returns structured JSON and a local image file path.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Single-image generation only; successful runs return ok, stage, image_path, bytes, base_url, model, and size, with optional base64 output when requested.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
