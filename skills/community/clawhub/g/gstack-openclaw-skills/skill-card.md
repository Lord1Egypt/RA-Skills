## Description: <br>
Gstack Openclaw Skills adapts the gstack development workflow into OpenClaw and WorkBuddy skills covering product ideation, code review, QA, documentation, and release workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dsg12te-del](https://clawhub.ai/user/dsg12te-del) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill bundle to route agent workflows for product ideation, planning review, code review, QA, documentation, and release preparation. It is intended for OpenClaw or WorkBuddy agent sessions where users want structured development guidance and automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill bundle can guide an agent to modify repositories from broad prompts. <br>
Mitigation: Use explicit commands, prefer dry-run or report-only modes, and inspect diffs before applying fixes. <br>
Risk: Release workflows may lead to commits, pushes, pull requests, or production deployment without consistent approval boundaries. <br>
Mitigation: Require separate confirmation before commits, pushes, pull request creation, or production deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dsg12te-del/gstack-openclaw-skills) <br>
- [Publisher profile](https://clawhub.ai/user/dsg12te-del) <br>
- [Original gstack project referenced by the artifact](https://github.com/garrytan/gstack) <br>
- [Artifact README](README.md) <br>
- [Artifact installation guide](INSTALL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command examples, code review notes, QA reports, release notes, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose repository edits, git operations, PR creation, or deployment steps depending on the selected workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, target metadata, top-level SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
