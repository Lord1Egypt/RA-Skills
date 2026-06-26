## Description: <br>
Manages an Eastmoney/Miaoxiang self-selected stock watchlist through natural-language query, add, and delete commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jessecq1995](https://clawhub.ai/user/jessecq1995) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers with an Eastmoney/Miaoxiang account use this skill to query, add, and delete stocks in a remote watchlist from command-line or natural-language requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Natural-language add and delete commands can persistently change a remote financial watchlist without a separate confirmation step. <br>
Mitigation: Run add or delete commands only when you explicitly intend to modify the watchlist, and review the command text before execution. <br>
Risk: The skill requires an Eastmoney/Miaoxiang API key for account access. <br>
Mitigation: Provide the key through MX_APIKEY in a trusted server-side environment and avoid exposing it in client-side or shared contexts. <br>
Risk: Watchlist query results are saved locally as CSV and raw JSON. <br>
Mitigation: Store output files in an appropriate directory and remove them when the account or financial data should not persist locally. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jessecq1995/mx-selfselect) <br>
- [Publisher profile](https://clawhub.ai/user/jessecq1995) <br>
- [Eastmoney Miaoxiang API host](https://mkapi2.dfcfs.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, CSV files, JSON files] <br>
**Output Format:** [Markdown guidance with shell commands; runtime output includes terminal text, CSV files, and raw JSON files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Query results are saved locally as CSV and raw JSON in the configured output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
