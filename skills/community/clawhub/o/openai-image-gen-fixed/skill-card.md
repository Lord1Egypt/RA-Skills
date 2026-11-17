## Description:

Batch-generate images via the OpenAI Images API with random prompt sampling and an index.html gallery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[saschaspoonbill](https://clawhub.ai/user/saschaspoonbill)

### License/Terms of Use:


## Use Case:

Developers and creative agents use this skill to generate batches of images from structured or user-provided prompts, then inspect the resulting PNG files, prompt mapping, and HTML gallery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A custom OpenAI-compatible endpoint can receive the API key and prompt content if OPENAI_BASE_URL or OPENAI_API_BASE is set unexpectedly.

Mitigation: Run in a trusted environment and leave OPENAI_BASE_URL and OPENAI_API_BASE unset unless intentionally using a trusted compatible endpoint.

Risk: Prompts and generated output metadata may contain confidential or sensitive information.

Mitigation: Avoid putting secrets, credentials, private data, or confidential business information in prompts.

Risk: The generated HTML gallery may be unsafe to open when prompts come from an untrusted source.

Mitigation: Do not open galleries generated from untrusted prompts until the HTML escaping issue identified by the security guidance is fixed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/saschaspoonbill/skills/openai-image-gen-fixed)

## Skill Output:

**Output Type(s):** [Files, Images, JSON, HTML, Shell commands]

**Output Format:** [PNG image files, prompts.json, index.html gallery, and command-line status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OPENAI_API_KEY; accepts count, model, prompt, size, quality, timeout, sleep, output directory, API key, and dry-run options.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
