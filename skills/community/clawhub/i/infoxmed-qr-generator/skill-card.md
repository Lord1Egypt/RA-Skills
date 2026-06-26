## Description: <br>
Generates Infoxmed VIP membership activation QR-code batches from natural-language requests, confirms the extracted parameters, and downloads the resulting zip file. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yaochao](https://clawhub.ai/user/yaochao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users with authorization to generate Infoxmed VIP activation QR codes use this skill to parse hospital, business-channel, card-type, and scan-count details before making the Infoxmed batch generation request. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an Infoxmed API password and may otherwise guide users toward persistent local shell-profile storage. <br>
Mitigation: Configure the password through a secure secret store, avoid echoing or persisting it in shell profiles, and only install the skill for authorized Infoxmed QR-code generation. <br>
Risk: Incorrect extracted hospital, business-channel, card-type, or scan-count parameters could generate incorrect activation QR codes. <br>
Mitigation: Review and confirm all extracted parameters before allowing the API request to run. <br>


## Reference(s): <br>
- [Infoxmed Qr Generator on ClawHub](https://clawhub.ai/yaochao/infoxmed-qr-generator) <br>
- [Infoxmed VIP QR batch generation endpoint](https://api.infox-med.com/system/batchGenerateVipQr) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls, files, guidance] <br>
**Output Format:** [Markdown with inline shell commands and a downloaded zip file path] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a local zip file containing generated QR codes after user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
