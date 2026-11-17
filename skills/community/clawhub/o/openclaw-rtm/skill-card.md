## Description:

Remember The Milk skill for OpenClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kissyjpf](https://clawhub.ai/user/kissyjpf)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to manage Remember The Milk tasks from an agent or command-line workflow, including listing, adding, annotating, scheduling, completing, and deleting tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores and handles Remember The Milk API credentials and authorization tokens.

Mitigation: Install only in trusted environments, prefer environment variables or a credential manager, restrict access to local ~/.rtm-*.json files, and rotate credentials if secrets may have been logged.

Risk: The skill can modify, complete, or delete remote Remember The Milk tasks.

Mitigation: Review agent-proposed task changes before execution, especially delete and complete operations.

## Reference(s):

- [Remember The Milk](https://www.rememberthemilk.com/)
- [Remember The Milk API Keys](https://www.rememberthemilk.com/services/api/keys.rtm)
- [Remember The Milk REST API Endpoint](https://api.rememberthemilk.com/services/rest/)
- [Remember The Milk Auth Endpoint](https://www.rememberthemilk.com/services/auth/)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text and Markdown-style command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include task IDs, task status, due dates, priorities, tags, notes, authorization URLs, and error messages.]

## Skill Version(s):

1.0.9 (source: server release metadata; artifact package.json and plugin metadata report 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
