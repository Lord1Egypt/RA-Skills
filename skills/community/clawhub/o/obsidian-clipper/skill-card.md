## Description: <br>
Save web content such as articles, videos, notes, Xiaohongshu posts, YouTube pages, Zhihu content, WeChat articles, and general web pages to an Obsidian vault with automatic classification, intelligent naming, and content extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[flyeasy](https://clawhub.ai/user/flyeasy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to collect user-provided web links or descriptions into an Obsidian vault as organized Markdown notes. It is intended for personal knowledge management workflows that need automatic source detection, categorization, naming, summarization, and batch saving. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The packaged config may contain a vault path or collector name that does not match the installing user's environment. <br>
Mitigation: Edit or verify config.json before use so the vault path, collector name, and categories are appropriate for the user. <br>
Risk: The skill fetches, searches, or opens user-provided URLs, which can expose confidential, private, intranet, or tokenized links to available retrieval tools. <br>
Mitigation: Use explicit save-to-Obsidian commands and avoid submitting sensitive URLs unless that tool access is acceptable. <br>
Risk: Some sources, including login-gated or hard-to-parse platforms, may produce incomplete extracted content. <br>
Mitigation: Review generated notes and provide copied text or screenshots when automatic retrieval cannot access the source reliably. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/flyeasy/obsidian-clipper) <br>
- [Publisher profile](https://clawhub.ai/user/flyeasy) <br>
- [README.md](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Configuration] <br>
**Output Format:** [Structured Markdown notes saved to an Obsidian vault, plus concise confirmation text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update config.json and writes notes under the configured vault path and category folders.] <br>

## Skill Version(s): <br>
2.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
