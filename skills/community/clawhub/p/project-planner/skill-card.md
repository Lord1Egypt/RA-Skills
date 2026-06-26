## Description: <br>
Triage ideas, problems, and feature requests into the right format: proposal doc, feature issue, or bug report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chriscox](https://clawhub.ai/user/chriscox) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and project maintainers use this skill to turn user ideas, feature requests, and bug reports into proposal documents, feature issues, or bug reports that follow the target repository's conventions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can direct an agent to create GitHub issues and push repository changes without an explicit approval step. <br>
Mitigation: Before issue creation, commits, or pushes, require the agent to show the target repository, proposed file changes, issue contents, labels, branch name, and exact git/gh commands for explicit approval. <br>


## Reference(s): <br>
- [Project Planner Skill Page](https://clawhub.ai/chriscox/project-planner) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [Fallback Proposal Template](artifact/templates/proposals/TEMPLATE.md) <br>
- [Project Planner Configuration Template](artifact/project-planner.yml) <br>
- [Bug Issue Template](artifact/issue-templates/bug.yml) <br>
- [Feature Issue Template](artifact/issue-templates/feature.yml) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, configuration, shell commands, guidance] <br>
**Output Format:** [Markdown documents, GitHub issue bodies, YAML-backed issue/configuration templates, and git/gh command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create proposal files, GitHub issues, branches, commits, and pushes when the agent is allowed to run git and gh commands.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
