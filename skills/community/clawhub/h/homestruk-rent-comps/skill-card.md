## Description: <br>
Analyzes rental comps and recommends competitive rent pricing for Massachusetts properties using comparable listings and property features. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AdamsJB](https://clawhub.ai/user/AdamsJB) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External landlords and property managers use this skill to analyze Massachusetts rental comps for lease renewals, vacancies, acquisition underwriting, and tenant rent inquiries. <br>

### Deployment Geography for Use: <br>
Massachusetts, United States <br>

## Known Risks and Mitigations: <br>
Risk: The skill may read property details from ~/.openclaw/shared/properties.json, which can include addresses, rents, and property context. <br>
Mitigation: Review the property file before use and provide only information appropriate for the rent-pricing analysis. <br>
Risk: Generated reports may store addresses, rents, and analysis locally under ~/.openclaw/workspace/properties. <br>
Mitigation: Handle generated reports according to the user's property-data retention and sharing requirements. <br>
Risk: Rent recommendations can be affected by incomplete comparable listings or outdated local-market information. <br>
Mitigation: Review the comparable listings, adjustment assumptions, and Massachusetts rent-increase notes before relying on the recommendation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AdamsJB/homestruk-rent-comps) <br>
- [Publisher profile](https://clawhub.ai/user/AdamsJB) <br>
- [Homestruk](https://homestruk.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown rent-comps report with structured property, comparable-listing, analysis, and recommendation sections.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include web_search query suggestions and a saved local Markdown report under ~/.openclaw/workspace/properties.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
