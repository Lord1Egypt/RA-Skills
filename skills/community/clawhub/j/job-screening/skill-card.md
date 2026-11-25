## Description:

Screens one employer's campus recruiting and new-grad openings, recommends the strongest-fit roles, and explains exclusions using résumé-visible evidence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ekko237](https://clawhub.ai/user/ekko237)

### License/Terms of Use:

MIT

## Use Case:

Students and new graduates use this skill to screen one employer's openings against their profile and résumé, rank eligible roles, and understand why other roles were excluded.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install instructions include an unpinned CLI command, which can change over time and create supply-chain risk.

Mitigation: Review the install source and use a reviewed, pinned version when available, as the security guidance recommends.

Risk: Résumé text shared during screening is sent to the AI model or service configured for the agent session.

Mitigation: Leave out résumé details you are not willing to share with that provider.

## Reference(s):

- [README](README.md)
- [First-use onboarding](references/onboarding.md)
- [Opportunity scan](references/opportunity-scan.md)
- [ClawHub listing](https://clawhub.ai/ekko237/skills/job-screening)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Markdown]

**Output Format:** [Markdown with a ranked role shortlist, résumé-based rationale, risks, and screening exclusions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tailored to the candidate profile and the supplied openings; explains each screened-out role.]

## Skill Version(s):

1.0.3 (source: frontmatter, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
