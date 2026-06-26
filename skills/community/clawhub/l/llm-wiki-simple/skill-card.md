## Description: <br>
Automatically scans raw articles, notes, papers, and code snippets, then uses an LLM to rewrite and organize them into a structured personal knowledge wiki. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wwl52](https://clawhub.ai/user/wwl52) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Knowledge workers and developers use this skill to turn local source documents into concise, categorized Markdown wiki pages with Obsidian-style backlinks. It supports maintaining a personal knowledge base by scanning raw files, rewriting them through LLM understanding, updating an index, and reporting changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local documents from the Raw folder and may process sensitive information if users place it there. <br>
Mitigation: Avoid putting secrets, credentials, or highly sensitive documents in the Raw folder before running the skill. <br>
Risk: The skill writes or updates generated wiki files, which can overwrite existing wiki content. <br>
Mitigation: Back up existing 01_Wiki content before first use and review generated changes before relying on them. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/wwl52/llm-wiki-simple) <br>
- [Obsidian](https://obsidian.md/) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Guidance] <br>
**Output Format:** [Structured Markdown wiki pages, index updates, and a text build summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes to local wiki directories and preserves the raw source directory as read-only input.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
