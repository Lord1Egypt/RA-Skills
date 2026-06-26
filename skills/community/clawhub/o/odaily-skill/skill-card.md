## Description: <br>
Odaily Skill helps an agent retrieve and summarize live crypto news, market data, upcoming events, Polymarket whale-trade signals, and raw Odaily API content for decision-oriented market analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[odaily](https://clawhub.ai/user/odaily) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to ask an agent for structured crypto market briefings, live news summaries, macro and event calendars, prediction-market whale signals, and API-oriented source content for further analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run Python tools, install Python dependencies, and make live network calls for crypto news and market-data analysis. <br>
Mitigation: Review and pin requirements before installation, and run the skill only in environments where live network access for market and news sources is acceptable. <br>
Risk: Broad auto-invocation from generic market or news trigger words could cause the agent to run the skill when the user intended a different workflow. <br>
Mitigation: Configure invocation rules narrowly and confirm intent before using the skill in sensitive environments. <br>
Risk: Optional Supabase configuration can write whale-trade records to a user-controlled database. <br>
Mitigation: Configure Supabase only when persistent storage is intended, and use scoped credentials for that database. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/odaily/odaily-skill) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/odaily) <br>
- [Odaily](https://www.odaily.news) <br>
- [Odaily newsflash API](https://web-api.odaily.news/newsflash/page) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with structured sections, tables, links, and occasional inline shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include live-data caveats and investment-advice disclaimers where the artifact behavior specifies them.] <br>

## Skill Version(s): <br>
1.0.10 (source: ClawHub release evidence; artifact frontmatter reports 4.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
