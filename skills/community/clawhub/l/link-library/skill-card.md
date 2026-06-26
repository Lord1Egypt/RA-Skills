## Description: <br>
Personal knowledge base that captures web content such as articles, tweets, videos, podcasts, images, and PDFs, then makes saved material retrievable for future conversations and writing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Nowhitestar](https://clawhub.ai/user/Nowhitestar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agent users who maintain a personal research library use this skill to save web links, preserve original content and metadata, retrieve prior items, and cite saved material in later writing or discussion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Shared links may be fetched and saved locally in full text, which can persist sensitive or private material beyond the current conversation. <br>
Mitigation: Use the skill only for content intended to become part of a persistent local library, and explicitly decline saving for temporary summaries or private links. <br>
Risk: Private or token-bearing URLs could expose credentials or restricted content if saved as library entries. <br>
Mitigation: Avoid saving URLs that contain access tokens, session identifiers, private documents, or other sensitive parameters. <br>
Risk: Some fetch workflows rely on external helper tools or commands whose behavior depends on the local environment. <br>
Mitigation: Verify helper tools before use and review fetched content and generated entries before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Nowhitestar/link-library) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown entries, concise chat responses, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local library entries with YAML frontmatter, summaries, tags, original content, notes, and related links.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
