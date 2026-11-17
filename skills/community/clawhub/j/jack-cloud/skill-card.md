## Description:

Deploy web services to the cloud with Jack, including project creation, deployment, databases, logs, and Jack Cloud services.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hellno](https://clawhub.ai/user/hellno)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to create and deploy Jack Cloud projects, manage Cloudflare Worker services, inspect logs, configure secrets, and operate attached services such as D1, R2, Vectorize, cron schedules, and custom domains.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Jack CLI stores an authentication token locally after browser OAuth login.

Mitigation: Install and use the skill only in environments where local Jack credentials can be stored under the user's configuration directory.

Risk: Deployment uploads project source code to Jack Cloud and creates or changes cloud resources.

Mitigation: Review project contents before deployment and use non-production projects when testing service, database, cron, secret, storage, or domain changes.

Risk: Database examples include write operations that can alter data.

Mitigation: Run write SQL examples against test data first and require explicit write intent for database changes.

Risk: The skill depends on installing the Jack CLI from npm.

Mitigation: Verify or pin the npm package before installation when supply-chain controls are required.

## Reference(s):

- [Jack Cloud services guide](reference/services-guide.md)
- [Jack documentation](https://docs.getjack.org)
- [Jack homepage](https://getjack.org)
- [Jack CLI npm package](https://www.npmjs.com/package/@getjack/jack)
- [ClawHub metadata homepage](https://github.com/getjack-org/skills)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command, code, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use Jack MCP tools when available; otherwise provides Jack CLI commands and configuration steps.]

## Skill Version(s):

0.3.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
