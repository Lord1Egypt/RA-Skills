## Description: <br>
Analyze Instagram profiles and posts with engagement metrics, view counts, follower ratios, and Reels analytics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TevfikGulep](https://clawhub.ai/user/TevfikGulep) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Social media analysts, marketers, and developers use this skill to analyze public Instagram profiles, posts, and Reels for engagement metrics, view-to-follower ratios, and exportable reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser automation against Instagram may violate site terms, trigger rate limits, or fail when Instagram changes its pages. <br>
Mitigation: Use only authorized and intended analysis targets, keep request volume low, respect Instagram terms, and tune scroll pauses or batch sizes when needed. <br>
Risk: Generated outputs can contain scraped profile, post, and engagement data retained on the local filesystem. <br>
Mitigation: Keep generated data out of shared folders and source control, restrict access to output directories, and delete retained data when it is no longer needed. <br>
Risk: The configuration includes fields for Instagram credentials, and the security guidance warns against storing real account credentials unless the implementation is improved. <br>
Mitigation: Avoid saving real credentials in this skill configuration; use safer credential handling before any production use. <br>
Risk: Dependencies are specified with minimum versions rather than pinned versions. <br>
Mitigation: Pin and review dependency versions before production use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/TevfikGulep/instagram-analyzer) <br>
- [Skill README](artifact/SKILL.md) <br>
- [Analyzer configuration](artifact/config/analyzer_config.json) <br>
- [Analyzer script](artifact/scripts/instagram_analyzer.py) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, CSV, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands; generated analysis data is saved as JSON or CSV files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local data files under data/profiles, data/posts, and data/output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
