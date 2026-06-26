## Description: <br>
Automatically scrape, process, and generate daily news digests from Chinese news sources with source attribution and original links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zigu-creator](https://clawhub.ai/user/zigu-creator) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, analysts, and developers use this skill to monitor Chinese news sources and generate daily digests covering industry dynamics, policy updates, economy, technology, energy, and pricing information. It supports scheduled or on-demand digest creation with optional LLM summarization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scraped article content may be sent to a configured LLM provider during optional summarization. <br>
Mitigation: Set NEWS_DIGEST_LLM_API_KEY and NEWS_DIGEST_LLM_BASE_URL explicitly, use an approved provider, or leave LLM credentials unset to rely on rule-based summaries. <br>
Risk: HTTPS certificate verification is weakened during scraping, which can allow spoofed or modified news content to enter the digest. <br>
Mitigation: Review and fix the TLS verification behavior before trusted use, or accept the risk explicitly for the monitored sources. <br>
Risk: The skill writes digest files to the Desktop and workspace and stores articles in a local SQLite database. <br>
Mitigation: Run it in an appropriate workspace, set NEWS_DIGEST_DB to a controlled path, and review retention or cleanup needs for stored article content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zigu-creator/news-digest-v1) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/zigu-creator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown digest file and timestamped text digest with source attribution and original article links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes a workspace digest file and a Desktop text digest; stores fetched articles and summaries in a local SQLite database.] <br>

## Skill Version(s): <br>
1.0.12 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
