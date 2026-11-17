## Description:

Guides Go developers in using the unofficial go-fireworks client to call Fireworks AI control-plane and inference APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to write Go code that calls Fireworks AI for inference or control-plane tasks, including managing models, deployments, datasets, and jobs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API credentials or private data could be sent to an unintended service if the base URL is wrong.

Mitigation: Use a narrowly scoped API key and verify the base URL before sending credentials or private data.

Risk: The unofficial Go dependency may introduce unreviewed behavior.

Mitigation: Review and pin the dependency before deployment.

Risk: Deployment, fine-tuning, batch-job, or deletion calls can incur costs or remove resources.

Mitigation: Run these calls only when the user requested the action and only on resources the task owns.

## Reference(s):

- [Setup and reference](artifact/references/setup.md)
- [Go package documentation](https://pkg.go.dev/github.com/psyb0t/go-fireworks)
- [Project homepage](https://github.com/psyb0t/go-fireworks)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with Go code examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

0.2.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
