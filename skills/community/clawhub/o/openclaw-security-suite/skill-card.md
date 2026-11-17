## Description:

Comprehensive security suite for OpenClaw skills. Includes static scanning (AST + keywords) and AI-powered semantic behavior review to detect malicious code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xunxingyuan](https://clawhub.ai/user/xunxingyuan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security reviewers use this skill to scan OpenClaw skill directories and review individual source files for suspicious imports, dangerous calls, keyword matches, and LLM-identified malicious behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The review action can read a local file path and send the full contents to the active LLM context.

Mitigation: Use the review action only on files intentionally approved for LLM processing, and avoid secrets, credentials, private agent state, and broad filesystem paths.

Risk: Scan and review results are advisory because advertised security layers are not all enforced and scanner coverage is incomplete.

Mitigation: Treat a clean result as one input to review rather than an authorization to deploy; pair it with human review and additional security checks.

## Reference(s):

- [OpenClaw Security README](README.md)
- [OpenClaw Security Suite Skill Definition](SKILL.md)
- [Security Policy Configuration](config/policy.json)
- [Malicious Pattern Configuration](config/malicious_patterns.json)

## Skill Output:

**Output Type(s):** [text, json, guidance]

**Output Format:** [JSON scan results or LLM-generated review text with JSON fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scan results include a safe flag and per-file issues; review results include risk_level and reason when the LLM follows the prompt.]

## Skill Version(s):

0.2.3 (source: SKILL.md frontmatter, package.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
