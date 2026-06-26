## Description: <br>
Fetch article content from general web page URLs, and call logseq-article-archive to organize, summarize, and archive the content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mesopodamia](https://clawhub.ai/user/mesopodamia) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to fetch web article content, convert it to Markdown, and send it to Logseq through the companion logseq-article-archive skill for summarization and archiving. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches article URLs, converts the content, passes it to logseq-article-archive, and saves it into Logseq. <br>
Mitigation: Use only URLs whose contents are intended to be archived, and review generated Markdown before saving sensitive or private material. <br>
Risk: The security summary notes that the skill tells the agent to automatically install an unpinned companion skill without a clear approval step. <br>
Mitigation: Ask for explicit approval before installing any missing companion skill and verify the companion skill source and version before use. <br>
Risk: Private or login-only pages may be fetched and archived if the user supplies them. <br>
Mitigation: Avoid private or login-only pages unless the user explicitly intends to archive their contents. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mesopodamia/logseq-web-article) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown article content with summary and metadata] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the companion logseq-article-archive skill for secondary analysis and archiving.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
