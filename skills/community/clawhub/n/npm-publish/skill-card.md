## Description:

Publish an NPM package to the registry, handling authentication via browser-based login with 2FA/security key support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clarezoe](https://clawhub.ai/user/clarezoe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release engineers use this skill to publish npm packages after validating build and test readiness, authenticating to npm, handling 2FA or security-key login, and verifying the published version.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead an agent to access raw npm credentials and automate login.

Mitigation: Prefer native npm login or a trusted password manager flow, avoid storing passwords in generated scripts, and keep any temporary login script out of source control.

Risk: The skill can create a persistent write-capable npm token on disk.

Mitigation: Use scoped or temporary publish tokens when possible, preserve existing npm configuration, and revoke tokens after publishing.

## Reference(s):

- [Npm Publish ClawHub Skill Page](https://clawhub.ai/clarezoe/skills/npm-publish)
- [npm Login](https://www.npmjs.com/login)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration]

**Output Format:** [Markdown guidance with bash and JavaScript code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes credential-handling guidance and commands that can modify npm authentication configuration.]

## Skill Version(s):

1.0.2 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
