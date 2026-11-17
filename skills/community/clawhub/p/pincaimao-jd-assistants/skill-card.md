## Description:

Pincaimao JD Assistant helps agents call the Pincaimao API to generate recruitment job postings from job descriptions and structured job tags from job titles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pincaimao](https://clawhub.ai/user/pincaimao)

### License/Terms of Use:

MIT-0

## Use Case:

Recruiters, HR operators, and agent developers use this skill to generate job posting drafts and structured job tags through Pincaimao's authenticated service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Hiring content is transmitted to Pincaimao's external service for processing.

Mitigation: Use the skill only when organizational policy permits Pincaimao to process the submitted recruitment data.

Risk: PCM_JD_ASSISTANT_KEY is a bearer credential used for authenticated API requests.

Mitigation: Store the key in the environment, avoid hardcoding it, and rotate it if exposure is suspected.

Risk: The skill depends on a companion pincaimao-basic skill for shared interface behavior.

Mitigation: Verify the companion skill before installing or using this skill in an agent environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pincaimao/skills/pincaimao-jd-assistants)
- [Pincaimao homepage](https://www.pincaimao.com)
- [Pincaimao API endpoint](https://api.pincaimao.com)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown with command examples, human-readable summaries, and optional raw API JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses PCM_JD_ASSISTANT_KEY for authenticated requests to Pincaimao.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
