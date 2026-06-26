## Description: <br>
Searches for music resources such as songs, albums, and lossless audio across Quark, Baidu, Aliyun, and UC cloud-drive links. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[patches429](https://clawhub.ai/user/patches429) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to search for publicly indexed music-resource links, filter results by cloud-drive provider or audio format, and summarize JSON results for the user. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can crawl arbitrary third-party pages and resolve arbitrary URLs. <br>
Mitigation: Run it in a contained environment, review returned links before sharing them, and avoid use on networks with access to sensitive internal services. <br>
Risk: The Bash launcher sources local .env content during startup. <br>
Mitigation: Keep the skill directory trusted, review .env changes before execution, and do not store secrets in the skill .env file. <br>
Risk: The skill may install cloudscraper into a local virtual environment on first use. <br>
Mitigation: Review dependency installation behavior and pin or preinstall dependencies in managed environments. <br>
Risk: @file arguments may read local file contents into the search query. <br>
Mitigation: Avoid @file arguments that point to sensitive files and review command arguments before execution. <br>


## Reference(s): <br>
- [ClawHub Music Search listing](https://clawhub.ai/patches429/music-search) <br>
- [Publisher profile](https://clawhub.ai/user/patches429) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration] <br>
**Output Format:** [JSON command output with agent-facing text or Markdown summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results can include cloud-drive links, magnet links, extraction codes, detected audio formats, source page URLs, and configurable result limits.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
