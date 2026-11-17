## Description:

Interact with the essesseff DevOps platform by calling the essesseff Public API for templates, organizations, apps, deployments, images, environments, retention policies, and packages, and by guiding app creation and Argo CD setup with the essesseff onboarding utility.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adamdurst](https://clawhub.ai/user/adamdurst)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and DevOps engineers use this skill to manage essesseff applications, deployment lifecycle actions, Argo CD environment setup, GitHub repository onboarding, package cleanup, and retention policy configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide production deployment actions, repository creation, package deletion, retention changes, and other DevOps operations.

Mitigation: Require explicit operator confirmation for production deployment, repository creation, package deletion, and retention policy changes.

Risk: The skill handles powerful essesseff, GitHub, Kubernetes, and Argo CD credentials.

Mitigation: Use short-lived, least-privilege tokens and keep secrets such as .env files and notifications-secret.yaml out of Git working trees.

Risk: Kubernetes and Argo CD setup can affect the wrong environment if local context is misconfigured.

Mitigation: Verify the intended cluster, namespace, and Argo CD target before running kubectl or onboarding commands.

Risk: The onboarding utility is external automation that can create and modify repositories and deployment configuration.

Mitigation: Pin and inspect the onboarding utility before execution, and install only when the publisher is trusted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/adamdurst/skills/openclaw-essesseff)
- [essesseff onboarding utility](https://github.com/essesseff/essesseff-onboarding-utility)
- [essesseff Public API](https://www.essesseff.com/docs/api)
- [Apps API](references/api-apps.md)
- [Environments API](references/api-environments.md)
- [Images API](references/api-images.md)
- [Organizations API](references/api-organizations.md)
- [Packages API](references/api-packages.md)
- [Retention Policies API](references/api-retention-policies.md)
- [Templates API](references/api-templates.md)
- [Onboarding Utility](references/onboarding-utility.md)
- [Prerequisites](references/prerequisites.md)
- [Non-Subscriber Mode Guide](references/non-subscriber-mode.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, curl examples, JSON payloads, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API request examples, environment variable setup, onboarding command sequences, and operational cautions.]

## Skill Version(s):

1.0.2 (source: server release metadata; skill frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
