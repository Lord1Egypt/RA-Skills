## Description:

Comprehensive CLI for Krónan.is grocery store using the official Public API to search products, browse categories, manage shopping carts and lists, view orders, track purchase statistics, and manage shopping notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arnif](https://clawhub.ai/user/arnif)

### License/Terms of Use:

MIT-0

## Use Case:

External users and AI agents use this skill to operate kronan-cli for Krónan grocery workflows, including product discovery, cart management, product lists, shopping notes, order review or modification, and purchase statistics. Agents should request fresh explicit approval before any state-changing command.

### Deployment Geography for Use:

Global, subject to availability of a Krónan account and Access Token

## Known Risks and Mitigations:

Risk: The install path clones a repository and executes an installer that downloads a binary.

Mitigation: Review the upstream repository and installer before installing, and prefer a pinned release with a verified checksum when available.

Risk: The skill handles a Krónan Access Token that can read and change account shopping data.

Mitigation: Store the token only in ~/.kronan/token with user-only permissions, and avoid entering tokens directly in commands where logs or shell history may capture them.

Risk: Cart, list, note, order, and stats commands can modify real user data.

Mitigation: Require fresh explicit approval before state-changing commands and do not let an agent run --force without approval.

Risk: Identity, order, and purchase statistics output may expose personal or shopping information.

Mitigation: Treat command output as sensitive and avoid sharing it unless the user has reviewed and approved the disclosure.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/arnif/skills/kronan)
- [kronan-cli Homepage](https://github.com/arnif/kronan-cli)
- [Krónan](https://www.kronan.is)
- [Access Token Setup](https://kronan.is/adgangur/adgangslyklar)
- [Krónan Public API Swagger UI](https://api.kronan.is/api/v1/schema/swagger-ui/)
- [Krónan Public API ReDoc](https://api.kronan.is/api/v1/schema/redoc/)
- [GitHub CLI](https://cli.github.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with shell command examples and optional JSON CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GitHub CLI for installation, Bun only when building from source, and a Krónan Access Token stored at ~/.kronan/token.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact frontmatter: 0.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
