## Description: <br>
Turn your Overcast listening history into actionable intelligence. Syncs episodes, transcripts, and chapters to SQLite, then uses LLM analysis to surface insights from what you've listened to and connect them to your current projects and interests. Depth of analysis is caller-configured. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hbmartin](https://clawhub.ai/user/hbmartin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and podcast-heavy knowledge workers use this skill to sync Overcast listening data into SQLite and ask an agent to summarize, search, and connect podcast episodes to current projects or interests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local SQLite database and transcript archive can expose private Overcast listening history and podcast transcript content. <br>
Mitigation: Store them in a private local directory such as ~/.overcast, use restrictive filesystem permissions, and avoid shared machines or cloud-synced folders. <br>
Risk: The Overcast auth cookie is stored locally and can grant access to the user's Overcast session. <br>
Mitigation: Treat ~/.overcast/auth.json like a password, restrict access to it, and rotate it with overcast-to-sqlite auth if exposure is suspected. <br>
Risk: Transcript analysis may send podcast content and user-interest context to the LLM service used by the agent. <br>
Mitigation: Review the configured LLM provider and avoid analyzing sensitive episodes or personal project context when that disclosure is inappropriate. <br>


## Reference(s): <br>
- [overcast-to-sqlite](https://github.com/hbmartin/overcast-to-sqlite) <br>
- [podcast-transcript-convert](https://github.com/hbmartin/podcast-transcript-convert) <br>
- [podcast-chapter-tools](https://github.com/hbmartin/podcast-chapter-tools) <br>
- [ClawHub skill page](https://clawhub.ai/hbmartin/hbmartin-podcast-intel) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline SQL and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include podcast summaries, key insights, follow-up items, SQL queries, and setup or sync commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
