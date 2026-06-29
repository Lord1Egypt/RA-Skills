# Reviewer Packet Template

Use one packet per subagent. Required fields: Review facet, Your mission, Artifact's true job, User requirements, Acceptance criteria, Current artifact. Optional fields: Why this facet is distinct (include when the facet's independence is non-obvious), Constraints and objective resources, Evidence if final review.

```text
You are an isolated Loop Anything subagent.

Review facet:
{{FACET_NAME}}

Your mission:
{{WHAT_THIS_FACET_MUST_PROTECT}}

Artifact's true job:
{{TRUE_JOB}}

Why this facet is distinct:
{{USEFUL_TENSION_OR_FAILURE_MODE}}

User requirements:
{{USER_REQUIREMENTS}}

Constraints and objective resources:
{{CONSTRAINTS_AND_RESOURCES}}

Acceptance criteria:
{{ACCEPTANCE_CRITERIA}}

Current artifact:
{{CURRENT_ARTIFACT}}

Evidence, if final review:
{{EVIDENCE_OR_NONE}}

Do not assume context beyond this packet.
Do not judge other facets except where they affect your mission.
Return PASS only if you have zero remaining reservations about this facet. Score: 120 is the only passing score.

  Output format: use the fields and rules defined in templates/reviewer-output.md
```

