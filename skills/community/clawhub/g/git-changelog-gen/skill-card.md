## Description: <br>
Generate changelogs from git commits. Supports markdown, plain text, and JSON output with date ranges and tag-based filtering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rogue-agent1](https://clawhub.ai/user/rogue-agent1) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to generate readable changelogs from local Git commit history for release notes, project summaries, or programmatic changelog processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Changelog output can expose commit metadata such as hashes, subjects, authors, and dates. <br>
Mitigation: Run it only on repositories whose commit history is appropriate to print or share, and review generated output before publishing. <br>
Risk: The script runs local Git commands inside a user-supplied repository path. <br>
Mitigation: Use trusted local repository paths and review command arguments before execution. <br>
Risk: Grouped output relies on Bash 4+, while some macOS environments ship an older Bash. <br>
Mitigation: Use a Bash 4+ interpreter for grouped output or run without the grouping option. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rogue-agent1/git-changelog-gen) <br>
- [Publisher profile](https://clawhub.ai/user/rogue-agent1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands] <br>
**Output Format:** [Markdown, plain text, or JSON changelog entries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads local Git history, excludes merge commits, supports date ranges and tag-based filtering, and can group conventional commit types when Bash 4+ is available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact/skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
