## Description:

A Chinese novel quality audit skill that checks logic flaws, character inconsistencies, pacing issues, and narrative bugs, then produces graded reports and repair suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bbroot](https://clawhub.ai/user/bbroot)

### License/Terms of Use:

MIT-0

## Use Case:

Writers, editors, and agent users use this skill to audit Chinese novel chapters or full manuscripts for logic, character, pacing, and foreshadowing issues and to receive prioritized repair guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Analyzer scripts may load local .env values even though the skill is primarily for manuscript analysis.

Mitigation: Run the skill in an isolated virtual environment and avoid executing analyzers from directories that contain sensitive .env files.

Risk: Analyzer commands can write report, log, or image files into the working directory or a specified output path.

Mitigation: Run commands in a scratch workspace, choose explicit output paths, and review generated files before sharing them.

Risk: The optional novel-master v2 workflow can read local novel state files and invokes scripts from a separate skill.

Mitigation: Use the novel-master commands only when that separate skill is trusted and the referenced local novel state is intended for analysis.

Risk: The dependency and file-output behavior is under-disclosed in the release evidence.

Mitigation: Review the package before installing, pin and verify dependencies, and install only the dependencies required for the chosen analyzer path.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bbroot/skills/novel-bug-checker-v2)
- [Bug patterns reference](references/bug-patterns.md)
- [Character consistency reference](references/character-consistency.md)
- [Narrative theory reference](references/narrative-theory.md)
- [Repair strategies reference](references/repair-strategies.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown reports with prioritized findings, repair options, and optional command-line analyzer output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local report files when analyzer scripts are run.]

## Skill Version(s):

2.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
