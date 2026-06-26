## Description: <br>
Unified social media content pipeline for checking draft posts against content-library relevance, AI-signature signals, and platform-specific pre-flight rules before publishing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PHY041](https://clawhub.ai/user/PHY041) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, marketers, and content teams use this skill to run a local pre-publish check for LinkedIn, Reddit, Twitter/X, and Hacker News drafts. It produces a combined PASS/WARN/FAIL report with specific fixes by orchestrating companion content, humanizer-audit, and platform-rules skills when they are installed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads draft text and any folder supplied with --library, which may include sensitive unpublished content. <br>
Mitigation: Run it only on drafts and dedicated content folders that are appropriate for local processing. <br>
Risk: The suite dynamically loads companion skill scripts from local skill directories. <br>
Mitigation: Install the companion skills only from trusted sources and review them before using the suite. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/PHY041/phy-social-suite) <br>
- [Publisher profile](https://clawhub.ai/user/PHY041) <br>
- [Canlah AI homepage](https://canlah.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Plain-text terminal report with command-line usage examples in Markdown documentation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local-only pipeline output; stages are skipped and reported when companion skills are unavailable.] <br>

## Skill Version(s): <br>
1.0.3 (source: server evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
