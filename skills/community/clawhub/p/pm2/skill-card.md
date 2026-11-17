## Description:

Manage Node.js applications with PM2 for production deployment, monitoring, auto-restart, boot auto-start, log review, and multi-process control.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asteinberger](https://clawhub.ai/user/asteinberger)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to operate Node.js services with PM2, including startup, monitoring, logging, restarts, production builds, ecosystem configuration, and cleanup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Boot-startup commands can alter host service startup behavior and may require elevated privileges.

Mitigation: Review the exact pm2 startup command before using sudo and avoid elevated shells unless required.

Risk: Cleanup and save commands can affect running services or persist an unintended process list.

Mitigation: Verify the PM2 process list before running pm2 save, pm2 delete all, pm2 kill, or pm2 unstartup on a production host.

Risk: Global npm installation can install unexpected packages if the registry or package source is not what the user expects.

Mitigation: Install PM2 only from the expected npm registry.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with bash and JavaScript code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes operational commands that can affect running PM2 processes and boot-startup configuration.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
