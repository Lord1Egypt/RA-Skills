## Description:

Guides agents through public-source supply-chain checks for imported products, including GACC status, foreign and domestic business records, certifications, anti-counterfeit trace pages, and evidence-based consumer recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pisces33](https://clawhub.ai/user/pisces33)

### License/Terms of Use:

MIT-0

## Use Case:

Consumers, investigators, and support agents use this skill to evaluate whether an imported product appears properly sourced, licensed, and represented. It produces a structured due-diligence report with confidence levels, evidence gaps, risk conclusions, and practical next steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may retain sensitive product photos, receipts, payment records, addresses, account details, and screenshots in local evidence packages.

Mitigation: Collect only the evidence needed for the investigation, redact personal and payment information before saving or sharing, and delete evidence packages after the case is finished.

Risk: The skill text suggests using curl or direct-IP checks when QR-code or trace-platform pages are blocked by browser protections.

Mitigation: Do not bypass blocked destinations; keep browser and network protections in place and avoid direct-IP or curl checks for QR-code links.

Risk: Public registry and trace-platform results can be incomplete, self-reported, or time-sensitive, which may lead to overstated conclusions.

Mitigation: Timestamp the report, separate independent official evidence from merchant-controlled claims, state confidence levels, and identify unresolved evidence gaps.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pisces33/skills/import-product-investigator)
- [National Enterprise Credit Information Publicity System](https://www.gsxt.gov.cn/)
- [GACC Cifer Query](https://ciferquery.singlewindow.cn/)
- [SAMR Special Food Information Query](https://bjzx.samr.gov.cn/sscxquery/)
- [NMPA Data Query](https://www.nmpa.gov.cn/)
- [CNCA Certification Query](https://www.cnca.gov.cn/)
- [MIIT Telecom Business Market Management System](https://dxzhgl.miit.gov.cn/)
- [Corporations Canada](https://ised-isde.canada.ca/cc/lgcy/fdrlCrpSrch.html)
- [New Zealand Companies Office](https://www.companiesoffice.govt.nz/)
- [Australian Business Register](https://abr.business.gov.au/)
- [SEC EDGAR](https://www.sec.gov/edgar/search/)
- [Companies House](https://find-and-update.company-information.service.gov.uk/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown investigative report with tables, risk labels, recommendations, and optional evidence-package file instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include confidence bands, timestamped source notes, screenshot/evidence-package guidance, and consumer action recommendations]

## Skill Version(s):

1.1.5 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
