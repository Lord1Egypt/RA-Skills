## Description: <br>
Scan any public web page for GDPR, CCPA/CPRA, and ePrivacy privacy and cookie-consent signals, with clear limits on what static HTML testing can detect. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[foomworks](https://clawhub.ai/user/foomworks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, site owners, and compliance reviewers use Privacy Scan to inspect public web pages for observable privacy and cookie-consent risk signals before launch or review. It helps identify tracker, consent-tooling, privacy-policy, Do-Not-Sell, cookie-attribute, HTTPS, and mixed-content signals, but it does not determine legal compliance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: URLs submitted for scanning are handled by a third-party hosted service. <br>
Mitigation: Use the skill for public pages and avoid submitting private, sensitive, or internal URLs. <br>
Risk: Static HTML scanning cannot determine whether trackers fire before consent or prove legal compliance. <br>
Mitigation: Treat results as risk signals, use browser-based testing for consent-timing questions, and obtain qualified compliance review where needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/foomworks/skills/privacy-scan) <br>
- [Privacy Scan Service](https://privacy-scan.foomworks.workers.dev) <br>
- [Privacy Scan MCP Endpoint](https://privacy-scan.foomworks.workers.dev/mcp) <br>
- [Privacy Scan OpenAPI Manifest](https://privacy-scan.foomworks.workers.dev/openapi.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance, shell commands] <br>
**Output Format:** [Markdown or text summaries of scanner findings, with optional curl commands and JSON responses from the remote service] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results are static-HTML risk signals and should not be treated as legal compliance determinations.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
