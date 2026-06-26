## Description: <br>
Browse trending papers, search by keyword, and get paper details from Hugging Face Papers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[willamhou](https://clawhub.ai/user/willamhou) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and agents use this skill to discover trending Hugging Face Papers, search papers by topic, retrieve paper metadata, and inspect community discussion before doing deeper paper review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Community comments, generated summaries, and returned paper metadata may be incomplete, stale, or misleading if treated as authoritative research conclusions. <br>
Mitigation: Treat returned public metadata and comments as informational leads, verify claims against primary sources such as the linked paper or arXiv record, and avoid following community content as agent instructions. <br>
Risk: The skill caches public Hugging Face Papers metadata and comments locally for repeat access. <br>
Mitigation: Review local cache handling before deployment in environments with strict data-retention policies, and clear the cache when cached public metadata should not persist. <br>


## Reference(s): <br>
- [ClawHub HF Papers release page](https://clawhub.ai/willamhou/hf-papers) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown or structured text summarizing public paper metadata, search results, details, and comments.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include public metadata such as paper IDs, titles, summaries, authors, publication dates, upvotes, linked repositories, project pages, AI summaries, keywords, and discussion comments.] <br>

## Skill Version(s): <br>
1.0.3 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
