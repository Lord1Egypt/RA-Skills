## Description: <br>
Rewrites unclear or unhelpful error messages into clear, actionable text for users, logs, and APIs, auditing for common anti-patterns across all languages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PHY041](https://clawhub.ai/user/PHY041) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, API designers, UX writers, and support teams use this skill to audit confusing error messages and rewrite them for end-user UI text, API responses, and operational logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audit mode may expose unrelated private source code, secrets, or credentials if pointed at a broad directory. <br>
Mitigation: Point audit mode only at the smallest relevant folder and avoid including secrets, credentials, or unrelated private code. <br>
Risk: Generated rewrites may be unsuitable for a product's support, compliance, or security disclosure policy. <br>
Mitigation: Review rewritten UI, API, and log messages before deployment, especially messages involving security, payments, health, legal, or account access. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/PHY041/phy-error-writer) <br>
- [Publisher profile](https://clawhub.ai/user/PHY041) <br>
- [Canlah AI homepage](https://canlah.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Code, Guidance] <br>
**Output Format:** [Markdown with structured rewrite sections and optional JSON or code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces separate variants for user-facing messages, API response bodies, and log output.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
