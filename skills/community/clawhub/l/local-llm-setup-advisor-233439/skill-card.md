## Description:

Helps developers, researchers, privacy-conscious users, hobbyists, and small teams plan and validate local LLM workflows on consumer CPU or GPU hardware without relying on cloud-only systems.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical users use this skill to choose practical local LLM setup steps, checklists, commands, and validation methods for ordinary CPU or consumer GPU hardware. It is intended for privacy-friendly workflows that avoid cloud-only dependencies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad activation wording may route loosely related local AI questions to this skill.

Mitigation: Review automatic routing behavior before deployment and narrow trigger wording if precise invocation is required.

Risk: Advice about local LLM setup may be incomplete or mismatched to a user's hardware or software environment.

Mitigation: Require the agent to restate assumptions, request material missing constraints, and include verification commands or checks before the user acts on setup guidance.

## Reference(s):

- [Requirement Plan](artifact/references/requirement-plan.md)
- [Local LLM Setup Advisor on ClawHub](https://clawhub.ai/kyro-ma/skills/local-llm-setup-advisor-233439)
- [Ask HN: MacBook vs. Dedicated GPU for LLM](https://news.ycombinator.com/item?id=48696532)
- [vLLM Disaggregated Prefill LMCache](https://segmentfault.com/a/1190000046720505)
- [vLLM Disaggregated Prefill](https://segmentfault.com/a/1190000046807401)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with checklists, inline code, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are tailored to the user's hardware, privacy constraints, and validation needs.]

## Skill Version(s):

0.20260729.110214 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
