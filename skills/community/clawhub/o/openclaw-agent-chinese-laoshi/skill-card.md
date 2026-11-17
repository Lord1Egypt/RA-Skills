## Description:

Use when studying or normalizing Chinese lesson transcript/subtitle inputs with bundled public lesson data, learner docs, local export bundles, and pilot-first prepublish leak gates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zack-dev-cm](https://clawhub.ai/user/zack-dev-cm)

### License/Terms of Use:

MIT-0

## Use Case:

Learners, tutors, and developers use this skill to study or normalize Chinese lesson transcript/subtitle inputs, create grounded Chinese lesson materials, and check public release bundles before publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill advertises bundled course-data and system-prompts assets that are not present in the release artifact.

Mitigation: Ask the publisher to include the missing assets or revise the skill so it no longer claims they are bundled before relying on those workflows.

Risk: Repository commands or Drive sync could run with unintended local access if treated as implicit capabilities.

Mitigation: Allow commands or Drive sync only after the exact command is shown, the source repository documents it, and the user intentionally provides any required local mount path.

Risk: Publication workflows could expose private paths, secret-shaped strings, debug endpoints, or known file IDs.

Mitigation: Run the documented public release gate and block publication when leak indicators or bundle drift are detected.

Risk: Chinese lesson outputs could become misleading if missing Hanzi, pinyin, translations, or weak source material are filled in by guesswork.

Mitigation: Keep uncertainty visible, mark missing fields, reject unsupported content, and build learner-facing materials only after grounded extraction exists.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zack-dev-cm/skills/openclaw-agent-chinese-laoshi)
- [Publisher profile](https://clawhub.ai/user/zack-dev-cm)
- [ClawDIS homepage](https://github.com/zack-dev-cm/openclaw-agent-chinese-laoshi)
- [Pipeline Reference](references/pipeline.md)
- [Release Gates](references/release-gates.md)
- [ChatGPT Connector Guidance](references/chatgpt-connector-guidance.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with optional JSON lesson assets, local export guidance, configuration notes, and proposed shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands must be shown for explicit user confirmation before execution; outputs should stay grounded in bundled public lesson data or user-provided transcript/subtitle text.]

## Skill Version(s):

1.0.15 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
