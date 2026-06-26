## Description: <br>
Access Granola meeting notes, summaries, transcripts, and attendees via the official Granola public REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gtkumar777](https://clawhub.ai/user/gtkumar777) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent retrieve Granola meeting summaries, attendees, calendar metadata, and transcripts for meeting review workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The configured Granola API key can expose sensitive meeting notes and transcripts. <br>
Mitigation: Use a least-privilege personal API key when possible, avoid workspace-wide keys unless intended, and store the key only in OpenClaw or another secure environment. <br>
Risk: Full transcript requests may surface verbatim sensitive conversation content. <br>
Mitigation: Prefer summaries for overview tasks and request full transcripts only when the user specifically needs verbatim content. <br>
Risk: Ambiguous meeting lookups can retrieve or disclose the wrong meeting content. <br>
Mitigation: Disambiguate by title, attendee, and date before retrieving detailed notes or transcripts. <br>


## Reference(s): <br>
- [Official Granola API docs](https://docs.granola.ai/introduction) <br>
- [Granola](https://granola.ai) <br>
- [ClawHub listing](https://clawhub.ai/gtkumar777/granola-direct-api) <br>
- [Publisher profile](https://clawhub.ai/user/gtkumar777) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include meeting summaries, attendee lists, calendar metadata, and transcript excerpts returned from Granola.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
