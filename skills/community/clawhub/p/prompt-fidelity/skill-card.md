## Description:

Self-checks how much of a search, filtering, recommendation, or data-retrieval request is verifiable versus judgment before answering.

This skill is ready for commercial/non-commercial use.

## Publisher:

[barneyjm](https://clawhub.ai/user/barneyjm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to make mixed objective and subjective answers more transparent. It decomposes a request into constraints, separates verified checks from inferred judgment, and reports fidelity, injected filters, and coverage limits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A referenced helper script is not included in the artifact, so the workflow may fail if followed literally.

Mitigation: Confirm the helper script is supplied in the installed skill or adapt the score calculation before relying on the workflow.

Risk: The skill can lead an agent to propose database or API queries over large or sensitive systems.

Mitigation: Review query scope before execution and prefer cheap counts, planner statistics, samples, or bounded local checks over unbounded scans.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/barneyjm/skills/prompt-fidelity)
- [Server-resolved GitHub provenance](https://github.com/Barneyjm/prompt-fidelity/tree/main/skills/prompt-fidelity)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with optional JSON constraint objects and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports verified vs inferred constraints, fidelity score framing, injected filters, and coverage limits.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
