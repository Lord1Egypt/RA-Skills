## Description:

Check selected pages once for status, redirects, timing and basic SEO fields.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hznetnewpower](https://clawhub.ai/user/hznetnewpower)

### License/Terms of Use:

MIT No Attribution

## Use Case:

External users and site owners use this skill to check 1–5 explicitly selected public HTTPS pages once, review availability, redirects, response time, TLS validation and basic static HTML SEO fields, and save JSON and Markdown reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Website operators can see the requests and the checking host's IP address.

Mitigation: Check only public URLs you intend to contact, and do not include login or session secrets.

Risk: Reports remain in the workspace and their content may enter the configured model's context.

Mitigation: Review reports before sharing and remove them from the workspace when they are no longer needed.

Risk: Using an unreviewed CLI release may introduce unexpected changes.

Mitigation: Prefer a reviewed CLI version over installing @latest.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/hznetnewpower/skills/mochi-site-check)
- [MochiLab homepage](https://mochilab.bz)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown]

**Output Format:** [JSON and Markdown report files with a concise natural-language summary]

**Output Parameters:** [1D (one batch of 1–5 URLs)]

**Other Properties Related to Output:** [One-off reports are saved as new files; response timing is measured from the running host and SEO fields come from static HTML.]

## Skill Version(s):

1.0.1 (source: SKILL.md frontmatter metadata, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
