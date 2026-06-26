## Description: <br>
Saves web articles into a local Obsidian vault with image capture, Markdown conversion, YAML frontmatter, and appended user notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liz-npa](https://clawhub.ai/user/liz-npa) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to archive web articles, comments, and images into an Obsidian vault as Markdown notes. It supports local and iCloud vault paths and can fall back from Jina.ai Reader to browser-based capture when article extraction fails. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Article URLs and content may be sent to Jina.ai Reader during extraction. <br>
Mitigation: Use the skill only for public or intentionally archived pages, and avoid private, tokenized, intranet, paywalled, or logged-in URLs unless that sharing and storage is intended. <br>
Risk: Browser fallback may capture content from an authenticated browsing session. <br>
Mitigation: Review the target page before saving and avoid fallback capture for pages whose session-only contents should not be archived. <br>
Risk: Image downloading is under-scoped and may fetch arbitrary linked image resources without size or count limits. <br>
Mitigation: Restrict downloads to expected http/https public hosts where possible, and add size and count limits before broad deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liz-npa/obsidian-save-article) <br>
- [Publisher profile](https://clawhub.ai/user/liz-npa) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown notes, JSON script output, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes article Markdown and downloaded image files to a user-configured Obsidian vault path.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
