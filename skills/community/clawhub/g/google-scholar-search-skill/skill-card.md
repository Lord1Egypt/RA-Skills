## Description:

Search academic papers on Google Scholar with keyword, author, and year filters, retrieve author profile metadata, and export results as JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackkuo666](https://clawhub.ai/user/jackkuo666)

### License/Terms of Use:

MIT

## Use Case:

Researchers, students, and developers use this skill to search academic literature, filter paper results, inspect author profiles, and save search results for downstream analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation guidance includes a pipe-to-shell installer path and dependencies that are not pinned to exact versions.

Mitigation: Install in an isolated, non-root virtual environment, review installer scripts before execution, and pin or lock dependencies before production use.

Risk: Runtime behavior scrapes Google Scholar and may be blocked, rate limited, or produce variable results.

Mitigation: Use responsible request patterns, validate returned metadata before relying on it, and consider official literature APIs when stable access is required.

Risk: The skill can write JSON output to a user-provided path.

Mitigation: Review output paths before execution and run the skill with least-privilege filesystem access.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jackkuo666/skills/google-scholar-search-skill)
- [Google Scholar](https://scholar.google.com/)
- [scholarly Python package](https://pypi.org/project/scholarly/)
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Console text or JSON file output with paper and author metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on Google Scholar availability, anti-bot behavior, and optional output file paths supplied by the user.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
