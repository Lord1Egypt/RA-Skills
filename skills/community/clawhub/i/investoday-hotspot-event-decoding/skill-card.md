## Description: <br>
Generates structured market hot-spot event decoding reports for themes, sectors, and industry events using public news and research sentiment from the Investoday finance data dependency. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kenneth-bro](https://clawhub.ai/user/kenneth-bro) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and finance research agents use this skill to understand recent theme, sector, or industry catalysts, the related logic chain, opportunity and risk directions, and follow-up validation points. It is intended for research context and not for individual stock recommendations or investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Market event summaries can be time-sensitive or incomplete and may be mistaken for investment advice. <br>
Mitigation: Treat outputs as research context, verify cited public source data before acting, and preserve the non-investment-advice risk notice. <br>
Risk: The skill depends on investoday-finance-data for public market data. <br>
Mitigation: Use the skill only when that dependency is trusted and configured for approved data access. <br>
Risk: Users could include private or non-public financial information in prompts. <br>
Mitigation: Keep prompts to public theme, sector, or industry topics and avoid entering private or non-public financial information. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kenneth-bro/investoday-hotspot-event-decoding) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/kenneth-bro) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown structured market event report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes core events, event interpretation, opportunity and risk directions, follow-up watch points, cited source titles, and a non-investment-advice risk notice.] <br>

## Skill Version(s): <br>
1.3.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
