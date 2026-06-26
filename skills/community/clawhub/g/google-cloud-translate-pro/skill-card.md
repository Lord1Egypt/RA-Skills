## Description: <br>
Translate text across 195 languages using Google Cloud Translation API with zero-config setup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[q2408808](https://clawhub.ai/user/q2408808) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to translate text, detect source languages, bulk-translate short text lists, and list supported language codes from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release is marketed as Google Cloud Translate while security evidence says text and API credentials route to SocketsIO. <br>
Mitigation: Treat it as a SocketsIO-backed remote translation tool, use a dedicated API key and unique password, review SocketsIO privacy and pricing terms, and avoid sending secrets, regulated data, or confidential business text unless SocketsIO is approved for the use case. <br>


## Reference(s): <br>
- [Supported Language Codes](references/language-codes.md) <br>
- [SocketsIO API Docs](https://socketsio.com/docs) <br>
- [SocketsIO Dashboard](https://socketsio.com/dashboard) <br>
- [SocketsIO Pricing](https://socketsio.com/pricing) <br>
- [ClawHub Skill Page](https://clawhub.ai/q2408808/google-cloud-translate-pro) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, guidance] <br>
**Output Format:** [Plain text or JSON responses from CLI and HTTP API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SOCKETSIO_API_KEY; uses network requests to SocketsIO translation endpoints.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
