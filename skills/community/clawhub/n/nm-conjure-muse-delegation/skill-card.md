## Description:

Delegates repository coding work to Meta's Muse Code CLI (muse).

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill when their delegation workflow selects Muse for repository-scale coding tasks, including unattended runs that need broad repository context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented installer runs a remote script through a shell, and the scanner could not determine the installer's contents or effects.

Mitigation: Read Meta's Muse Code documentation and inspect the installer source before running it; use the guided setup when its source review is available.

Risk: Repository content may be sent to an external model service during delegation.

Mitigation: Review prompts and included files, and exclude credentials or other sensitive repository content unless its transmission is approved.

Risk: The security scan was partial and could not resolve several local references.

Mitigation: Review the full skill and its referenced local files before using it in a repository.

## Reference(s):

- [Muse Code documentation](https://dev.meta.ai/docs/muse-code)
- [Muse Code configuration](https://dev.meta.ai/docs/muse-code/configuration)
- [Muse models](https://dev.meta.ai/docs/models)
- [Project homepage (server metadata)](https://github.com/athola/claude-night-market/tree/master/plugins/conjure)
- [ClawHub release page](https://clawhub.ai/athola/skills/nm-conjure-muse-delegation)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance, Code]

**Output Format:** [Markdown delegation results with shell command and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Delegated results are saved as a timestamped Markdown file.]

## Skill Version(s):

1.10.4 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
