## Description: <br>
Local approval system for managing agent permissions, approving or denying requests, viewing history, and managing auto-approved categories. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shaiss](https://clawhub.ai/user/shaiss) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to add a local human-in-the-loop approval workflow around agent actions, including reviewing pending requests, approving or denying them, and managing category-based auto-approvals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Standing auto-approvals may allow future agent actions in learned categories to proceed without human review. <br>
Mitigation: Use learned categories only for narrow, low-risk actions, review categories and pending or history files regularly, and reset approvals after mistakes or suspicious behavior. <br>
Risk: A governed agent with access to approval commands could approve its own requests or add new learned categories. <br>
Mitigation: Restrict approve, approve --learn, deny, and reset commands to a trusted user or trusted wrapper; do not let governed agents run approval-management commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shaiss/local-approvals) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [CLI text output and local JSON state files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Maintains local pending request and approval state under the user's OpenClaw skill directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
