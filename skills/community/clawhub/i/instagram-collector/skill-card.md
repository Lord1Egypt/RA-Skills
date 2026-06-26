## Description: <br>
Collects Instagram profile metrics for a supplied handle using Apify's Instagram Profile Scraper. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AdarshVMore](https://clawhub.ai/user/AdarshVMore) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Marketing and analytics agents use this skill to gather public Instagram account metrics for a brand handle and populate the Instagram Performance section of an audit report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The collector sends requested Instagram handles and scraper results to Apify for processing. <br>
Mitigation: Use this skill only when users are comfortable with Apify processing the requested handles and returned profile data. <br>
Risk: Apify usage may consume quota or incur charges and depends on a valid API token. <br>
Mitigation: Use a dedicated Apify token, monitor quota and charges, and rotate or revoke the token if access is no longer needed. <br>
Risk: Public Instagram data returned by Apify may be stale, incomplete, or unavailable for private and missing profiles. <br>
Mitigation: Treat results as audit inputs, keep the documented error field behavior, and avoid blocking downstream collectors when Instagram data is unavailable. <br>


## Reference(s): <br>
- [Instagram Collector on ClawHub](https://clawhub.ai/AdarshVMore/instagram-collector) <br>
- [Apify Instagram Profile Scraper API endpoint](https://api.apify.com/v2/acts/apify~instagram-profile-scraper/runs) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Configuration] <br>
**Output Format:** [Markdown with TypeScript code blocks and structured data schema] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Describes a collector that returns structured Instagram metrics with graceful error fields.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
