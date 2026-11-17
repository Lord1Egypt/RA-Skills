## Description:

Node.js cron job scheduling with the `cron` npm package.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlark](https://clawhub.ai/user/openlark)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to schedule recurring Node.js or TypeScript tasks, validate cron expressions, configure timed callbacks, and avoid common second-precision cron pitfalls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled callback code runs with the permissions of the Node.js process.

Mitigation: Review callback behavior before deployment and run jobs with the least privileges needed for the scheduled task.

Risk: Unreviewed dependency versions or timezone mistakes can cause unreliable scheduling behavior.

Mitigation: Use an exact reviewed `cron` package version with a lockfile and confirm the intended IANA timezone.

## Reference(s):

- [Node Cron API Reference](references/api_reference.md)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, configuration]

**Output Format:** [Markdown with TypeScript examples and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
