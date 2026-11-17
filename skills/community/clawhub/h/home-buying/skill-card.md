## Description:

Buy a home with budget guardrails, listing scorecards, offer strategy, due diligence triage, and closing readiness checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

External users buying a primary home or investment property use this skill to keep budgeting, property comparison, offer strategy, due diligence, and closing readiness decisions disciplined and documented.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can maintain persistent local home-buying memory at ~/home-buying/.

Mitigation: Confirm the user's desired activation mode before setup and avoid storing full identity documents, account numbers, lender portal credentials, or other unnecessary sensitive details.

Risk: Home-buying recommendations may influence significant financial and contractual decisions.

Mitigation: Treat outputs as decision support, keep walk-away thresholds explicit, and require user review before offers, contingency removals, financing commitments, or closing decisions.

## Reference(s):

- [ClawHub Home Buying Skill Page](https://clawhub.ai/ivangdavila/skills/home-buying)
- [Home Buying Homepage](https://clawic.com/skills/home-buying)
- [Setup](setup.md)
- [Budget Guardrails](budget-guardrails.md)
- [Listing Scorecard](listing-scorecard.md)
- [Offer Ladder](offer-ladder.md)
- [Due Diligence](due-diligence.md)
- [Closing Readiness](closing-readiness.md)
- [Memory Template](memory-template.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Configuration, Files]

**Output Format:** [Markdown guidance, checklists, scorecards, and local note templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create and update scoped local memory under ~/home-buying/ after user confirmation.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
