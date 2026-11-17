## Description:

Build full-stack web and mobile apps from a text description, with feature planning and Quick Start builds that return project and session context for monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[versacexcodes](https://clawhub.ai/user/versacexcodes)

### License/Terms of Use:

MIT

## Use Case:

Developers and builders use this skill to create, iterate on, deploy, and publish LaunchPulse web or Expo mobile app projects from natural-language requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill exposes production, billing, deployment, app-store publishing, domain, database, and secret-handling actions.

Mitigation: Review commands and account permissions before execution, especially for deploy, store-publish, domains, db, payments, storage, and env-files operations.

Risk: Authentication tokens and service credentials can be supplied directly or stored locally for later use.

Mitigation: Use only a trusted LaunchPulse account, avoid production credentials unless intended, and permission-harden or remove the stored auth file after use.

Risk: The API base can be overridden, which could send requests or credentials to an unintended backend.

Mitigation: Use --api-base or LAUNCHPULSE_API_BASE_URL only with a trusted local or hosted backend.

## Reference(s):

- [LaunchPulse Homepage](https://launchpulse.ai)
- [ClawHub Skill Page](https://clawhub.ai/versacexcodes/skills/mobile-app-builder-ai)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with CLI commands and JSON status responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node and LaunchPulse authentication; may start hosted background builds and return project IDs, session IDs, billing links, and live preview or publishing status URLs.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter and script report 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
