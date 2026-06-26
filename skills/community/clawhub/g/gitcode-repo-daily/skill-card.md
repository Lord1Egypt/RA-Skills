## Description: <br>
Generate daily operations reports for GitCode repositories with key metrics, AI summaries, and Markdown output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[autoxj](https://clawhub.ai/user/autoxj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and repository maintainers use this skill to turn GitCode repository activity into daily operational reports. It collects repository metrics, supports AI-written summaries from report data, and renders a structured Markdown report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a GitCode token to call GitCode APIs. <br>
Mitigation: Use a least-privilege token and avoid installing the skill where that token should not be exposed. <br>
Risk: Repository metrics, PR titles or bodies used for summaries, and generated summaries may be retained in local skill files. <br>
Mitigation: Review saved default repositories on shared machines and delete temp_dir or resources/report.db when local report history should not be retained. <br>
Risk: Generated reports depend on GitCode API availability, token validity, and configured repositories. <br>
Mitigation: Check script error output for missing tokens, empty repository lists, API timeouts, and per-repository fetch errors before relying on a report. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/autoxj/gitcode-repo-daily) <br>
- [Publisher profile](https://clawhub.ai/user/autoxj) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Design and usage documentation](artifact/README.md) <br>
- [Daily report template](artifact/resources/daily_report.md) <br>
- [GitCode API base](https://api.gitcode.com/api/v5) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, JSON intermediate data, and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a GitCode token and repository list; generated report history and summaries may be stored locally by the skill.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
