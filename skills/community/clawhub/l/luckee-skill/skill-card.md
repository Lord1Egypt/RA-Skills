## Description:

Operate the Luckee AI e-commerce assistant through the luckee-tool OpenClaw plugin for Amazon seller advertising diagnosis, keyword research, competitor analysis, listing optimization, and reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xing89qs](https://clawhub.ai/user/xing89qs)

### License/Terms of Use:

MIT-0

## Use Case:

Amazon sellers and their supporting agents use this skill to install, configure, authenticate, and operate Luckee through OpenClaw. It supports ad diagnosis, ASIN and keyword research, competitor analysis, listing optimization, business data analysis, and structured reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence says the skill installs mutable third-party code.

Mitigation: Review and pin the GitHub plugin version and luckee-cli version, or disable automatic CLI installation and install reviewed packages manually before deployment.

Risk: Authentication tokens can be set through chat or configuration and are persisted across gateway restarts.

Mitigation: Prefer browser OAuth over sending live tokens in chat or command lines, use restricted OpenClaw service accounts, redact tokens in logs, and rotate any token that may have appeared in logs, chat history, or shell history.

## Reference(s):

- [Luckee Skill reference](artifact/reference.md)
- [Luckee OpenClaw plugin repository](https://github.com/motse-ai/luckee-openclaw-plugin.git)
- [ClawHub Luckee Skill page](https://clawhub.ai/xing89qs/skills/luckee-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce setup steps, troubleshooting guidance, token-handling instructions, and Luckee query results through OpenClaw when the plugin is available.]

## Skill Version(s):

0.1.2026210402 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
