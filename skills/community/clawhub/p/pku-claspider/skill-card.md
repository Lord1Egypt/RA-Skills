## Description:

PKU Claspider helps agents use a CLI scraper to collect and merge Peking University course catalog data from dean, elective, and Zhiyun sources into JSON exports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wjsoj](https://clawhub.ai/user/wjsoj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and PKU course-data users use this skill when they need an agent to run or explain claspider commands for bulk course catalog scraping, filtering, and merging. It is for read-only catalog data collection, not course enrollment changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated PKU sources may require reused login sessions or a browser JWT token.

Mitigation: Do not paste real JWTs into chat, logs, shared terminals, or shell history; prefer safer credential mechanisms when available and treat reused session directories as sensitive account material.

Risk: The skill is intended for read-only course information gathering, but authenticated source access still touches university account context.

Mitigation: Review commands before execution and use the skill only for catalog scraping and merging, not course selection, dropping, or other account-changing actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wjsoj/skills/pku-claspider)
- [PKU Dean course schedule source](https://dean.pku.edu.cn)
- [PKU elective course source](https://elective.pku.edu.cn)
- [PKU Zhiyun classroom source](https://onlineroomse.pku.edu.cn)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON-oriented guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide JSON exports from the claspider CLI; authenticated sources require careful handling of session material and JWT tokens.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
