## Description: <br>
Analyzes Jungle Scout Share of Voice data for Amazon keywords, including brand visibility across organic and sponsored results, 30-day search volume, PPC bid median, and top ASIN click and conversion metrics across supported marketplaces. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External e-commerce operators, marketplace analysts, and developers use this skill to assess Amazon keyword competition, brand dominance, sponsored versus organic visibility, PPC bid context, and top ASIN conversion performance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a LinkFox API key and sends Amazon keyword queries to the LinkFox tool gateway. <br>
Mitigation: Use an approved, scoped API key and avoid submitting confidential or sensitive keyword research unless LinkFox processing is acceptable. <br>
Risk: Automatic feedback reporting may send user intent or interaction details to a separate LinkFox feedback service. <br>
Mitigation: Use the skill only where that extra reporting is approved, or block feedback calls by policy before deployment. <br>


## Reference(s): <br>
- [Jungle Scout Share of Voice API Reference](references/api.md) <br>
- [LinkFox Jungle Scout Share of Voice API endpoint](https://tool-gateway.linkfox.com/tool-jungle-scout/keywords/share-of-voice) <br>
- [ClawHub skill release page](https://clawhub.ai/linkfox-ai/linkfox-junglescout-keyword-share-of-voice) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown analysis with tables, JSON examples, and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a LinkFox API key and analyzes one keyword per API call.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
