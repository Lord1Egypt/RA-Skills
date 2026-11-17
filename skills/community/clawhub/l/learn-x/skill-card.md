## Description:

Learn-X is a subject-agnostic Socratic learning coach that helps an agent diagnose a learner's starting point, introduce one concept at a time, ask structured questions, and end each session with a learner-produced artifact.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dimayip](https://clawhub.ai/user/dimayip)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill when they want an agent to coach them through learning a topic rather than directly lecturing or completing the work for them. It is intended for learning sessions where diagnosis, active recall, guided practice, and a tangible learner artifact are more important than fast factual answers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation instructions may cause users to install an unreviewed or moving version of the skill.

Mitigation: Install from a reviewed commit or pinned package version when possible, and prefer project-scoped installation over global installation.

Risk: The broad activation wording may route general learning requests into a structured coaching flow when the user expected a direct answer.

Mitigation: Use this skill when the user wants guided learning, active recall, and a learner-produced artifact; route pure fact lookups or delegated work to a more appropriate workflow.

Risk: The artifact is primarily Chinese with an English README, so users may receive coaching in an unintended language depending on the agent environment.

Mitigation: Confirm the user's preferred language at the start of the session when language preference is unclear.

## Reference(s):

- [Learn-X ClawHub skill page](https://clawhub.ai/dimayip/skills/learn-x)
- [diagnose-playbook.md](references/diagnose-playbook.md)
- [question-templates.md](references/question-templates.md)
- [session-patterns.md](references/session-patterns.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown conversational guidance with structured questions and learner-facing tasks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces coaching prompts, milestone paths, micro-tasks, lock-in reviews, and learner artifact options; it does not run tools or access data by itself.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
