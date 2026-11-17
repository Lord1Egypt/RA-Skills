## Description:

Edit images with Google Nano Banana 2 through RunComfy, covering subject-preserving image-to-image edits, batch edits, schema guidance, invocation examples, and routing guidance for related image-generation skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[permew](https://clawhub.ai/user/permew)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creative operators use this skill to prepare RunComfy CLI invocations for Nano Banana 2 image edits, including background swaps, localized object edits, batch SKU edits, and ad-creative variations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install an unpinned global third-party CLI package.

Mitigation: Pin or otherwise verify `@runcomfy/cli` before installation, especially in shared, CI, or production environments.

Risk: RunComfy tokens and generated files may be exposed if run in an overly broad environment.

Mitigation: Use the least-privileged environment practical for `RUNCOMFY_TOKEN`, local RunComfy configuration, and generated output directories.

Risk: Prompts and image URLs are sent to RunComfy's cloud service.

Mitigation: Avoid submitting sensitive prompts or private image URLs unless the user has approved that disclosure path.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/permew/skills/nano-banana-edit)
- [RunComfy](https://www.runcomfy.com)
- [RunComfy CLI Documentation](https://docs.runcomfy.com/cli/introduction?utm_source=clawhub&utm_medium=skill&utm_campaign=nano-banana-edit)
- [Nano Banana 2 Edit Endpoint](https://www.runcomfy.com/models/google/nano-banana-2/edit?utm_source=clawhub&utm_medium=skill&utm_campaign=nano-banana-edit)
- [RunComfy CLI Troubleshooting](https://docs.runcomfy.com/cli/troubleshooting?utm_source=clawhub&utm_medium=skill&utm_campaign=nano-banana-edit)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command examples and JSON input snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands use the RunComfy CLI and may download generated image files to a caller-specified output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
