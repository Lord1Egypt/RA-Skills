## Description: <br>
Run an Oxford Union-style multi-agent debate on any motion using Mixture of Agents architecture. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[markoxmobs](https://clawhub.ai/user/markoxmobs) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, developers, and analysts use this skill to run structured Oxford Union-style debates that stress-test a motion, prepare arguments, and produce a balanced debate brief. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A debate run can make many sequential model calls and consume time or tokens. <br>
Mitigation: Set an appropriate hard round cap and completeness threshold before starting. <br>
Risk: Motions may include sensitive or confidential material that is sent to the configured LLM provider. <br>
Mitigation: Avoid confidential motions unless the provider and workspace are approved for that data. <br>
Risk: Debate outputs can sound persuasive even when arguments or evidence are incomplete. <br>
Mitigation: Treat the final brief as preparation material and verify factual claims before relying on it. <br>


## Reference(s): <br>
- [Oxford Union Debate - Reference Guide](references/DEBATE_FORMAT.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown debate transcript and structured brief; the brief generation step asks the model for JSON before presentation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses user-selected completeness threshold and hard round cap; normal runs may make many sequential LLM calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
