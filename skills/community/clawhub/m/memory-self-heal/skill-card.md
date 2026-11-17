## Description:

General-purpose self-healing loop that learns from past failures, retries safely, and records reusable fixes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dalomeve](https://clawhub.ai/user/dalomeve)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill when an agent repeatedly fails, stalls, or reports completion without verifiable artifacts. It guides the agent through evidence scanning, failure classification, bounded retries, controlled escalation, and concise memory writeback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can prompt broad scans of memory, task files, and runtime logs, which may expose secrets or unrelated project data.

Mitigation: Use it only with project-scoped evidence locations, redact credentials before writeback, and limit scan roots to approved paths.

Risk: Reusable recovery rules written to memory can affect future sessions if they are too broad or insufficiently validated.

Mitigation: Require concise, evidence-backed memory entries and review reusable rules before allowing them to guide later tasks.

Risk: Repeated automated retries can waste time or compound incorrect assumptions.

Mitigation: Keep the documented maximum of three retries per blocker signature and escalate with the minimum unblock input when validation does not succeed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dalomeve/skills/memory-self-heal)
- [Publisher Profile](https://clawhub.ai/user/dalomeve)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell command examples and structured checklist/writeback blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces bounded recovery steps, validation checks, escalation prompts, and concise memory entries.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
