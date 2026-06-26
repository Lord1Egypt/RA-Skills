## Description: <br>
Manages PRs, watches issues, checks CI, and prepares releases for routine GitHub repository maintenance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yezhaowang888-stack](https://clawhub.ai/user/yezhaowang888-stack) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Project maintainers, engineering managers, and open-source contributors use this skill to triage PRs and issues, check CI status, detect merge conflicts, and track work across repositories. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: GitHub token access can expose private repositories or allow unintended repository changes if the token is too broad. <br>
Mitigation: Use a narrowly scoped token limited to the intended repositories, and prefer read-only permissions unless write actions are required. <br>
Risk: Repository-changing actions such as commenting, labeling, closing issues, assigning reviewers, triggering CI, publishing releases, merging PRs, or deleting branches can affect live projects. <br>
Mitigation: Require explicit confirmation before any write, release, merge, or destructive branch action. <br>
Risk: Automated PR, issue, and CI summaries can be incomplete or wrong. <br>
Mitigation: Review the generated guidance and verify critical CI or release status in GitHub before acting on it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yezhaowang888-stack/huimai-github-auto) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries with inline commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require GITHUB_TOKEN and explicit confirmation for repository-changing actions.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence and SKILL.md changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
