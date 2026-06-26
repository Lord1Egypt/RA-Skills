## Description: <br>
Build a courier station AI chat system with Express, GPT-5.5, local JSON DB, OCR, and WeChat-style frontend. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jeremycooper2077](https://clawhub.ai/user/jeremycooper2077) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and station operators use this skill to generate a courier-station chatbot template for package lookup, OCR-assisted waybill recognition, chat responses, and package management workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The generated template handles shipment personal data and chat history. <br>
Mitigation: Minimize personal data sent to the AI provider, document consent and privacy handling, and define retention and deletion rules before real station use. <br>
Risk: Package management and listing features may be exposed without documented access controls. <br>
Mitigation: Add authentication and authorization for admin and package APIs, and avoid exposing management endpoints publicly. <br>
Risk: The skill requires a sensitive API credential for AI calls. <br>
Mitigation: Store SU2_API_KEY outside source-controlled files and restrict runtime access to the deployment environment that needs it. <br>


## Reference(s): <br>
- [Parcel Station Chat on ClawHub](https://clawhub.ai/jeremycooper2077/parcel-station-chat) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline code blocks and API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes guidance for Express routes, local JSON storage, OCR handling, chat behavior, and frontend setup.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
