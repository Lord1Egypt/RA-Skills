## Description: <br>
HTTP client and server misconfiguration detector that detects insecure connections, missing timeouts, cookie security issues, caching misconfigurations, and request handling vulnerabilities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[suhteevah](https://clawhub.ai/user/suhteevah) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use HTTPLint to scan projects for HTTP client and server configuration risks, review findings, and generate text, JSON, or HTML reports for local or CI workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: License handling can run code from a crafted license token. <br>
Mitigation: Use only license keys from trusted sources and do not paste or store license keys from untrusted sources. <br>
Risk: The optional hook installer changes repository automation and can add recurring commit and push scans. <br>
Mitigation: Run hook installation only in repositories where recurring scans and lefthook.yml changes are acceptable. <br>
Risk: Local scans inspect project files selected by the user. <br>
Mitigation: Use scans only on projects you intend to inspect and review the skill before installation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/suhteevah/httplint) <br>
- [HTTPLint homepage](https://httplint.pages.dev) <br>
- [HTTPLint hooks documentation](https://httplint.pages.dev/docs/hooks) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, html, shell commands, configuration] <br>
**Output Format:** [CLI output and reports in text, JSON, HTML, or markdown-oriented remediation guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Free scans cover 30 patterns; licensed tiers expand coverage to 60 or 90 patterns.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
