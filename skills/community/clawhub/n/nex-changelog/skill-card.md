## Description: <br>
Nex Changelog helps agents generate and manage changelogs, release notes, client emails, Telegram updates, and structured exports from manual entries or git commit history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nexaiguy](https://clawhub.ai/user/nexaiguy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, agencies, and software teams use this skill to manage project changelogs, import git commits, create releases, and produce client-facing or public release communications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Client-facing or public drafts may include internal notes, vulnerability details, or private project information if audience filtering misses sensitive content. <br>
Mitigation: Review generated emails, public release notes, and Telegram drafts before sending or publishing them. <br>
Risk: The tool reads git history from repositories the user specifies and stores changelog data locally under ~/.nex-changelog. <br>
Mitigation: Run it only against intended repositories and protect or remove the local changelog database when it contains sensitive project or client data. <br>


## Reference(s): <br>
- [Nex AI Homepage](https://nex-ai.be) <br>
- [Keep a Changelog](https://keepachangelog.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration] <br>
**Output Format:** [Plain text, Markdown, JSON, and generated email or chat-message drafts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local SQLite data and exported changelog files under ~/.nex-changelog.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
