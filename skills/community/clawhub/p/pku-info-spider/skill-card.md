## Description:

WeChat Official Account article crawler CLI tool for working on the Rust info-spider crate, including WeChat QR login, account search, article fetching, and article-to-Markdown conversion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wjsoj](https://clawhub.ai/user/wjsoj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when maintaining or debugging the info-spider CLI, especially workflows for authenticated WeChat MP access, Official Account search, article retrieval, and Markdown scraping.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated WeChat scraping may access content or accounts without adequate authorization boundaries.

Mitigation: Use the skill only for accounts and content the operator is authorized to access, and document those boundaries before use.

Risk: Stored session artifacts such as tokens, fingerprints, and account identifiers can expose authenticated access if mishandled.

Mitigation: Protect local session files as credentials, avoid sharing them, and clear sessions when access is no longer needed.

Risk: Anti-crawler delay and bypass guidance can encourage platform-control evasion.

Mitigation: Apply explicit request limits, follow applicable platform terms, and avoid workflows intended to bypass access controls.

## Reference(s):

- [PKU Info Spider on ClawHub](https://clawhub.ai/wjsoj/skills/pku-info-spider)
- [wjsoj ClawHub profile](https://clawhub.ai/user/wjsoj)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, configuration]

**Output Format:** [Markdown with inline code and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Chinese user-facing strings, JSON or JSONL output guidance, and Markdown conversion guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
