## Description:

PAO System is a Personal AI Operator framework for skill management, protocol handling, WebSocket communication, cross-device memory sync, and multi-agent task distribution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hansondong](https://clawhub.ai/user/hansondong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical operators use PAO System to coordinate AI assistants across devices, synchronize local memory, manage skills, and distribute work to multiple agents over local networking protocols.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Default networking and storage may expose cross-device coordination data without authentication or clear safeguards.

Mitigation: Review the networking model before installation, bind listener and WebSocket services to localhost or a trusted VPN, and add authentication and TLS before broader use.

Risk: File handling and callbacks can broaden access beyond the intended workspace or destination.

Mitigation: Restrict file handlers to an explicit workspace and validate outbound URLs and callbacks against an allowlist.

Risk: Sensitive memories may be stored before encryption-at-rest is implemented.

Mitigation: Avoid storing sensitive memory data until encryption-at-rest and storage controls have been implemented and reviewed.

## Reference(s):

- [PAO System ClawHub page](https://clawhub.ai/hansondong/skills/pao-system)
- [README](README.md)
- [User Guide](docs/user_guide.md)
- [API Reference](docs/api_reference.md)
- [Task Deployment Guide](task_deploy_guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell, Python, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local networking, worker, and deployment guidance for PAO services.]

## Skill Version(s):

1.1.2 (source: server release evidence, SKILL.md frontmatter, pyproject.toml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
