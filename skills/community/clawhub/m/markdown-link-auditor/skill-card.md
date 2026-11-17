## Description:

Audits Markdown for empty labels, duplicate URLs, raw URLs, suspicious schemes, and missing image alt text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hmahmadcs](https://clawhub.ai/user/hmahmadcs)

### License/Terms of Use:

MIT-0

## Use Case:

Documentation authors and developers use this skill to review pasted Markdown for link hygiene issues before publishing READMEs, documentation, or release announcements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live link checks could access external URLs beyond the default static audit.

Mitigation: Do not fetch links by default; obtain explicit approval for each URL before checking its HTTP status.

Risk: Suspicious link schemes could be unsafe to open.

Mitigation: Flag suspicious schemes in the report without opening javascript: or data URLs.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/hmahmadcs/skills/markdown-link-auditor)
- [CommonMark specification](https://commonmark.org/)
- [MDN HTTP response status codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Issue counts, short excerpts, suggested rewrites, and a prioritized checklist.]

## Skill Version(s):

1.0.1 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
