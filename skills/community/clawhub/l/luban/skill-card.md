## Description:

Luban helps agents audit, benchmark, refine, validate, and package existing agent skills into public skill assets with a structured polishing report, replacement-ready edits, and a shareable result card.

This skill is ready for commercial/non-commercial use.

## Publisher:

[donttal](https://clawhub.ai/user/donttal)

### License/Terms of Use:

MIT-0

## Use Case:

Skill authors, maintainers, and agent developers use Luban to improve existing skills before publication by checking positioning, comparing similar skills, scoring structure and live behavior, proposing bounded edits, and documenting validation evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can lead an agent toward remote repository actions such as push, pull request, merge, tag, release, or deployment.

Mitigation: Require explicit approval for each remote action, naming the action, remote, branch, and release target before execution.

Risk: The workflow involves inspecting skill repositories and searching the web for comparison data, which may expose sensitive project context if used on private material.

Mitigation: Use it only on repositories approved for agent inspection and external comparison, and remove secrets, private account data, and unreleased confidential details first.

Risk: Generated polishing reports and replacement snippets may introduce inaccurate positioning or unsafe operational guidance if applied without review.

Mitigation: Review proposed edits against the original baseline and run the documented validation checks before keeping or publishing changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/donttal/skills/luban)
- [AI News Radar case study](examples/ai-news-radar-case.md)
- [LearnPrompt/ai-news-radar](https://github.com/LearnPrompt/ai-news-radar)
- [AI News Radar v0.7.0 release](https://github.com/LearnPrompt/ai-news-radar/releases/tag/v0.7.0)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown report with replacement-ready snippets, validation notes, and a shareable result card]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include concrete file-change recommendations, test prompts, benchmark references, and release-readiness guidance.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
