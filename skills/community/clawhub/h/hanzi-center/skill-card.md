## Description:

雄韬汉字视觉重心分析引擎 uses a pixel-level model based on stroke mass, distance, and slant to calculate and explain the visual center of Chinese characters across multiple font styles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xtoyun](https://clawhub.ai/user/xtoyun)

### License/Terms of Use:

MIT-0

## Use Case:

External users, calligraphy learners, typography reviewers, and developers use this skill to analyze where a Chinese character's visual center falls, compare characters or fonts, and explain perceived imbalance in writing or type design.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation uses npm with a native canvas dependency resolved from the npmmirror registry.

Mitigation: Install in an isolated environment and review the lockfile and registry source before use.

Risk: Default execution writes a PNG visualization file into the working directory.

Mitigation: Use --no-png when file creation is not desired.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xtoyun/skills/hanzi-center)
- [Homepage and online demo](http://shufa.xtocn.com/汉字视觉重心.html)

## Skill Output:

**Output Type(s):** [Text, JSON, Files, Shell commands, Guidance]

**Output Format:** [Markdown guidance with shell commands; CLI output as text or JSON plus an optional PNG visualization file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally with Node.js and node-canvas; PNG output is enabled by default and can be disabled with --no-png.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
