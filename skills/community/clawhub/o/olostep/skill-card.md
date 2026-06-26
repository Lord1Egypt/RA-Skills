## Description: <br>
Helps an agent scrape webpages, search Google, crawl and map sites, batch-scrape URLs, and request AI-powered answers with citations through the Olostep Web Data API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zeeshanadilbutt](https://clawhub.ai/user/zeeshanadilbutt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill when they need live web data for research, documentation ingestion, competitor analysis, data extraction, error debugging, or structured web intelligence. It guides the agent to call Olostep endpoints for scraping, Google search parsing, crawls, batches, site maps, retrieval, and cited answers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a third-party web data provider, so submitted URLs, queries, and tasks may be shared with Olostep. <br>
Mitigation: Avoid private, authenticated, regulated, proprietary, or personal-data-heavy targets unless the user has permission and is comfortable sharing them with Olostep. <br>
Risk: Crawls and batch scrapes can collect large volumes of web content, including up to 10,000 URLs per batch. <br>
Mitigation: Keep crawls and batches tightly scoped, confirm target-site rules and organizational approval, and fetch only what the current task needs. <br>


## Reference(s): <br>
- [Olostep API Docs](https://docs.olostep.com) <br>
- [Olostep Homepage](https://olostep.com) <br>
- [ClawHub Skill Page](https://clawhub.ai/zeeshanadilbutt/olostep) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with curl commands, JSON request examples, and response-field notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OLOSTEP_API_KEY and sends requested URLs, queries, or tasks to the third-party Olostep API.] <br>

## Skill Version(s): <br>
1.0.3 (source: artifact/SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
