## Description:

Maintain CHANGELOG.md files in Keep a Changelog 1.1.0 format, including creating changelogs, recording notable changes, cutting releases, and auditing existing changelogs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nanookai](https://clawhub.ai/user/nanookai)

### License/Terms of Use:

MIT

## Use Case:

Developers and maintainers use this skill to keep project release notes readable and consistent with Keep a Changelog 1.1.0 and Semantic Versioning conventions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may inspect git tags and commit history to draft release notes.

Mitigation: Review the generated changelog entries before committing or releasing.

Risk: The skill may edit CHANGELOG.md when asked to manage release notes or changelog content.

Mitigation: Review the file diff before publishing the release.

## Reference(s):

- [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/)
- [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html)
- [Changelog template](references/template.md)
- [NanookAI skills marketplace](https://github.com/NanookAI/skills)
- [ClawHub skill page](https://clawhub.ai/nanookai/skills/keepachangelog)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with changelog entries, audit findings, and inline shell commands when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May edit CHANGELOG.md when asked to create, update, audit, or cut a release.]

## Skill Version(s):

1.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
