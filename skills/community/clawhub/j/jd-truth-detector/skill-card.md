## Description:

Reverse-engineers job descriptions by translating jargon, inferring culture signals, comparing an optional resume, and identifying negotiation signals from pasted text, selected job-posting URLs, or text, Markdown, DOCX, and PDF files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ucsdzehualiu](https://clawhub.ai/user/ucsdzehualiu)

### License/Terms of Use:

MIT

## Use Case:

Developers and job seekers use this skill to analyze job descriptions, surface likely real requirements and culture signals, compare a resume when provided, and prepare negotiation questions. It is intended for advisory analysis, not automated employment decision-making.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: URL scraping can fetch untrusted pages and may be unsuitable in environments with access to internal services.

Mitigation: Prefer pasted job-description text for untrusted postings and avoid URL mode from privileged networks.

Risk: Job-description and resume content can be sent to the configured LLM endpoint.

Mitigation: Use a trusted or local OpenAI-compatible endpoint for sensitive resumes and review configuration before running analysis.

Risk: Generated reports can reflect misleading or manipulative language from the job posting.

Mitigation: Treat the report as advisory and review findings before using them for application or negotiation decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ucsdzehualiu/skills/jd-truth-detector)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and HTML reports generated from structured analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can use pasted text, URL scraping, or local files as input and can send job-description and resume content to a configured OpenAI-compatible LLM endpoint.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
