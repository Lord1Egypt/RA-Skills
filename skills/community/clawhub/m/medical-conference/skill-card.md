## Description:

Searches NoahAI medical conference and presentation databases for conferences, abstracts, posters, sessions, and conference-presented drug or trial data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bombert](https://clawhub.ai/user/bombert)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to answer medical conference questions by searching for conference metadata and presentation or abstract details by series, date, location, drug, disease, target, author, or institution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conference, drug, disease, author, institution, and target search terms are sent to noah.bio using NOAH_API_TOKEN.

Mitigation: Avoid sensitive private queries and review prompts, terminal output, and agent traces before sharing them.

Risk: The scripts print query payloads to stderr, which can expose search terms in shared terminals or logs.

Mitigation: Run the scripts in private sessions and protect or redirect logs when queries contain sensitive terms.

Risk: The scripts depend on Python requests and authenticated network access.

Mitigation: Use an isolated virtual environment with pinned dependencies and provide NOAH_API_TOKEN through the environment rather than inline command text.

## Reference(s):

- [NoahAI](https://noah.bio)
- [NoahAI API](https://www.noah.bio/api/)
- [ClawHub skill page](https://clawhub.ai/bombert/skills/medical-conference)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands]

**Output Format:** [Plain text search results or raw JSON, optionally saved to a file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns conference and presentation search results from NoahAI; the chained script can resolve a conference first and then search presentations.]

## Skill Version(s):

1.0.8 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
