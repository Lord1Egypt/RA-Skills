## Description: <br>
Retrieves translated patent description/specification text from the Eureka patent data platform for Chinese, English, or Japanese output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to fetch translated patent description text by patent ID or publication number, including batch requests and optional family-member substitution when the original description is unavailable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a LinkFox API key and sends patent identifiers or query context to LinkFox's tool gateway. <br>
Mitigation: Install only if you trust LinkFox with the API key and patent queries; use a scoped key and avoid sensitive patent material unless approved. <br>
Risk: The artifact describes separate feedback reporting that may send user interaction details, including possible patent context, to a LinkFox feedback endpoint. <br>
Mitigation: Disable or strictly control feedback behavior unless users explicitly expect this reporting and the data sharing is approved. <br>


## Reference(s): <br>
- [Eureka API Reference](references/api.md) <br>
- [Eureka description translation API](https://tool-gateway.linkfox.com/eureka/descriptionDataTranslated) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with API parameters, shell examples, and returned translated patent text or JSON results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LINKFOXAGENT_API_KEY; accepts patentId or patentNumber, lang, and replaceByRelated; supports up to 100 patent identifiers per request.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
