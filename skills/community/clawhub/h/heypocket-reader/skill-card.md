## Description: <br>
Read transcripts and summaries from Pocket AI recording devices for retrieval, search, and analysis of recordings, transcripts, summaries, and action items. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tmustier](https://clawhub.ai/user/tmustier) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users with Pocket accounts use this skill to list recordings, retrieve transcripts, read summaries, extract action items, and search private Pocket recording data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill accesses a logged-in Pocket browser session and private recording data. <br>
Mitigation: Install only for trusted use cases, review transcript access before running, and avoid using it on shared machines. <br>
Risk: The skill stores a Firebase access token in ~/.pocket_token.json. <br>
Mitigation: Treat the token file like a password, remove it when no longer needed, and keep it out of repositories, backups, and shared home directories. <br>
Risk: The integration uses an unofficial reverse-engineered Pocket API. <br>
Mitigation: Review results before relying on them and expect behavior to change if Pocket updates its web app or API. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tmustier/heypocket-reader) <br>
- [Pocket AI](https://heypocket.com) <br>
- [Pocket web app](https://app.heypocket.com) <br>
- [Pocket API base](https://production.heypocketai.com/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python examples, shell commands, plain text transcripts, markdown summaries, and Python data objects] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a logged-in Pocket browser session and caches a Firebase token in ~/.pocket_token.json for about one hour.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
