## Description:

Podcast Intel helps agents sync Overcast episodes, transcripts, and chapters into SQLite, then analyze recent listening for insights tied to the user's projects and interests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hbmartin](https://clawhub.ai/user/hbmartin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and podcast listeners use this skill to create a local Overcast listening database, retrieve transcripts and chapters, and generate focused LLM analysis of recent or starred episodes. It supports recurring listening intelligence workflows, including summaries, actionable insights, follow-up items, search, and listening statistics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Overcast auth cookie stored in ~/.overcast/auth.json can grant account access if exposed.

Mitigation: Keep the file in a private directory with restrictive permissions and rotate it by re-running Overcast authentication if exposure is suspected.

Risk: The local SQLite database and transcript archive can contain sensitive listening history, episode metadata, and transcript text.

Mitigation: Avoid cloud-synced or shared storage for the database and transcripts unless that sharing is intentional.

Risk: Daily sync creates an ongoing local record of listening activity.

Mitigation: Enable scheduled sync only when the user explicitly wants a recurring local record.

Risk: The workflow depends on third-party CLI packages.

Mitigation: Review or pin package versions before running them in managed or higher-assurance environments.

## Reference(s):

- [overcast-to-sqlite](https://github.com/hbmartin/overcast-to-sqlite)
- [podcast-transcript-convert](https://github.com/hbmartin/podcast-transcript-convert)
- [podcast-chapter-tools](https://github.com/hbmartin/podcast-chapter-tools)
- [ClawHub skill page](https://clawhub.ai/hbmartin/skills/hbmartin-podcast-intel)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with bash, SQL, and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Depth of analysis is caller-configured; outputs may include episode summaries, key insights, project connections, follow-up items, search results, and listening statistics.]

## Skill Version(s):

1.0.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
