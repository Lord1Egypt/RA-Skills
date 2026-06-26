## Description: <br>
Use when the user wants to call, test, or integrate the HTMLPix HTML-to-image API, including auth setup, signed URL minting, image rendering, template CRUD, and AI template generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jymaa](https://clawhub.ai/user/jymaa) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to generate integration guidance, curl examples, SDK wrappers, and troubleshooting steps for the HTMLPix HTML-to-image API. It supports backend API-key handling, signed image URL minting, template management, and AI-assisted template generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API keys could be exposed if private HTMLPix endpoints are called from browser client code. <br>
Mitigation: Keep HTMLPix API keys server-side or in secret-managed environments and mint signed image URLs from backend code. <br>
Risk: Template create/update requests and AI-generated templates may introduce unexpected rendering behavior or incorrect output. <br>
Mitigation: Review template code and generated template results before deploying or using them in production workflows. <br>
Risk: Generated image URLs and submitted template variables are data shared with a third-party service. <br>
Mitigation: Treat signed URLs as opaque, avoid mutating their query parameters, and avoid sending sensitive data unless approved for the integration. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jymaa/htmlpix) <br>
- [HTMLPix API Base URL](https://api.htmlpix.com) <br>
- [HTMLPix API Key Management](https://htmlpix.com/api-keys) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline JSON, curl, and code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include API request bodies, endpoint constraints, authentication notes, and error-handling guidance.] <br>

## Skill Version(s): <br>
0.1.3 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
