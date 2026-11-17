## Description:

Converts Markdown files or strings into formatted HTML for web display, static site generation, documentation, and content pipeline workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[frankxpj](https://clawhub.ai/user/frankxpj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content engineers use this skill to convert Markdown input from files, stdin, or Node.js code into HTML snippets or output files. It is suited to local trusted notes, documentation conversion, and content pipeline drafts that receive downstream security review before publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Converted HTML can be unsafe if generated from untrusted Markdown or published directly to a website, CMS, or database-rendered page.

Mitigation: Use the skill for trusted local content or add a real HTML sanitizer and URL validation before publishing the generated HTML.

Risk: The artifact documentation presents code-block escaping as safe, but the converter does not provide comprehensive HTML sanitization.

Mitigation: Treat the generated HTML as unsanitized output and review it before deployment or downstream storage.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/frankxpj/skills/md-2-html)

## Skill Output:

**Output Type(s):** [text, code, shell commands]

**Output Format:** [Markdown guidance with shell and JavaScript examples; generated HTML as text or files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces content HTML without a full html/head/body wrapper.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
