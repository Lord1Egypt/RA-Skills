## Description:

Navigate New York State for living, moving, working, and visiting with region fit, taxes, winter risk, and daily logistics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to get practical New York State guidance for visiting, relocating, living, or operating a business, with answers adjusted for region, commute, taxes, housing, weather, schools, healthcare, and local workflow differences.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional plaintext memory in ~/new-york/ may contain sensitive personal context if the user saves more detail than needed.

Mitigation: Ask before creating or updating memory, keep saved context coarse, avoid credentials, SSNs, payment details, account numbers, immigration details, medical specifics, and full street addresses, and tell users they can review or delete memory.md.

Risk: Location-specific guidance can require ZIP, county, district, or address-level details that may be sent to official state or local portals.

Mitigation: Use the coarsest location that answers the question, disclose when a lookup needs more precise location data, and prefer official portals for current rules.

Risk: DMV, tax, health insurance, school, utility, and local compliance steps can change over time or vary by municipality.

Mitigation: Verify precise compliance steps against current official state, county, district, utility, or municipal sources before relying on deadlines, forms, eligibility, or fees.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/new-york)
- [New York State services](https://www.ny.gov/)
- [New York DMV driver licenses](https://dmv.ny.gov/driver-license)
- [New York DMV vehicle services](https://dmv.ny.gov/vehicles)
- [New York Department of Taxation and Finance](https://www.tax.ny.gov/)
- [New York State of Health](https://nystateofhealth.ny.gov/)
- [New York Department of Financial Services consumers](https://www.dfs.ny.gov/consumers)
- [New York Business Express](https://www.businessexpress.ny.gov/)
- [New York Department of State corporations and business entities](https://dos.ny.gov/corporations-and-business-entities)
- [New York preparedness resources](https://www.dhses.ny.gov/prepare)
- [New York State Education Department](https://www.nysed.gov/)
- [New York State Parks](https://parks.ny.gov/)
- [I LOVE NY official travel portal](https://www.iloveny.com/)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with practical checklists, tradeoff analysis, official-source pointers, and optional shell or file guidance for local memory setup.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update optional plaintext memory at ~/new-york/memory.md only after user confirmation.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
