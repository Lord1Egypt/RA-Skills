## Description:

Builds requirements-based open-source project shortlists using public GitHub metadata and project documentation to compare capabilities, maintenance, licenses, and compatibility.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to shortlist public open-source libraries or tools against project requirements, compare evidence and tradeoffs, and identify unanswered adoption questions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Public repository queries and documentation URLs are sent to Crawlora using an API key; sensitive inputs could be exposed.

Mitigation: Use only public repositories and documentation; exclude secrets, internal documents, and sensitive adoption criteria from requests.

Risk: Broad searches and scraping can consume API credits beyond the shortlist task.

Mitigation: Keep requests and pages bounded by the task scope and available credit budget.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/crawlora-org/skills/open-source-project-shortlisting)
- [Crawlora endpoint reference](reference/endpoints.md)

## Skill Output:

**Output Type(s):** [Analysis, Guidance]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Conditional shortlist, requirements/evidence matrix, tradeoffs, version and license pointers, and follow-up questions.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
