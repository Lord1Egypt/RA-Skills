## Description: <br>
Scrapes Product Hunt leaderboard launches and enriches them with product details, maker profiles, website text, and public contact information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[browseract-cli](https://clawhub.ai/user/browseract-cli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, growth teams, and analysts use this skill to collect structured Product Hunt launch data for startup monitoring, product discovery, competitive tracking, and contact enrichment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can collect public maker profiles, external links, website text, and email addresses from Product Hunt and linked websites. <br>
Mitigation: Use it only for intended Product Hunt research, avoid unnecessary maker or website enrichment, and follow applicable privacy, consent, and site rules. <br>
Risk: Broad or rapid scraping can trigger rate limits or site protections. <br>
Mitigation: Use narrow date ranges or top-N limits, keep website/email enrichment off unless needed, and add delays between page visits. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/browseract-cli/skills/producthunt-launches) <br>
- [Product Hunt](https://www.producthunt.com) <br>
- [Product Hunt daily leaderboard pattern](https://www.producthunt.com/leaderboard/daily/{YYYY}/{M}/{DD}/all) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell command snippets and JSON extraction results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include ranked launch records, launch details, maker profile fields, website text, public email addresses, URLs, images, upvotes, comments, and timestamps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
