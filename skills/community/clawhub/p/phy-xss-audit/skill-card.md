## Description: <br>
Cross-Site Scripting (XSS) static vulnerability scanner (OWASP A03:2021). Detects reflected, stored, and DOM-based XSS in JavaScript/TypeScript, React, Vue, Angular, Python/Django/Jinja2, PHP, Ruby/ERB, and Go html/template. Zero external dependencies - pure Python stdlib only. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PHY041](https://clawhub.ai/user/PHY041) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security engineers use this skill to scan local source files or repositories for XSS patterns and review findings with suggested fixes before release or in CI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scanner runs locally over source code and its findings may include snippets from private files. <br>
Mitigation: Run it only on repositories or files you intend to inspect, and review or redact output before sharing it outside the trusted project team. <br>
Risk: Static XSS pattern matching can produce false positives or miss vulnerabilities outside the documented checks. <br>
Mitigation: Treat findings as review prompts, confirm them against the affected code path, and use complementary security review for release decisions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/PHY041/phy-xss-audit) <br>
- [Canlah AI Homepage](https://canlah.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, guidance] <br>
**Output Format:** [Plain text reports, JSON findings, or GitHub Actions annotations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [CI mode can exit nonzero on critical or high findings; findings may include source snippets and suggested fixes.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
