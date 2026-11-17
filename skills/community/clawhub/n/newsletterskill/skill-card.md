## Description:

Newsletter Skill helps agents plan, review, implement, audit, or improve newsletter work across editorial calendars, issue structure, sponsorship inventory, reader growth, and retention loops.

This skill is ready for commercial/non-commercial use.

## Publisher:

[polnikale](https://clawhub.ai/user/polnikale)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and newsletter teams use this skill to produce issue outlines, editorial calendars, sponsor slot plans, reader survey syntheses, growth experiments, and retention audits with clear review gates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Newsletter advice could be applied directly to live email systems, including sends, contact imports, suppression changes, DNS/authentication changes, provider migrations, or production automation edits.

Mitigation: Require explicit human approval before live email-system changes and review generated plans before applying them.

Risk: Recommendations may be based on incomplete audience, consent, suppression, engagement, or sponsorship context.

Mitigation: State which source material supports each recommendation and do not assume missing fields, consent, or suppression state.

Risk: Sponsor placement or growth recommendations could weaken reader trust if they conflict with the publication promise.

Mitigation: Keep sponsor copy distinct from editorial copy and check that growth ideas match the audience and publication promise.

## Reference(s):

- [Newsletter Skill Operating Checklist](artifact/references/operating-checklist.md)
- [ClawHub Skill Page](https://clawhub.ai/polnikale/skills/newsletterskill)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown or structured text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include issue outlines, editorial calendars, sponsor slot plans, survey syntheses, growth experiments, retention audits, QA checks, and approval gates.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
