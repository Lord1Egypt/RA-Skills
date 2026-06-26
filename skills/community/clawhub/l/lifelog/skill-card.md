## Description: <br>
LifeLog records daily life entries to Notion, recognizes dates such as today, yesterday, the day before yesterday, and specific dates, appends entries to the matching day, and supports scheduled summaries for emotion, event, location, and people fields. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[421zuoduan](https://clawhub.ai/user/421zuoduan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External ClawHub users use LifeLog to capture personal journal entries in a private Notion database, append them by date, and optionally run daily summaries that fill structured diary fields. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Personal diary entries may include sensitive information and are stored in Notion. <br>
Mitigation: Use a private Notion database, limit the Notion integration to that database, and avoid logging secrets or highly sensitive personal data. <br>
Risk: Configured agents or LLMs may analyze journal content during daily summaries. <br>
Mitigation: Enable scheduled summaries only when that analysis is intended, and review the agent or LLM configuration before allowing ongoing processing. <br>
Risk: Notion tokens can grant access beyond the intended diary database if over-permissioned or shared. <br>
Mitigation: Keep tokens in environment variables or a private secret store, do not commit them to shared files, and scope the Notion integration to one private database. <br>


## Reference(s): <br>
- [LifeLog ClawHub listing](https://clawhub.ai/421zuoduan/lifelog) <br>
- [Notion integration setup](https://www.notion.so/my-integrations) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text status output, Markdown instructions, and bash command invocations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes or updates Notion database pages when configured with a Notion integration token and database ID.] <br>

## Skill Version(s): <br>
1.2.4 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
