## Description: <br>
LetPub Skills helps agents retrieve LetPub journal details, collect submission comments, and recommend journals for manuscript targeting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yon8](https://clawhub.ai/user/yon8) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and agent builders use this skill to query LetPub journal metadata, gather logged-in user comments, analyze journal fit, and produce candidate journal recommendations from manuscript context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores LetPub passwords and session cookies in plaintext and reuses them automatically. <br>
Mitigation: Use a dedicated low-risk LetPub account, avoid reusing important passwords, keep credentials.json and cookies.json out of source control and shared folders, and delete them after use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/yon8/letpub-skills) <br>
- [Get journal detail reference](references/get_journal_detail.md) <br>
- [Get journal comments reference](references/get_journal_comments.md) <br>
- [Search journal reference](references/search_journal.md) <br>
- [LetPub](https://www.letpub.com.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python code examples and parsed journal data summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require a LetPub account, local credentials.json, and cookies.json for comment retrieval.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
