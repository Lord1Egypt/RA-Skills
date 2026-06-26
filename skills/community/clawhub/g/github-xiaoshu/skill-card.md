## Description: <br>
Interact with GitHub using the `gh` CLI. Use `gh issue`, `gh pr`, `gh run`, and `gh api` for issues, PRs, CI runs, and advanced queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaomaju-888](https://clawhub.ai/user/xiaomaju-888) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to guide an agent in inspecting GitHub issues, pull requests, CI workflow runs, logs, and advanced GitHub API queries through the authenticated `gh` CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill guides use of an authenticated `gh` CLI, including commands that can inspect or modify GitHub issues, pull requests, workflows, and API resources. <br>
Mitigation: Review the exact repository target and command before allowing write operations, especially `gh api`, workflow, pull request, or issue-modifying actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiaomaju-888/github-xiaoshu) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, API Calls, Markdown] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include `gh` command examples and JSON or jq filtering guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
