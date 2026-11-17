## Description: <br>
Analyzes a single GitHub Pull Request to estimate merge likelihood and recommend practical improvements based on technical, review, process, and PR hygiene signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individual developers and open source contributors use this skill before or during review to assess one PR's chance of being merged, identify blocking risks, and prioritize improvements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authenticated GitHub CLI access can expose PR metadata, comments, checks, commits, changed files, and author history visible to the logged-in account, including private repository data. <br>
Mitigation: Use the skill only on PRs the logged-in GitHub account is intended to analyze, and confirm the active gh CLI account before installation or execution. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/thcjp/skills/merge-check-tool-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and structured PR analysis reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses authenticated GitHub CLI data available to the local gh account for the target PR.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
