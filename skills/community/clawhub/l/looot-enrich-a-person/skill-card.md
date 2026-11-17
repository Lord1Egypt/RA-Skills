## Description:

Enrich a person from an email, LinkedIn profile, or name and company through looot, with billed calls requiring user approval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[walidboulanouar](https://clawhub.ai/user/walidboulanouar)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to look up professional details from an email, LinkedIn profile, or name and company. It supports contact enrichment for routing, scoring, and profile completion, with the user approving each billed lookup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Person identifiers are sent to an external enrichment provider, and lookups may return personal details.

Mitigation: Use only an identifier appropriate for the task and tell the user which provider and price apply before running a billed lookup; run only after approval.

Risk: A lookup can return an uncertain or incomplete match.

Mitigation: Retain any reported match likelihood, list missing fields, and do not fill gaps from memory.

## Reference(s):

- [looot skill setup instructions](https://looot.ai/skill.md)
- [Person enrichment skill page](https://looot.ai/agent-skills/enrich-a-person)
- [ClawHub skill release](https://clawhub.ai/walidboulanouar/skills/looot-enrich-a-person)

## Skill Output:

**Output Type(s):** [API Calls, Text, Markdown]

**Output Format:** [Person-enrichment results summarized in text or Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include match confidence and notes for fields that were not returned.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
