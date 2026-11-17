## Description:

Azure Foundry image generation skill for OpenClaw; generates images via a Foundry deployment and returns image bytes or URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jacqueskang](https://clawhub.ai/user/jacqueskang)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to configure an agent to call an Azure Foundry image-generation deployment and retrieve generated image bytes or result URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A primary Azure API key could be sent to an arbitrary or plaintext endpoint if FOUNDRY_ENDPOINT is set unsafely.

Mitigation: Set FOUNDRY_ENDPOINT only to a trusted HTTPS Azure Foundry or Cognitive Services endpoint and keep FOUNDRY_API_KEY narrowly scoped.

Risk: The documented example uses fixed /tmp paths that may be inappropriate on shared machines.

Mitigation: Replace fixed /tmp paths with a private mktemp directory before use in shared environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jacqueskang/skills/ms-foundry-image-gen)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Files]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated images may be returned as image bytes saved to a file or as URLs, depending on the Foundry deployment response.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
