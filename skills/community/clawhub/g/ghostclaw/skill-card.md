## Description:

Architectural code review and refactoring assistant that perceives code vibes and system-level flow issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ev3lynx727](https://clawhub.ai/user/ev3lynx727)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use Ghostclaw to review repository architecture, score codebase health, identify coupling and cohesion problems, and plan refactors aligned with stack-specific conventions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can write reports and cache analysis data in repositories or local directories.

Mitigation: Use no-write or dry-run modes where available, run in a constrained workspace, and review generated files before publishing or committing them.

Risk: Repository watcher and PR modes can pull repositories and create GitHub pull requests when configured.

Mitigation: Enable PR creation only with limited-scope credentials, review proposed PR contents before merge, and avoid running watcher automation against untrusted repositories.

Risk: Optional local analyzers and update paths execute external commands from the runtime environment.

Mitigation: Use trusted PATH entries, install dependencies from trusted sources, avoid self-update behavior, and run the skill with limited permissions.

## Reference(s):

- [Ghostclaw Stack Patterns](ghostclaw/references/stack-patterns.md)
- [Ghostclaw Stack Patterns YAML](ghostclaw/references/stack-patterns.yaml)
- [ClawHub Skill Page](https://clawhub.ai/ev3lynx727/skills/ghostclaw)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, terminal text, and optional JSON analysis data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write timestamped architecture reports, cache analysis results, and create GitHub pull requests when explicitly configured.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
