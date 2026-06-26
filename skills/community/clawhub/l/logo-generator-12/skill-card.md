## Description: <br>
Interact with GitHub using the `gh` CLI for issues, pull requests, CI runs, workflow logs, API queries, JSON output, and jq filtering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hucy](https://clawhub.ai/user/hucy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to ask an agent for GitHub CLI commands and guidance for inspecting pull requests, workflow runs, logs, and API responses. Users should verify the active GitHub account and repository target before running commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The public release identity is logo-generator, but the artifact behaves as a GitHub CLI helper, which could mislead users before it uses their local GitHub access. <br>
Mitigation: Install only if a GitHub CLI helper is intended, and review the artifact behavior before enabling the skill. <br>
Risk: Suggested gh commands may operate with the user's currently authenticated GitHub account and may target the wrong repository if context is ambiguous. <br>
Mitigation: Verify `gh` authentication, use explicit `--repo owner/repo` targets, and manually review any command that writes, deletes, merges, dispatches workflows, or uses raw `gh api`. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/hucy/logo-generator-12) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include gh CLI commands that can read or change GitHub resources depending on the command selected by the user.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
