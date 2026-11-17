## Description:

Search Jerusalem specialty coffee shops by name, amenities, ratings, and opening hours.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexpolonsky](https://clawhub.ai/user/alexpolonsky)

### License/Terms of Use:

MIT

## Use Case:

External users and agents use this skill to find Jerusalem specialty coffee shops, compare amenities, check ratings and reviews, and identify shops that appear to be open now.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill fetches public Google Docs data and caches it locally; the security evidence flags cache handling as a local file-safety concern, especially in shared multi-user environments.

Mitigation: Install only in environments where this local cache behavior is acceptable; avoid administrator execution or shared multi-user use until the cache is private per user and terminal output is sanitized.

## Reference(s):

- [Jlm Coffee on ClawHub](https://clawhub.ai/alexpolonsky/skills/jlm-coffee)
- [Publisher profile](https://clawhub.ai/user/alexpolonsky)
- [Jerusalem coffee data site](https://coffee.amsterdamski.com)
- [Public JSON data export](https://docs.google.com/document/d/1BfsXKQLbKjogfSebRr0Ixt4L4VJHqPqTfnWxkosvcuM/export?format=txt)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Plain text or JSON CLI output, often summarized as Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Python 3 on macOS or Linux; CLI output can include ANSI color unless disabled; data is cached locally for 15 minutes.]

## Skill Version(s):

2.1.0 (source: server release metadata; artifact frontmatter says 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
