## Description:

Meitu Skills is an agent skill library for Meitu OpenAPI that lets agents generate and edit posters, stickers, videos, product images, portraits, and other media through Meitu CLI workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[meituskills](https://clawhub.ai/user/meituskills)

### License/Terms of Use:

MIT

## Use Case:

External users, developers, and agent operators use this skill pack to route media generation and editing requests to Meitu OpenAPI via the local meitu CLI, including scene workflows for posters, cutouts, product visuals, video generation, and personalized visual assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package requires access to Meitu OpenAPI credentials.

Mitigation: Prefer environment-injected credentials, restrict any credentials file permissions, and do not commit credentials to version control.

Risk: Media, prompts, and selected local profile or memory context may be processed by Meitu OpenAPI.

Mitigation: Review or disable local memory and profile use when shared visual workspace contents are sensitive.

Risk: The package uses persistent shared visual state and can write generated outputs or workflow memory to configured local paths.

Mitigation: Review declared permissions and local workspace contents before production use, especially in shared environments.

Risk: The security evidence recommends using a pinned, reviewed Meitu CLI version.

Mitigation: Use a reviewed CLI runtime version and keep runtime repair or upgrades as an explicit operator action.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/meituskills/skills/meitu-skills)
- [Publisher profile](https://clawhub.ai/user/meituskills)
- [README](README.md)
- [Security model](SECURITY.md)
- [Routing guide](references/routing-guide.md)
- [Meitu tools command catalog](meitu-tools/references/tools.yaml)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and structured JSON CLI results, including media URLs when generation succeeds.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Meitu OpenAPI credentials and a compatible meitu CLI runtime; some workflows write outputs or visual memory to configured local paths.]

## Skill Version(s):

2.0.14 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
