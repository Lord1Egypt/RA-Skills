## Description: <br>
Server-Side Request Forgery (SSRF) vulnerability scanner (OWASP A10:2021) that detects URL-fetching sinks in Python, Java, Node.js, PHP, Go, and Ruby, flags cloud metadata endpoint access, and reports CWE-918 findings with fix guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PHY041](https://clawhub.ai/user/PHY041) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security engineers use this skill to scan authorized codebases for SSRF-prone URL fetches, cloud metadata endpoint access, missing allowlist checks, and related CWE-918 remediation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local source trees to audit SSRF patterns. <br>
Mitigation: Run it only against codebases you are authorized to inspect and handle reported findings according to the repository owner's security process. <br>
Risk: Static SSRF findings can be false positives or lack full runtime context. <br>
Mitigation: Review each reported CWE-918 finding before making code changes or enforcing CI gates. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/PHY041/phy-ssrf-audit) <br>
- [Canlah AI homepage](https://canlah.ai) <br>
- [OWASP Top 10 A10:2021 Server-Side Request Forgery](https://owasp.org/Top10/A10_2021-Server-Side_Request_Forgery_%28SSRF%29/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with embedded Python scanner code, shell commands, and optional JSON scanner output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The scanner reports severity, file path, line number, CWE-918 context, taint and metadata-endpoint indicators, and fix snippets.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
