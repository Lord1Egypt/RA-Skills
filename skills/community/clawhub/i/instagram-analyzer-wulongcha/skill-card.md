## Description: <br>
Analyze Instagram profiles and posts with engagement metrics, view counts, follower ratios, and Reels-focused analytics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wulooongcha](https://clawhub.ai/user/wulooongcha) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and social media operators use this skill to inspect Instagram profiles, posts, and Reels for engagement metrics, view-to-follower ratios, and exported analysis data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill automates Instagram scraping with stealth and human-like browser behavior. <br>
Mitigation: Use it only for accounts or content you are authorized to analyze, and do not use it to evade service limits or access controls. <br>
Risk: The artifact references Instagram credentials and includes empty username and password fields in configuration. <br>
Mitigation: Store credentials outside shared files, restrict file permissions, and remove secrets before sharing logs, configs, or generated outputs. <br>
Risk: The skill writes scraped profile, post, batch, and Reels-link data to local files. <br>
Mitigation: Run in an isolated environment, limit collected data to the intended task, and delete generated data when it is no longer needed. <br>
Risk: Dependencies and browser automation increase installation and runtime exposure. <br>
Mitigation: Use pinned dependencies, install Chromium from trusted sources, and review the environment before running the analyzer. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wulooongcha/instagram-analyzer-wulongcha) <br>
- [Publisher profile](https://clawhub.ai/user/wulooongcha) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, CSV, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with command examples plus JSON and CSV analysis files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes profile, post, batch, and Reels-link outputs under the configured data directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
