## Description:

Search and discover academic scholars using OpenJobs AI with filters for name, affiliation, research areas, citations, h-index, publications, education, and location.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openjobsai](https://clawhub.ai/user/openjobsai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to search the OpenJobs AI scholar database, discover academic researchers, and present concise researcher summaries from structured API results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential handling can expose the MIRA_KEY if the agent prints or repeats the environment variable.

Mitigation: Use a non-disclosing presence check for MIRA_KEY and avoid echoing, logging, or repeating the key in conversation.

Risk: Search criteria are sent to OpenJobs AI.

Mitigation: Submit only search criteria appropriate for the OpenJobs AI service and avoid adding unrelated sensitive information to queries.

Risk: The skill's response rules try to suppress extra warnings after results.

Mitigation: Preserve concise result formatting while still allowing necessary security, privacy, or correctness warnings.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/openjobsai/skills/openjobs-ai-talent-search)
- [OpenJobs AI](https://www.openjobs-ai.com/?utm_source=scholar_search_skill)
- [OpenJobs AI platform](https://platform.openjobs-ai.com/)
- [OpenJobs AI scholar search API endpoint](https://mira-api.openjobs-ai.com/v1/scholar-fast-search)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries with inline shell commands and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MIRA_KEY; scholar-fast-search requires at least one filter and returns up to 20 results.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
