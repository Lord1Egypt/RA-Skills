## Description: <br>
Pull request size analyzer and split planner that measures GitHub or local git diffs, classifies PR size, detects logical chunks, and proposes a split plan with branch names, dependency order, and a ready-to-post PR comment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PHY041](https://clawhub.ai/user/PHY041) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to evaluate oversized pull requests and turn broad diffs into smaller, reviewable PRs. It is intended for GitHub PRs, local branches, or raw diff files where a concise split plan and reviewer-facing checklist are useful. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can cause the agent to read local or GitHub PR diffs, which may expose source changes or repository context to the agent session. <br>
Mitigation: Invoke it explicitly with /pr-size only in repositories where this access is acceptable, and verify which GitHub account the gh CLI is using. <br>
Risk: Generated comments, branch plans, or PR creation commands may be incorrect for the repository's workflow. <br>
Mitigation: Review all generated comments and shell commands before allowing the agent to post to GitHub or modify branches. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/PHY041/phy-pr-size-splitter) <br>
- [Publisher homepage](https://canlah.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report with inline tables, checklists, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include PR size classifications, logical chunk groupings, proposed branch names, dependency order, and a draft GitHub PR comment.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
