## Description: <br>
Guides when to ask clarifying questions versus proceed autonomously to reduce unnecessary clarifying questions when intent is clear. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and agent operators use this skill to decide when an assistant should ask clarifying questions and when it should proceed autonomously. It is intended to reduce unnecessary interruptions while preserving review, confirmation, and rollback for high-risk work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated or selected guidance may lead an agent to proceed when clarification would be needed for destructive, security-critical, data-migration, or breaking-change work. <br>
Mitigation: Require explicit confirmation for irreversible or high-stakes operations and document assumptions before proceeding. <br>
Risk: Text produced with this skill may be factually incorrect, incomplete, or unsuitable for formal administrative or organizational use. <br>
Mitigation: Review generated text for factual accuracy, policy or legal compliance, confidentiality, and required formatting before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/nm-conserve-decisive-action) <br>
- [Source homepage from metadata](https://github.com/athola/claude-night-market/tree/master/plugins/conserve) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, text, markdown] <br>
**Output Format:** [Markdown guidance and decision criteria] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Text-only guidance; no credentials, tools, MCP servers, or executable scripts detected.] <br>

## Skill Version(s): <br>
1.9.12 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
