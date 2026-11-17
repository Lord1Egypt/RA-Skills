## Description:

Agent guide for running and monitoring GPU experiments with the jl CLI on JarvisLabs.ai.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gladiator07](https://clawhub.ai/user/gladiator07)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to operate JarvisLabs GPU and CPU instances, run managed training jobs, monitor logs, transfer files, and clean up billable cloud resources through the jl CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs an unpinned JarvisLabs CLI package and relies on authenticated access to the user's JarvisLabs account.

Mitigation: Use only trusted CLI package sources, review the installed package before use, and inject JL_API_KEY through a protected secret manager or environment mechanism.

Risk: The skill can guide an agent to create, pause, resume, or destroy billable cloud instances, including destructive deletion.

Mitigation: Require explicit user approval before creating billable resources or running jl destroy, and prefer pause when preserving data matters.

Risk: Credentials may be exposed through logs, shell history, or transcripts during authentication and troubleshooting.

Mitigation: Avoid pasting secrets into visible commands, redact logs before sharing them, and rotate any token that appears in logs, history, or transcripts.

## Reference(s):

- [JarvisLabs CLI documentation](https://docs.jarvislabs.ai/cli/)
- [ClawHub skill page](https://clawhub.ai/gladiator07/skills/jarvislabs-gpu)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes operational guidance for authentication, instance lifecycle, managed runs, log monitoring, file transfer, and cleanup.]

## Skill Version(s):

1.0.2 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
