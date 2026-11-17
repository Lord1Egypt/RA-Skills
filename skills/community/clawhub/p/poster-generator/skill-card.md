## Description:

Poster Generator helps agents create professional marketing posters, social media graphics, event flyers, and promotional materials from templates, custom text, colors, and output options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhenstaff](https://clawhub.ai/user/zhenstaff)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing teams, designers, content creators, and agents use this skill to generate branded posters, social media graphics, event flyers, and batch visual assets from templates and structured prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents or users to install and run an unpinned external npm or GitHub package that was not included for audit.

Mitigation: Prefer a pinned npm version or reviewed commit, avoid npx and global installs when possible, and run in a low-privilege workspace.

Risk: System-level setup commands such as sudo font installation can change the host environment.

Mitigation: Use local font paths, containers, or other scoped environments when possible; use sudo only after reviewing the exact system change.

Risk: Generated poster output paths can overwrite existing files when reused.

Mitigation: Use fresh output directories or unique filenames and review generated assets before publishing or deploying them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zhenstaff/skills/poster-generator)
- [GitHub Repository](https://github.com/ZhenRobotics/openclaw-poster-generator)
- [npm Package](https://www.npmjs.com/package/openclaw-poster-generator)
- [Documentation](https://github.com/ZhenRobotics/openclaw-poster-generator/wiki)
- [Issue Tracker](https://github.com/ZhenRobotics/openclaw-poster-generator/issues)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration, Files]

**Output Format:** [Markdown guidance with shell, JSON, JavaScript, and TypeScript examples; generated poster files may be PNG, JPG, PDF, or SVG.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports template selection, custom text, colors, image inputs, dimensions, quality, DPI, and batch output paths.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
