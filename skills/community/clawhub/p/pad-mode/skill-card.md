## Description: <br>
Pad Mode helps an agent turn complex requests into structured Plan, Act, Deliver workflows with task breakdowns, approval gates, execution tracking, and completion review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yipxiyi](https://clawhub.ai/user/yipxiyi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and other agent users use Pad Mode to plan and track non-trivial work before execution. It is most useful for multi-step requests that need explicit scope, approval, verification, and completion review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Plan files may contain sensitive information from user requests because they are saved locally. <br>
Mitigation: Avoid putting secrets or sensitive data in requests and review generated plan files before approving execution. <br>
Risk: High-impact work such as deployments, payments, databases, or account changes can cause unwanted changes if approved without review. <br>
Mitigation: Use foreground mode for high-impact work and review each plan before allowing execution. <br>


## Reference(s): <br>
- [Pad Mode on ClawHub](https://clawhub.ai/yipxiyi/pad-mode) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown plans, status updates, and concise execution guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local plan documents and requires user approval gates before execution.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
