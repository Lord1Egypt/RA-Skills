## Description: <br>
Shopping assistant that helps agents search Luogang products, retrieve product details, and present purchase links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fireium](https://clawhub.ai/user/fireium) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External shoppers and shopping-support agents use this skill to search Luogang commerce listings, compare basic product details, and hand off users to H5 or mini-program purchase pages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Shopping queries may include unrelated personal information if users provide it while searching. <br>
Mitigation: Avoid sending unnecessary personal information to the product lookup service. <br>
Risk: Purchase links open external H5 or mini-program pages outside the chat flow. <br>
Mitigation: Review the destination page before buying and do not treat the skill as having order or payment authority. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fireium/luogang-shopping-assistant) <br>
- [Luogang MCP service endpoint](https://yuju-mcp.wxhoutai.com/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline JSON and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Product result summaries should stay concise and include detail or purchase links when available.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
