## Description:

Creates Amazon listing main images, supporting images, and A+ page assets using GPT Image 2.6 through Qinghu AI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Amazon sellers use this skill to prepare prompts and generate main listing images, supporting images, and A+ assets for a selected marketplace, category, placement, size, and language.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reference images and prompts are sent to Qinghu's China service.

Mitigation: Upload only suitable material and verify the CLI package and configured service endpoint before use.

Risk: The external CLI and service behavior have not been independently verified, and image generation may incur charges.

Mitigation: Protect the API key in process environment variables, review the cost estimate, and obtain user confirmation before paid generation.

## Reference(s):


## Skill Output:

**Output Type(s):** [Images, Guidance, Shell commands, Configuration]

**Output Format:** [Generated image files, JSON task and result files, and Markdown or text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prompts are limited to 5,000 characters; model-specific image options determine available sizes and image counts.]

## Skill Version(s):

0.1.0 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
