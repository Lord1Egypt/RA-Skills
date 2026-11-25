## Description:

Query Karman, a monitor for small Solar System bodies whose motion gravity does not explain (non-gravitational accelerations, interstellar visitors). Use when the user asks which asteroids or comets move anomalously, why an object got its label, how the evidence compares with JPL, what the watch has seen lately, or how the method was validated.

This skill is ready for commercial/non-commercial use.

## Publisher:

[logic](https://clawhub.ai/user/logic)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and astronomy researchers use this skill to query Karman's anomaly monitoring results, inspect evidence and validation, compare findings with JPL, and check interstellar visitor watch status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The supplied security results note a low-probability Unicode warning but do not identify the flagged text.

Mitigation: Review the flagged text in SKILL.md; the scan rates the release benign and treats the warning as expected for the skill's purpose.

Risk: Users could mistake an anomaly label or candidate for a confirmed cause or identification.

Mitigation: Present labels as the most likely cause on the available evidence, retain status and limits with reported figures, and describe candidates as needing checks.

## Reference(s):

- [Karman](https://karman.si)
- [Karman MCP server](https://karman.si/mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis, API Calls]

**Output Format:** [Text or Markdown explanations and summaries of queried objects, anomaly evidence, validation, and watch status.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Answers should preserve reported status and limits; labels describe the most likely cause on available evidence, not a confirmed identification.]

## Skill Version(s):

0.1.1 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
