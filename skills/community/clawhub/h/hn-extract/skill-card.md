## Description: <br>
Extract a HackerNews post, including the linked article and comments, into clean Markdown for quick reading or LLM input. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guoqiao](https://clawhub.ai/user/guoqiao) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to collect a Hacker News discussion, linked article text, comments, and metadata into a single Markdown artifact for review, summarization, or downstream LLM workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may make outbound requests to Hacker News, Algolia, the linked article site, and uv package sources. <br>
Mitigation: Use it only in environments where outbound web access and uv dependency downloads are allowed. <br>
Risk: Article extraction can fail or be incomplete when sites require authentication, block scraping, or return unexpected markup. <br>
Mitigation: Review the generated Markdown before relying on it for summaries, decisions, or redistribution. <br>
Risk: The script writes to the requested output path and creates parent directories as needed. <br>
Mitigation: Use a controlled temporary output path and avoid passing sensitive or shared directories unless intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/guoqiao/hn-extract) <br>
- [Skill source](https://github.com/guoqiao/skills/blob/main/hn-extract/hn-extract/SKILL.md) <br>
- [Examples](https://github.com/guoqiao/skills/blob/main/hn-extract/examples) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Text] <br>
**Output Format:** [Markdown file or stdout text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates parent directories for requested output paths; verbose mode can also save JSON, HTML, and text debug files.] <br>

## Skill Version(s): <br>
0.1.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
