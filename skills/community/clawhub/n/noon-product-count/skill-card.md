## Description:

Noon 商品数量统计工具。输入阿拉伯语关键词，在 noon.com 沙特站搜索，返回搜索结果的商品数量。

This skill is ready for commercial/non-commercial use.

## Publisher:

[freemanwangfuhan-coder](https://clawhub.ai/user/freemanwangfuhan-coder)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to search Noon Saudi Arabia with Arabic keywords and report the product count for each keyword.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automates a third-party commerce site and uses stealth browser automation, which may trigger bot-detection, blocking, or terms-of-service concerns.

Mitigation: Review authorization and Noon usage terms before running, and only use it where this automation is allowed.

Risk: The documented dependency installation uses unpinned npm packages.

Mitigation: Install dependencies in a sandbox or pinned lockfile-based environment before use.

Risk: The security review verdict is suspicious because the skill claims CAPTCHA bypass without enough user-facing caution.

Mitigation: Review the skill before installing and avoid using CAPTCHA bypass behavior unless explicitly permitted.

## Reference(s):

- [Noon Saudi Arabia](https://www.noon.com/saudi-ar/)
- [ClawHub skill page](https://clawhub.ai/freemanwangfuhan-coder/skills/noon-product-count)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Command-line text output with product counts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns one count or error string per Arabic keyword.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
