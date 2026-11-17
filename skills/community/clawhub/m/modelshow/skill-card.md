## Description:

ModelShow compares multiple AI model responses through blind judging, ranks the answers, and saves the results for later review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[schbz](https://clawhub.ai/user/schbz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, evaluators, and other agent users use this skill to compare several configured model responses to the same prompt, reduce name bias through blind judging, and keep Markdown and JSON records of the comparison.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, referenced files, model responses, and judge output may be shared with every configured model and retained in local result files.

Mitigation: Use non-sensitive inputs unless multi-model sharing and local transcript retention are acceptable; review saved Markdown and JSON outputs before redistribution.

Risk: The optional web indexer can publish saved prompts, responses, and judge output when pointed at a public directory.

Mitigation: Run the indexer only for directories intended for publication and keep private results in a non-public output directory.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/schbz/skills/modelshow)
- [Publisher profile](https://clawhub.ai/user/schbz)
- [Project homepage](https://github.com/schbz/modelshow)
- [README](README.md)
- [CHANGELOG](CHANGELOG.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration guidance]

**Output Format:** [Markdown response plus saved JSON and Markdown result files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes model rankings, scores, judge commentary, response text, run metadata, and an optional local index when explicitly configured.]

## Skill Version(s):

1.2.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
