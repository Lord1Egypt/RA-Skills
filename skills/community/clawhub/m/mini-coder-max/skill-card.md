## Description: <br>
Autonomous coding agent that systematically plans, implements, reviews, and delivers high-quality code by following a structured planning, implementation, quality assurance, and delivery workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nemo-ryanniddel](https://clawhub.ai/user/nemo-ryanniddel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to structure coding work across planning, research, implementation, review, and delivery. It is intended for broad coding tasks, from small fixes to larger multi-module software changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill has broad coding-task activation and may propose or perform file changes in sensitive repositories. <br>
Mitigation: Review the plan before allowing file changes, run changes in a controlled workspace, and keep repository permissions scoped to the task. <br>
Risk: Prompts or research context could expose private credentials or sensitive project information if supplied by the user. <br>
Mitigation: Do not include secrets, tokens, or private credentials in prompts, and redact sensitive repository details before requesting external research. <br>
Risk: Generated code or guidance can still be incorrect or incomplete for the target system. <br>
Mitigation: Require code review, run relevant tests and security checks, and validate the implementation against the original requirements before deployment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/nemo-ryanniddel/mini-coder-max) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/nemo-ryanniddel) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with code blocks, command snippets, review notes, and delivery summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include plans, assumptions, risk notes, implementation details, test results, and follow-up guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
