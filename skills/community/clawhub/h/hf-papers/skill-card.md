## Description:

Browse trending papers, search by keyword, and get paper details from Hugging Face Papers

This skill is ready for commercial/non-commercial use.

## Publisher:

[willamhou](https://clawhub.ai/user/willamhou)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and technical readers use this skill to find trending Hugging Face Papers, search papers by topic, inspect metadata, and read community discussion. It helps agents surface paper summaries, authorship, engagement, linked resources, and arXiv IDs for deeper reading.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill queries Hugging Face Papers and stores public paper results in a local cache.

Mitigation: Use it only where local caching of public paper metadata is acceptable, and clear the cache when cached results should not persist.

Risk: Cached or trending paper results can become stale as Hugging Face Papers updates throughout the day.

Mitigation: Refresh the query or clear cached results when decisions require the latest paper metadata.

## Reference(s):

- [HF Papers ClawHub release](https://clawhub.ai/willamhou/skills/hf-papers)
- [Hugging Face Papers](https://huggingface.co/papers)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown prose with structured paper metadata and JSON-shaped examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns public paper results and may use a disclosed local cache for repeat access.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
