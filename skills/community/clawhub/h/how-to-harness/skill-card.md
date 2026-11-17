## Description:

How to Harness guides agents through structured design sessions for Harness-style closed-loop, self-optimizing AI systems where humans steer through evaluation, gates, versioning, rollback, and time-budget decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dimayip](https://clawhub.ai/user/dimayip)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, product leads, and AI system designers use this skill to turn ideas for closed-loop or self-optimizing agent systems into reviewed PRDs, design docs, RFCs, ADRs, kickoff checklists, one-pagers, or milestone plans. The skill is intended for systems that need evaluation-driven improvement, tiered automation, human approval gates, resumable execution, and explicit escalation paths.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill applies strong process constraints that can slow or redirect ordinary design work if invoked outside closed-loop or self-optimizing AI system design.

Mitigation: Review the trigger criteria before use and route ordinary product, CRUD, one-shot Q&A, or already-settled workflow requests to a more appropriate skill or direct documentation path.

Risk: Global installation makes the facilitation behavior available across future projects where its strict sequencing may not be desired.

Mitigation: Prefer project-local or manually inspected installation when the behavior should remain scoped to one workspace.

Risk: Unpinned npx installation commands can resolve different installer code over time.

Mitigation: Avoid running unpinned installers with elevated privileges and inspect the installation source or use a pinned, project-local installation path when possible.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dimayip/skills/how-to-harness)
- [OpenAI Harness Engineering](https://openai.com/index/harness-engineering/)
- [Decision Checklists](references/decision-checklists.md)
- [Deliverables Templates and Guide](references/deliverables.md)
- [Ralph Case Study](references/ralph-case-study.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Configuration, Shell commands]

**Output Format:** [Conversational guidance and structured Markdown deliverables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are produced section by section after user decisions are locked and approved.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
