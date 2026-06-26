## Description: <br>
An autonomous Notion coworker agent that monitors Gmail for Notion comment mentions, researches requested answers across memory, Notion, and optionally the web, then replies in the original Notion discussion and documents the research in a subpage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lauroBRCWB](https://clawhub.ai/user/lauroBRCWB) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and teams use this skill to process unread Notion mention notifications from Gmail, research the requested answer using available workspace and web context, and post concise replies back to Notion. It also creates a research subpage so handled mentions have an audit trail. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read Gmail and Notion context, use past chat memory, and publish persistent replies or research pages in Notion. <br>
Mitigation: Use confirmation before posting comments or creating pages, limit the number of notifications handled at once, and avoid writing sensitive private context into shared Notion pages. <br>
Risk: Automatic replies can introduce incorrect or incomplete answers into team discussions. <br>
Mitigation: Require review for medium- or low-confidence answers and preserve source notes in the research subpage for auditability. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls, Guidance] <br>
**Output Format:** [Markdown and plain-text summaries with Notion comment and page creation actions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce persistent Notion comments and research subpages, and may summarize processed Gmail notifications for user follow-up.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
