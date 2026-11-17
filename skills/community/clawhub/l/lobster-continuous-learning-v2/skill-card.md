## Description:

Instinct-based learning system that observes sessions via hooks, creates atomic instincts with confidence scoring, and evolves them into skills, commands, and agents with project-scoped isolation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangxiaofei860208-source](https://clawhub.ai/user/wangxiaofei860208-source)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to capture Claude Code session patterns, convert recurring behavior into project-scoped or global instincts, and evolve those instincts into reusable skills, commands, or agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can log prompts, tool inputs, tool outputs, file paths, command output, project roots, and git remotes locally.

Mitigation: Use it only in repositories where this local logging is acceptable, review the stored observations, and periodically delete observations and archives that are no longer needed.

Risk: The background observer can create persistent instructions from observed behavior.

Mitigation: Keep the observer disabled until reviewed, inspect generated instincts and evolved artifacts before relying on them, and remove generated content that should not persist.

Risk: Imported instincts can influence future agent behavior.

Mitigation: Import instincts only from trusted files or URLs and review imported instincts before promoting them to global scope.

## Reference(s):

- [Lobster Continuous Learning V2 on ClawHub](https://clawhub.ai/wangxiaofei860208-source/skills/lobster-continuous-learning-v2)
- [ECC-Tools GitHub App](https://github.com/apps/ecc-tools)
- [The Longform Guide](https://x.com/affaanmustafa/status/2014040193557471352)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown, YAML instinct files, shell commands, and JSON configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local observations, instincts, exported instinct bundles, and evolved skill, command, or agent files under the user's Claude configuration directory.]

## Skill Version(s):

2.1.0 (source: frontmatter); ClawHub release version 1.0.0

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
