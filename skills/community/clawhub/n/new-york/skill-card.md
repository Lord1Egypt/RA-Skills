## Description: <br>
Navigate New York State for living, moving, working, and visiting with region fit, taxes, winter risk, and daily logistics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill for New York State resident, relocation, travel, and business guidance where region, county, transit, taxes, weather, schools, insurance, or agency workflows materially change the answer. <br>

### Deployment Geography for Use: <br>
United States, focused on New York State <br>

## Known Risks and Mitigations: <br>
Risk: Optional local memory may retain sensitive personal, location, family, health, vehicle, housing, or timeline context if the user chooses to save it. <br>
Mitigation: Enable memory only when continuity is useful, review ~/new-york/memory.md, and avoid storing full addresses, IDs, credentials, immigration details, payment information, or other sensitive records. <br>
Risk: Precise DMV, tax, health-plan, school, utility, housing, weather, and local-agency guidance can become outdated or vary by county, district, utility, or municipality. <br>
Mitigation: Verify current and address-specific details against official state or local sources before giving compliance steps or deadline-sensitive guidance. <br>
Risk: Location-specific lookups may disclose ZIP, county, district, or region context to official New York or local-government websites. <br>
Mitigation: Send location details only when the user asks for location-specific guidance and the lookup is necessary for the answer. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/new-york) <br>
- [Skill homepage](https://clawic.com/skills/new-york) <br>
- [Official sources map](artifact/sources.md) <br>
- [New York State services](https://www.ny.gov/) <br>
- [New York DMV](https://dmv.ny.gov/) <br>
- [New York Department of Taxation and Finance](https://www.tax.ny.gov/) <br>
- [NY State of Health](https://nystateofhealth.ny.gov/) <br>
- [New York Department of Financial Services](https://www.dfs.ny.gov/) <br>
- [New York State Education Department](https://www.nysed.gov/) <br>
- [New York Business Express](https://www.businessexpress.ny.gov/) <br>
- [New York State preparedness resources](https://www.dhses.ny.gov/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Configuration] <br>
**Output Format:** [Markdown and plain-language guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose optional local memory in ~/new-york/ only after user confirmation.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
