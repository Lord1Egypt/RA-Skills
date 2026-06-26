## Description: <br>
Navigate Orlando as visitor, resident, remote worker, or family with theme parks, neighborhoods, transit, costs, and local strategies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill for Orlando-specific travel, relocation, family, work, business, neighborhood, cost, transit, safety, and theme-park planning. The agent gives practical guidance, asks for key local constraints, and points users to official sources when exact current rules or prices matter. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional local memory may retain trip goals, neighborhood shortlists, commute constraints, school needs, or other personal planning context. <br>
Mitigation: Enable continuity only when useful, periodically review ~/orlando/memory.md, and avoid storing sensitive identifiers, payment details, ticket numbers, insurance IDs, or exact home addresses. <br>
Risk: Live verification can send travel dates, route context, ZIP, district, or filing type to public Orlando, Florida, park, transit, airport, or university websites. <br>
Mitigation: Use live lookups only for user-requested location-specific or date-specific guidance and limit the shared context to what is needed for that lookup. <br>
Risk: Park prices, line-skip rules, parking fees, toll policies, school boundaries, immigration requirements, and business filing rules can change. <br>
Mitigation: Treat stored guidance as planning context and verify exact current requirements with official sources before the user makes bookings, filings, or move decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/orlando) <br>
- [Skill homepage](https://clawic.com/skills/orlando) <br>
- [Visit Orlando](https://www.visitorlando.com) <br>
- [City of Orlando](https://www.orlando.gov) <br>
- [LYNX](https://www.golynx.com) <br>
- [SunRail](https://sunrail.com) <br>
- [Walt Disney World](https://disneyworld.disney.go.com) <br>
- [Universal Orlando](https://www.universalorlando.com) <br>
- [SeaWorld Orlando](https://seaworld.com/orlando) <br>
- [Florida Sunbiz](https://www.sunbiz.org) <br>
- [University of Central Florida](https://www.ucf.edu) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with occasional inline shell commands and local memory templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May optionally use local continuity files under ~/orlando/ when the user agrees.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
