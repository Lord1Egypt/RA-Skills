## Description:

Runs command-line tools through Nix, using local commands when available and fetching matching nixpkgs packages when needed, with support for package selection, search, updates, and multi-package shells.

This skill is ready for commercial/non-commercial use.

## Publisher:

[msdimos](https://clawhub.ai/user/msdimos)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to execute missing or version-sensitive CLI tools through Nix without manually installing packages, including workflows that require multiple command-line packages in one environment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run arbitrary commands and may download and execute packages from a moving nixpkgs source.

Mitigation: Review before use in sensitive workspaces; prefer a fixed, audited nixpkgs revision and narrower activation rules before granting access to private files, credentials, or write permissions.

Risk: The search option has a command-execution injection risk.

Mitigation: Avoid passing untrusted values to --search or --limit and review the script before enabling search in automated workflows.

Risk: The skill over-directs agents to use it for all CLI work.

Mitigation: Limit activation to tasks that need Nix-based command discovery, version control, or multi-package environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/msdimos/skills/nix-run)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke local commands directly or run tools from nixpkgs-unstable through Nix.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
