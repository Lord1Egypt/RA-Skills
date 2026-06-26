## Description: <br>
Provides a unified JisuAPI gateway that lets an agent use one JISU_API_KEY to call supported data APIs such as weather, gold, stock, express, OCR, and exchange-rate endpoints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jisuapi](https://clawhub.ai/user/jisuapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill as a single structured-data gateway for JisuAPI services, listing supported endpoints and calling an opened API with JSON parameters. It is suited for workflows that need one configured key for data such as weather, market prices, recipes, express tracking, OCR, barcode data, identifiers, and location lookups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Some optional JisuAPI calls can send sensitive identifiers, document images, phone numbers, bank cards, VINs, courier numbers, QR or barcode images, or location data to JisuAPI. <br>
Mitigation: Confirm before sending sensitive data, install only when JisuAPI is trusted for the intended data, and review JisuAPI billing and data-handling terms. <br>
Risk: The skill uses a JISU_API_KEY for requests to JisuAPI, so usage may expose billed API access if the key is mishandled. <br>
Mitigation: Keep JISU_API_KEY in the environment, avoid sharing it in prompts or logs, and rotate the key if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jisuapi/jisu) <br>
- [JisuAPI documentation](https://www.jisuapi.com/) <br>
- [JisuAPI API base URL](https://api.jisuapi.com) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [JSON responses from the helper script, with Markdown usage guidance and inline shell commands in the skill documentation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and JISU_API_KEY; call requests accept an api path and optional params object.] <br>

## Skill Version(s): <br>
1.0.10 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
