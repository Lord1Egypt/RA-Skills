## Description: <br>
Activates an explicitly critical review posture when a user asks the agent to find problems, stress test an artifact, challenge assumptions, or play devil's advocate. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[long1973m](https://clawhub.ai/user/long1973m) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, developers, and reviewers use this skill to request adversarial review of plans, code, documents, arguments, data pipelines, architectures, prompts, and other artifacts. It focuses the agent on surfacing concrete flaws, risks, assumptions, edge cases, failure modes, and unverified claims. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill intentionally pushes the agent toward harsh, problem-focused feedback, which may produce overly severe or unbalanced review output if the user expects neutral analysis. <br>
Mitigation: Use this skill only when explicitly critical feedback is desired, and give clear scope and tone limits when needed. <br>
Risk: The skill asks the agent to verify claims and test behavior, which could lead to unsafe handling of untrusted code if execution is allowed without boundaries. <br>
Mitigation: Do not allow the agent to run or test untrusted code unless the user explicitly approves execution in a safe sandbox. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown findings organized by problem category, with unverified claims listed separately] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only skill; produces critical review guidance and does not define tools, credential use, persistence, or external data access.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
