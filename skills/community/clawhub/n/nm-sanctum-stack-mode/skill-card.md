## Description: <br>
Detects shared stack membership and iterates a command across all PRs in base-to-tip order. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent-command authors use this skill to make commands operate across a stack of dependent pull requests, resolving stack membership, iterating each PR in base-to-tip order, and producing a consolidated root summary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger terms may cause the skill to be used during an ordinary single-PR review conversation. <br>
Mitigation: Use explicit --stack intent for multi-PR iteration and fall back to the normal single-PR workflow when stack mode is not intended. <br>
Risk: The workflow reads pull request metadata and can post a consolidated stack summary through the GitHub CLI. <br>
Mitigation: Confirm the target repository, GitHub CLI authorization, and generated summary before allowing the comment to be posted. <br>
Risk: A failed PR in the middle of a stack can leave downstream PR context stale. <br>
Mitigation: Halt iteration at the failed PR and leave downstream PRs untouched until the failure is resolved. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/athola/skills/nm-sanctum-stack-mode) <br>
- [Configured homepage](https://github.com/athola/claude-night-market/tree/master/plugins/sanctum) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Markdown, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides callers to resolve PR stacks, iterate workflows, and post one consolidated root summary comment.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
