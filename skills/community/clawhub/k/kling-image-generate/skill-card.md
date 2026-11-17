## Description:

Kling Image Generate helps agents use Kling AI image-generation APIs for text-to-image, image-to-image, multi-image reference generation, Omni-Image, image expansion, task querying, and task listing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[umrzcz-831](https://clawhub.ai/user/umrzcz-831)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to configure Kling API credentials and run scripts that generate, edit, expand, and track AI image tasks through Kling's cloud API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, reference images, and generated task data are sent to Kling's cloud API.

Mitigation: Use the skill only when Kling is approved for the intended data, and avoid sensitive prompts, private images, regulated data, and internal callback URLs unless that approval is in place.

Risk: Kling access and secret keys are required for JWT authentication.

Mitigation: Store keys in local environment variables only, keep them out of shared shells, logs, and source control, and rotate them if exposure is suspected.

## Reference(s):

- [Kling Image Generation API Reference](references/api-reference.en.md)
- [Kling Image Generation API Reference (Chinese)](references/api-reference.md)
- [Kling API endpoint](https://api-beijing.klingai.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses from bundled Python scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include generated image URLs, task IDs, task status JSON, progress text, and configuration steps for local environment variables.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
