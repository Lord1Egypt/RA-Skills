## Description: <br>
Luban is a skill-polishing workshop that helps developers audit, benchmark, improve, validate, and publish agent skills as understandable, installable, shareable public assets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[donttal](https://clawhub.ai/user/donttal) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill authors use this skill to turn an existing agent skill, repository, ClawHub page, or SKILL.md draft into a clearer, more testable, and more publishable public skill asset. It guides premise review, ecosystem benchmarking, structured scoring, bounded edits, validation, and a final skill-polishing report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow may inspect private repositories or skill materials that contain sensitive content. <br>
Mitigation: Use offline-only review when needed, avoid exposing private inputs during research, and check generated examples for secrets, tokens, cookies, private paths, or personal data before publication. <br>
Risk: The skill can recommend network research, edits, shell commands, commits, pushes, releases, or deployments as part of skill polishing. <br>
Mitigation: Confirm before network research and require explicit user approval before commits, pushes, releases, deployments, or other irreversible actions. <br>
Risk: Suggested rewrites could introduce inaccurate claims or misleading guidance into a public skill. <br>
Mitigation: Review proposed content against the source skill and preserve only changes that pass the workflow's validation gate. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/donttal/luban) <br>
- [AI News Radar polishing case study](artifact/examples/ai-news-radar-case.md) <br>
- [LearnPrompt ai-news-radar repository](https://github.com/LearnPrompt/ai-news-radar) <br>
- [ai-news-radar v0.7.0 release](https://github.com/LearnPrompt/ai-news-radar/releases/tag/v0.7.0) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown report with replacement snippets, tables, command examples, and a result-card section] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include proposed file changes, validation plans, benchmark findings, and publication guidance.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
