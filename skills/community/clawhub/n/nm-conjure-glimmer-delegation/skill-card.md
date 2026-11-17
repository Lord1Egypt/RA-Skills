## Description:

Delegates to a local Muse Glimmer via ollama

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to delegate a task to a locally hosted Muse Glimmer model through Ollama when the prompt must stay on the machine or other providers are exhausted.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation pipes a downloaded script directly into a shell, creating a significant supply-chain risk.

Mitigation: Inspect or independently verify the installer first, or use a trusted package manager; understand and approve the system changes before installing.

Risk: The security scan was partial because two local path-like references could not be resolved.

Mitigation: Resolve and review those references before relying on behavior the scan did not cover.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/athola/skills/nm-conjure-glimmer-delegation)
- [Project homepage listed in skill metadata](https://github.com/athola/claude-night-market/tree/master/plugins/conjure)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions]

**Output Format:** [Markdown guidance with shell command examples and delegated text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Delegated output is saved as a timestamped Markdown file.]

## Skill Version(s):

1.10.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
