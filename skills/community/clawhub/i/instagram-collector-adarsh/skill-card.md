## Description: <br>
Collects Instagram profile metrics for a handle using Apify, including follower count, post count, engagement rate, posting frequency, average likes and comments, and top hashtags. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AdarshVMore](https://clawhub.ai/user/AdarshVMore) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and marketing-audit agents use this skill to collect public Instagram profile metrics for a supplied handle and populate an Instagram performance section in an audit report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an Apify API token and sends target Instagram handles to Apify for scraping. <br>
Mitigation: Confirm the Apify data flow is acceptable before installation and keep the API token scoped and protected. <br>
Risk: Apify usage may consume account quota or incur costs. <br>
Mitigation: Monitor Apify plan limits, concurrent runs, and per-run costs during use. <br>
Risk: The local apifyService.ts implementation is referenced by the artifact but is not included in the skill package. <br>
Mitigation: Review and test the local service implementation in the consuming pipeline before relying on collector results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AdarshVMore/instagram-collector-adarsh) <br>
- [Apify Instagram Profile Scraper API endpoint](https://api.apify.com/v2/acts/apify~instagram-profile-scraper/runs) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, configuration] <br>
**Output Format:** [Markdown instructions with TypeScript interface examples and JSON-compatible metric output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns a valid InstagramData object on success or failure, with an error field when collection fails.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
