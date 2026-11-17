## Description:

Use when working with Halo CLI login, bearer token or basic auth, profile setup, profile switching, current profile inspection, or fixing missing keyring credentials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ruibaby](https://clawhub.ai/user/ruibaby)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure Halo CLI authentication, inspect and switch auth profiles, and diagnose missing or broken keyring credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Login examples can place real passwords or tokens on the command line if copied literally.

Mitigation: Prefer secure login methods such as an interactive prompt, stdin, or another non-history mechanism if supported; avoid shared systems and logs, disable command tracing, and rotate any exposed credential.

Risk: Profile deletion is destructive.

Mitigation: Review the target profile before deletion and use --force only when deletion is intentional in non-interactive workflows.

## Reference(s):

- [Halo Cli Auth on ClawHub](https://clawhub.ai/ruibaby/skills/halo-cli-auth)
- [Publisher profile: ruibaby](https://clawhub.ai/user/ruibaby)
- [Shared Halo CLI skill reference](../halo-cli-shared)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Halo CLI commands that handle credentials and profile configuration.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
