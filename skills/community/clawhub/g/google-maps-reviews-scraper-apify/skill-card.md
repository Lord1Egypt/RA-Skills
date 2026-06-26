## Description: <br>
Use this skill when the user needs Google Maps reviews from exact places through an Apify actor, including review text, ratings, dates, review URLs, reviewer profile data, owner replies, review context, detailed ratings, and place metadata from Google Maps place URLs, CID URLs, review URLs, or Place IDs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hundevmode](https://clawhub.ai/user/hundevmode) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and operations teams use this skill to collect structured Google Maps review data for exact places through Apify. It supports local SEO, reputation monitoring, sentiment analysis, competitor research, and BI export workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Google Maps place identifiers and resulting review data are sent to Apify during runs. <br>
Mitigation: Use the skill only when that data transfer is acceptable for the user's workflow and organization. <br>
Risk: Reviewer names, profile URLs, photos, and related public profile fields may be privacy-sensitive. <br>
Mitigation: Set personalData=false unless those fields are needed and lawful for the specific use case. <br>
Risk: Apify runs can incur usage costs or stop early when the configured budget is too low. <br>
Mitigation: Use scoped Apify tokens and set budget limits with maxTotalChargeUsd or the script's --budget-usd option. <br>


## Reference(s): <br>
- [Input and Output Contract](references/input-output-contract.md) <br>
- [Sample Input](references/sample_input.json) <br>
- [Troubleshooting](references/troubleshooting.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/hundevmode/google-maps-reviews-scraper-apify) <br>
- [Project Homepage](https://github.com/hundevmode/apify-google-maps-reviews-scraper-agent-skill) <br>
- [Apify Actor Store Page](https://apify.com/x_guru/google-maps-reviews-scraper) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON output from the Apify runner] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The runner returns JSON containing run status, actor ID, fetch time, input used, item count, and review rows.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
