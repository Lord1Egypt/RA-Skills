## Description:

Builds and manages professional resumes through the Placed career platform, including creation, updates, template changes, and PDF, DOCX, JSON, and Markdown exports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ajitsingh25](https://clawhub.ai/user/ajitsingh25)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to create, update, template, list, and export resumes on placed.exidian.tech with a Placed API key. It supports resume section editing, template browsing, and export workflows for PDF, DOCX, JSON, and Markdown outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive resume data and sends it to placed.exidian.tech.

Mitigation: Review resume contents before API calls and confirm before exporting, sharing, or making resumes public.

Risk: The skill may store a long-lived API key in a local plaintext credentials file.

Mitigation: Prefer a temporary or session-only API key, avoid plaintext credential files where possible, and confirm before writing credentials to disk.

Risk: The server security summary flags unsafe shell practices around local credential loading and API calls.

Mitigation: Review generated shell commands before execution and avoid sourcing or writing credential files unless the local exposure risk is acceptable.

## Reference(s):

- [Placed Resume Builder API Reference](references/api-guide.md)
- [Placed homepage](https://placed.exidian.tech)
- [ClawHub skill page](https://clawhub.ai/ajitsingh25/skills/placed-resume-builder)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash and JSON code blocks; API responses may include resume JSON, Markdown exports, and PDF or DOCX download URLs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [PDF download URLs expire after 15 minutes; API use requires a PLACED_API_KEY bearer token.]

## Skill Version(s):

1.1.0 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
