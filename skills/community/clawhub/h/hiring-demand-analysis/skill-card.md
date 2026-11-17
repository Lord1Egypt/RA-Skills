## Description:

Compare advertised hiring demand across roles, skills, locations, and seniority using Crawlora's jobs dataset, with explicit controls for coverage and compensation units.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, recruiters, and workforce planners use this skill to compare observed job postings by role, skill, location, employer, seniority, remote status, and advertised pay while reporting sample coverage and limitations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Job queries and the Crawlora API key are sent to Crawlora.

Mitigation: Use a key intended for Crawlora and avoid sensitive or unnecessary search parameters.

Risk: Mixing Google Jobs samples with stored dataset counts or treating postings as hires can misstate demand.

Mitigation: Report separate sources, deduplicated denominators, observation dates, and coverage limits.

Risk: Large searches can consume API credits.

Mitigation: Agree on a bounded sample and review credit usage before extensive queries.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/crawlora-org/skills/hiring-demand-analysis)
- [Crawlora jobs endpoint reference](reference/endpoints.md)
- [Crawlora](https://crawlora.net)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands]

**Output Format:** [Markdown analysis with counts, proportions, and cited example postings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes cohort definitions, denominators, exclusions, sample coverage, compensation units, and limitations.]

## Skill Version(s):

1.0.12 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
