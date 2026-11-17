## Description:

Reads your resume pool to build a candidate profile, then searches LinkedIn, Indeed, Glassdoor, ZipRecruiter, Google Jobs, and company career pages for matching roles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jerronl](https://clawhub.ai/user/jerronl)

### License/Terms of Use:

MIT-0

## Use Case:

Job seekers and career-focused agents use this skill to search for roles that match a resume-derived candidate profile, configured keywords, location, salary, and listing recency. It records shortlisted, rejected, and errored results in a structured local tracker and carries search context forward through handoff notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads a local resume directory and may process personal employment history, contact details, salary targets, and role preferences.

Mitigation: Set RESUME_DIR to a dedicated folder containing only resumes the user wants the agent to inspect.

Risk: The tracker and handoff files persist job-search history, rejected roles, shortlisted roles, salary targets, and contact notes on the local machine.

Mitigation: Review those files periodically and delete or redact sensitive entries when they are no longer needed.

## Reference(s):

- [Jobautopilot Search on ClawHub](https://clawhub.ai/jerronl/skills/jobautopilot-search)
- [Publisher profile: jerronl](https://clawhub.ai/user/jerronl)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown tracker rows, Markdown handoff notes, plain-text candidate profile summaries, and shell configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a browser tool with the search profile and local environment variables for keywords, location, tracker, handoff, resume directory, salary, and listing age filters.]

## Skill Version(s):

1.3.0 (source: release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
