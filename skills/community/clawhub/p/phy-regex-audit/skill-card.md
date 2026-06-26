## Description: <br>
Regex Audit helps agents scan source files for ReDoS risks and regex quality issues, then report severity-ranked findings with locations and suggested fixes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PHY041](https://clawhub.ai/user/PHY041) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security engineers use this skill to audit application source code for regex denial-of-service patterns, unsafe validators, missing anchors, locale assumptions, and related regex quality issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad scans may include unrelated secrets, private material, or sensitive source context in the generated report. <br>
Mitigation: Run the skill on explicit files or source directories and avoid directories that contain unrelated secrets or private material. <br>
Risk: Static regex analysis can produce false positives or miss context-specific behavior. <br>
Mitigation: Review findings and test suggested regex rewrites before applying them in production code. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/PHY041/phy-regex-audit) <br>
- [Canlah AI homepage](https://canlah.ai) <br>
- [OWASP ReDoS reference](https://owasp.org/www-community/attacks/ReDoS) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown report with code snippets; optional JSON for CI-oriented output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Severity-ranked regex findings with file, line, context, attack examples, and fix suggestions.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
