## Description: <br>
pr-pilot helps agents submit professional pull requests and manage the lifecycle from branch push through PR creation, CI monitoring, review responses, iteration, and tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sliverp](https://clawhub.ai/user/sliverp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use pr-pilot to prepare structured pull request descriptions, run GitHub CLI workflows, monitor CI and reviews, respond to feedback, and track multiple PRs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide pushes, PR creation, comments, and other GitHub actions using the user's account. <br>
Mitigation: Before allowing commands, confirm the exact repository, branch, staged files, PR title and body, comments, and any force-push or merge-conflict steps. <br>
Risk: GitHub authentication may expose or overuse credentials if tokens are pasted into chat, logs, or broad-permission environments. <br>
Mitigation: Use least-privileged GitHub authentication and avoid pasting long-lived tokens into chat or logs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sliverp/pr-pilot) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance, Configuration] <br>
**Output Format:** [Markdown guidance with shell command blocks and PR description templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include PR URLs, CI status summaries, review responses, and a pr-tracker.md table for multi-PR tracking.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
