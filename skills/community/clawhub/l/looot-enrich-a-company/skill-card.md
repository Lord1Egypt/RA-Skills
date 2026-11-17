## Description:

Enrich a company. Use when the user says things like "tell me about example.com as a company", "enrich this list of company domains" or "how big is this company and what do they do". Runs through looot, billed per call.

This skill is ready for commercial/non-commercial use.

## Publisher:

[walidboulanouar](https://clawhub.ai/user/walidboulanouar)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to look up company profile details from one or more domains and summarize the available information, such as industry, headcount, headquarters, and founding year. It is intended for users who want to understand a company or enrich a list of known companies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A paid enrichment run can incur per-call charges.

Mitigation: Inspect the endpoint and its current list price, show the price, and get approval before running; report the total after a batch.

Risk: The security scan evidence is incomplete because one local reference could not be matched to a bundled artifact.

Mitigation: Review the unmatched reference and scan the complete packaged skill before deployment.

## Reference(s):

- [Looot skill setup](https://looot.ai/skill.md)
- [Enrich a Company page](https://looot.ai/agent-skills/enrich-a-company)
- [ClawHub release page](https://clawhub.ai/walidboulanouar/skills/looot-enrich-a-company)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Structured text or Markdown company profile]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Available company fields vary by provider; unavailable funding or technology details are identified as missing.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
