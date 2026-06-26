## Description: <br>
Security scanner for Moltbot skills. Scan GitHub repositories for vulnerabilities before installation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[moltcheck](https://clawhub.ai/user/moltcheck) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to scan GitHub repositories and Moltbot skills for security risks before installing or relying on them. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scanned GitHub repository URLs are sent to moltcheck.com for API-backed analysis. <br>
Mitigation: Install only if sharing those repository URLs with the MoltCheck service is acceptable. <br>
Risk: The skill can use a MoltCheck API key and setup output includes payment details. <br>
Mitigation: Use a MoltCheck-specific API key, keep setup output private, and verify payment wallet or credit-purchase details through the official MoltCheck site before sending funds. <br>


## Reference(s): <br>
- [MoltCheck Website](https://moltcheck.com) <br>
- [MoltCheck API Documentation](https://moltcheck.com/api-docs.md) <br>
- [MoltCheck OpenAPI Specification](https://moltcheck.com/openapi.json) <br>
- [ClawHub Skill Page](https://clawhub.ai/moltcheck/moltcheck) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, markdown, configuration, guidance] <br>
**Output Format:** [JSON responses with scan summaries, scores, grades, risk details, credit information, and setup guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scan results may include report URLs, undeclared permissions, and remaining credit counts when returned by the MoltCheck API.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
