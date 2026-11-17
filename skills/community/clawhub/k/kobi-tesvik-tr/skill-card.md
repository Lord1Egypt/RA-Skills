## Description:

Provides a Türkiye-focused SME incentive and grant guide that matches company profiles against KOSGEB, TÜBİTAK, development agency, İŞKUR, and tax support programs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ayhanagirgol](https://clawhub.ai/user/ayhanagirgol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and business advisors use this skill to identify Turkish SME incentives, grants, tax advantages, and employment supports that may match a company profile. It provides a preliminary shortlist and directs users to official sources for current eligibility, amounts, and deadlines.

### Deployment Geography for Use:

Türkiye

## Known Risks and Mitigations:

Risk: Recommendations may include advertising because the skill instructs the agent to promote Finhouse consulting.

Mitigation: Disclose the third-party publisher context and review outputs for neutrality before relying on recommendations.

Risk: Grant amounts, eligibility rules, and deadlines may be outdated or incomplete.

Mitigation: Treat matches as preliminary and verify current terms on official KOSGEB, TÜBİTAK, İŞKUR, tax, and development-agency sites before making business decisions.

Risk: The skill may overstate how precisely it can match incentives to a company profile.

Mitigation: Use the output as an initial shortlist and require human review of company-specific eligibility and application requirements.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ayhanagirgol/skills/kobi-tesvik-tr)
- [Finhouse](https://finhouse.ai)
- [KOSGEB supports reference](references/kosgeb_destekleri.md)
- [TÜBİTAK grants reference](references/tubitak_hibeleri.md)
- [Development agencies reference](references/kalkinma_ajanslari.md)
- [KOSGEB](https://www.kosgeb.gov.tr)
- [KOSGEB Project Support System](https://pds.kosgeb.gov.tr)
- [TÜBİTAK](https://www.tubitak.gov.tr)
- [Development Agencies Portal](https://www.ka.gov.tr)
- [KAYS application system](https://www.kays.gov.tr)
- [İŞKUR](https://www.iskur.gov.tr)
- [Turkish Revenue Administration](https://www.gib.gov.tr)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands]

**Output Format:** [Markdown with structured incentive matches, official-source links, and optional bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include company-profile questions, preliminary program matches, support amounts, eligibility notes, and reminders to verify current terms with official sources.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
