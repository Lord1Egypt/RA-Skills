## Description: <br>
Autonomous PR review loop with Greptile for reading review feedback, fixing issues, pushing updates, re-triggering review, and merging pull requests when the review score is sufficient. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cemoso](https://clawhub.ai/user/cemoso) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering agents use this skill to manage Greptile pull request feedback loops: fetch reviews, parse scores, apply fixes, push follow-up commits, and decide when to merge or escalate. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can push commits, post pull request comments, merge pull requests, and delete branches. <br>
Mitigation: Install it only in repositories where the agent is explicitly allowed to perform those actions, and rely on repository protections or human approval before merge and branch deletion. <br>
Risk: The skill includes force-merge paths when review rounds are exhausted or scores stagnate. <br>
Mitigation: Disable or gate force-merge behavior for low, failed, or stagnant review scores unless a human reviewer approves the merge. <br>
Risk: Automated fixes may change code in response to review comments without fully resolving architectural or ambiguous issues. <br>
Mitigation: Escalate architectural decisions and unclear feedback to a human reviewer before applying fixes or merging. <br>


## Reference(s): <br>
- [Common Greptile Feedback Patterns](references/greptile-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON from the helper script, with Markdown guidance and inline bash commands in the skill documentation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The helper script writes or updates review-state.json in the workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
