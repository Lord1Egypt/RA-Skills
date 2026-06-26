## Description: <br>
Track TikTok ad activity and monitor advertiser changes using PipiAds tools for TikTok ad discovery and Facebook-based monitoring workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fanyanggod](https://clawhub.ai/user/fanyanggod) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, marketers, and external users use this skill to research TikTok ads, inspect advertisers and creatives, create monitor tasks, and review ongoing ad, landing page, product, and copy changes through PipiAds/Pipispy-backed tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a PIPIADS_API_KEY and uses third-party PipiAds/Pipispy services. <br>
Mitigation: Store the API key in an environment variable or secret manager, and only install and use the skill if you trust PipiAds/Pipispy and the pinned npm MCP package. <br>
Risk: Search and monitoring operations may be sent to PipiAds/Pipispy and may consume account credits. <br>
Mitigation: Use narrow searches, review monitor scope before creating tasks, and account for credit usage before running broad monitoring workflows. <br>
Risk: Ad intelligence results can be incomplete, stale, or misinterpreted for market decisions. <br>
Mitigation: Treat outputs as research inputs, verify important advertiser or creative claims against primary sources, and review findings before business use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/fanyanggod/pipiads-tiktok-ad-tracker-monitor) <br>
- [PipiAds homepage](https://www.pipiads.com) <br>
- [Pipispy account and billing](https://www.pipispy.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with setup commands, environment configuration, and text summaries of PipiAds/Pipispy ad research and monitoring results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires npm and PIPIADS_API_KEY; PipiAds API operations may consume account credits.] <br>

## Skill Version(s): <br>
1.0.1 (source: evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
