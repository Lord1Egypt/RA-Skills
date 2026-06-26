## Description: <br>
Extract and break down content from web documents, PDFs, images, and URLs into structured markdown notes stored locally and synced to Obsidian. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[biohackerrrrrr](https://clawhub.ai/user/biohackerrrrrr) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use Image Breaker to convert provided URLs, PDFs, images, screenshots, or pasted document content into structured Markdown notes with tags, source attribution, local storage, and optional Obsidian syncing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-provided documents, screenshots, PDFs, and extracted notes may be persisted locally and copied into an Obsidian workflow. <br>
Mitigation: Process confidential or medical material only when that persistence is acceptable, and review saved notes and storage destinations before sharing or acting on them. <br>
Risk: The artifact includes a hardcoded Obsidian vault path and calls a separate obsidian-sync helper when syncing is enabled. <br>
Mitigation: Update the vault path for the deployment environment and review the sync helper before enabling automatic sync. <br>
Risk: Extraction and summarization of documents, especially medical or lab material, can introduce omissions or incorrect interpretation. <br>
Mitigation: Keep source attribution in each note and review generated content against the original source before relying on it. <br>


## Reference(s): <br>
- [Content Templates for Image Breaker](artifact/references/content-templates.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/biohackerrrrrr/image-breaker) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown notes with YAML frontmatter, local file paths, optional shell commands, and a completion summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include generated note files under workspace research or content directories and optional Obsidian sync destinations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
