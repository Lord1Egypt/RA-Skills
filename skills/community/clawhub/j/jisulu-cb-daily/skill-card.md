## Description:

每日从集思录抓取可转债基本数据、强赎倒计时、下修倒计时，支持Cookie管理和本地持久化存储。

This skill is ready for commercial/non-commercial use.

## Publisher:

[cchunter](https://clawhub.ai/user/cchunter)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to collect daily Jisilu convertible bond data, including base bond fields, forced redemption countdowns, downward conversion price adjustment countdowns, and a local CSV record for later analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for and stores a live Jisilu session cookie in plaintext.

Mitigation: Treat kbzw__user_login like a password, avoid sharing it in chats, restrict access to references/cookie.json, and delete or rotate the cookie if it is exposed.

Risk: Optional scheduled execution can write logs that include part of the cookie value.

Mitigation: Review cron logging before enabling automation, restrict access to output logs, and avoid sharing cron.log or terminal output that contains credential fragments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cchunter/skills/jisulu-cb-daily)
- [Jisilu convertible bond list data source](https://www.jisilu.cn/web/data/cb/list)
- [Jisilu forced redemption data source](https://www.jisilu.cn/web/data/cb/redeem)
- [Jisilu downward adjustment data source](https://www.jisilu.cn/web/data/cb/adjust)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Files, Guidance]

**Output Format:** [CSV files plus console or Markdown status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes daily output files named output/jisilu_cb_YYYY-MM-DD.csv and may create references/cookie.json for the user's Jisilu cookie.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
