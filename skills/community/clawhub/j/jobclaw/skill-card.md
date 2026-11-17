## Description:

Job Hunter helps agents search public LinkedIn job listings, filter by role, technology, location, and experience, and optionally score matches with Google Gemini.

This skill is ready for commercial/non-commercial use.

## Publisher:

[keepfit44](https://clawhub.ai/user/keepfit44)

### License/Terms of Use:

MIT-0

## Use Case:

Job seekers and career-support agents use this skill to search job postings, narrow results by technology and geography, score fit against stated criteria, save interesting jobs, and revisit prior searches.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Gemini API keys, saved jobs, and search history are stored locally in plaintext.

Mitigation: Use the skill only on trusted machines, avoid command-line key setup on shared or logged systems, restrict file permissions where possible, and rotate the Gemini key if exposure is suspected.

Risk: When AI scoring is enabled, job listings and user criteria are sent to Google Gemini.

Mitigation: Do not include sensitive personal details in free-text criteria, and enable AI scoring only when this external processing is acceptable.

Risk: The skill scrapes public LinkedIn job pages and may encounter rate limits or access changes.

Mitigation: Expect slower searches, pause after scraping errors or rate limits, and review use against applicable site terms before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/keepfit44/skills/jobclaw)
- [Search Format Reference](references/search_format.md)
- [Google AI Studio API Keys](https://aistudio.google.com/apikey)
- [LinkedIn Jobs Search](https://www.linkedin.com/jobs/search/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON job-search results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results are scored, sorted, and capped for presentation; saved jobs and search history are retained locally.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
