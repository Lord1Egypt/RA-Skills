## Description: <br>
Automates OK.com marketplace workflows for searching listings, browsing categories, viewing listing details, managing favorites, managing posted ads, and switching locales across supported countries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[winterw](https://clawhub.ai/user/winterw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to search OK.com classifieds, compare listings, fetch listing details, switch country or city context, and manage account favorites or posted ads when authenticated. <br>

### Deployment Geography for Use: <br>
Singapore, USA, Canada, Japan, UAE, Australia, UK, Hong Kong, Malaysia, and New Zealand. <br>

## Known Risks and Mitigations: <br>
Risk: The skill can exercise broad control over OK.com browser sessions, including authenticated account actions. <br>
Mitigation: Install only when that control is acceptable, use an isolated browser profile or dedicated session, and review account-changing actions before execution. <br>
Risk: Credential and login flows may expose sensitive account access through browser automation or command-line password entry. <br>
Mitigation: Prefer manual OAuth login, avoid passing passwords on the command line, and do not use unrelated normal browser profiles or unrelated CDP sessions. <br>
Risk: The extension and persistent profile behavior can retain access beyond a single command run. <br>
Mitigation: Review and limit extension permissions and persistent profile usage before using the skill with important listings or sensitive messages. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/winterw/ok-core-skills) <br>
- [Primary skill instructions](SKILL.md) <br>
- [Search workflow](skills/ok-search/SKILL.md) <br>
- [Authentication workflow](skills/ok-auth/SKILL.md) <br>
- [Account management workflow](skills/ok-account/SKILL.md) <br>
- [Runtime requirements](pyproject.toml) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON CLI results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [CLI subcommands return JSON; browser automation may require python3, uv, Playwright, or the OK Bridge extension.] <br>

## Skill Version(s): <br>
0.0.5 (source: server release evidence; artifact frontmatter reports 1.0.0 and pyproject.toml reports 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
