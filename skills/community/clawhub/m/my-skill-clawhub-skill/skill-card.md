## Description:

Standardizes ClawHub publishing with required versions and changelogs, and supports searching and installing ClawHub skills with optional version selection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[canonxu](https://clawhub.ai/user/canonxu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill publishers use this skill to standardize ClawHub publish and install workflows, including required version and changelog inputs for releases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing the latest remote skill by slug can select an unexpected version or publisher if the slug is not checked carefully.

Mitigation: Specify an exact version when installing and confirm the slug and publisher profile in ClawHub before use.

Risk: The helper searches before install but does not independently verify signatures or digests.

Mitigation: Treat search results as discovery only and rely on ClawHub publisher, version, and security evidence review before deployment.

## Reference(s):


## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks and shell command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces ClawHub publish, search, and install commands; install supports an optional explicit version.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
