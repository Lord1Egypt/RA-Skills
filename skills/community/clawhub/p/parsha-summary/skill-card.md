## Description:

Generates weekly Torah portion summaries from Sefaria, with optional Hebrew text, verse counts, sample verses, and JSON output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abeperl](https://clawhub.ai/user/abeperl)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to get quick weekly parsha overviews or parsha content for a dvar Torah outline, either for the current week or by selecting a named Torah portion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on outbound requests to Hebcal and Sefaria for calendar and Torah text data.

Mitigation: Review network access policy before installation and use it only where outbound requests to those public APIs are acceptable.

## Reference(s):

- [Sefaria API](https://www.sefaria.org/api)
- [Hebcal API](https://www.hebcal.com/hebcal)
- [ClawHub Skill Page](https://clawhub.ai/abeperl/skills/parsha-summary)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Plain text or JSON, with command examples shown in Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Optional Hebrew text; configurable summary length; requires outbound requests to Hebcal and Sefaria for current calendar and Torah text data.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
