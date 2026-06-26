## Description: <br>
Converts web article URLs into structured Obsidian knowledge-base entries with raw article notes, generated image references, classification, wiki summaries, and knowledge graph links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tracky2009](https://clawhub.ai/user/tracky2009) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, agents, and knowledge workers use this skill to turn one or more web article URLs into organized Obsidian vault content, including raw notes, classified wiki nodes, image mappings, and bidirectional knowledge links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes and updates files in an Obsidian vault, so an incorrect OBSIDIAN_VAULT_PATH or unreviewed run could place content in the wrong vault or change existing knowledge-base material. <br>
Mitigation: Set OBSIDIAN_VAULT_PATH deliberately, keep vault backups, and review file diffs after runs that create raw notes, wiki nodes, mappings, or Clippings copies. <br>
Risk: External article fetching and image-generation helpers may process private URLs, article-derived prompts, metadata, or generated images outside the local vault. <br>
Mitigation: Avoid private URLs unless external processing is acceptable, set DASHSCOPE_API_KEY only when intended, and verify any referenced scraping or image-generation helper skills before use. <br>
Risk: The skill can rely on sensitive credentials for optional image generation. <br>
Mitigation: Provide credentials only through environment variables, do not hard-code API keys in notes or scripts, and rotate or revoke keys if exposed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/tracky2009/obsidian-knowledge-pipeline) <br>
- [Pipeline Guide](artifact/pipeline.md) <br>
- [Classification and Wiki Standard](artifact/classification.md) <br>
- [Image Mapping Rules](artifact/image-mapping.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command snippets, file templates, and Obsidian note structures.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates Obsidian vault content under OBSIDIAN_VAULT_PATH, including raw article notes, image mapping entries, wiki nodes, and Clippings copies.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
