## Description:

Guides Git fetch, push, reset, and repository recovery in WorkBuddy sandboxes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oracis](https://clawhub.ai/user/oracis)

### License/Terms of Use:

MIT-0

## Use Case:

Developers using WorkBuddy sandboxes can diagnose Git failures and recover repositories while preserving local work and checking remote state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment flags credential exposure and publishing-data concerns in the skill's guidance.

Mitigation: Review authentication steps before use, keep tokens out of terminal output and logs, and remove any token-bearing remote URL immediately after use.

Risk: Authorization workarounds and repository repair steps could conceal differences between local and remote content.

Mitigation: Confirm the repository and authorization context, inspect local and remote diffs before reset or restore, and verify the resulting remote commit.

Risk: The security scan had partial coverage, including unresolved references and a bundled image outside analyzer scope.

Mitigation: Review the complete skill content and referenced material before installation, consistent with the security guidance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/oracis/skills/git-sandbox-safe-ops)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration]

**Output Format:** [Markdown with shell and Python code blocks and tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes diagnostic steps and repository recovery commands that may change Git state.]

## Skill Version(s):

1.0.2 (source: server-resolved release and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
