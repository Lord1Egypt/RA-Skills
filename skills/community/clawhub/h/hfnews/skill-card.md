## Description: <br>
Fetch and filter news from multiple sources with stopwords/blacklist support. Customized for Hubert's interests (IT, Cybersecurity) with political/sports noise filtered out. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huberteff](https://clawhub.ai/user/huberteff) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users can use this skill to retrieve concise IT, cybersecurity, and general news headline lists while filtering unwanted topics through a configured blacklist. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes web requests to public news sites, which can expose network activity and depends on third-party page or feed availability. <br>
Mitigation: Install only when this network behavior is acceptable, and run it with normal user privileges. <br>
Risk: The JavaScript scraper launches Chromium with browser sandboxing disabled. <br>
Mitigation: Prefer the RSS Python path where practical, keep Chromium and Puppeteer updated, and avoid running the browser path with elevated privileges. <br>


## Reference(s): <br>
- [ClawHub hfnews Skill Page](https://clawhub.ai/huberteff/hfnews) <br>
- [ClawHub Publisher Profile: huberteff](https://clawhub.ai/user/huberteff) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands] <br>
**Output Format:** [Plain-text categorized headline lists with article URLs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports all categories by default or a single requested category; applies blacklist filtering before returning headlines.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
