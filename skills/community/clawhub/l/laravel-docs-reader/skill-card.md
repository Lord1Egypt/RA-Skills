## Description:

Laravel Docs Reader gives agents and developers version-aware Laravel documentation lookup, project version detection, PSR-12 code skeleton generation, and Laravel 10/11/12 difference guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[relunctance](https://clawhub.ai/user/relunctance)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill while working on Laravel projects to retrieve version-specific documentation, generate PSR-12 code skeletons, inspect config, facade, and Artisan references, and compare behavior across Laravel 10, 11, and 12.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Version detection may inspect Laravel project files and may run Artisan if that feature is implemented.

Mitigation: Use the skill in trusted project workspaces and review detected versions before applying generated guidance.

Risk: Cache and update behavior may create a local .cache directory and fetch documentation updates from GitHub or Packagist.

Mitigation: Enable network and cache writes only where those actions are acceptable, and review auto-update pull requests before merging.

Risk: The skill may suggest using laravel-package-search for third-party package discovery.

Mitigation: Treat package-search suggestions as optional and review third-party packages independently before installing them.

## Reference(s):

- [Laravel Docs Reader on ClawHub](https://clawhub.ai/relunctance/skills/laravel-docs-reader)
- [Publisher profile: relunctance](https://clawhub.ai/user/relunctance)
- [README](artifact/README.md)
- [Version Detection Logic](artifact/references/version-detection.md)
- [Laravel Version Diff (10 / 11 / 12)](artifact/references/version-diff.md)
- [PSR-12 Coding Standard Quick Reference](artifact/references/psr-12.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown responses with inline PHP, shell, JSON, and YAML snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Version-aware guidance for Laravel 10, 11, and 12; may include PSR-12 code skeletons, documentation summaries, version notes, and caveats.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact specification)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
