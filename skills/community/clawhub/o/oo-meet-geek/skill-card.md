## Description: <br>
MeetGeek lets an agent retrieve meetings, summaries, insights, highlights, transcripts, and team data from a connected MeetGeek account through OOMOL's oo CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers use this skill to search and read MeetGeek meeting records, transcripts, summaries, highlights, insights, and team meeting data from an already connected account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Meeting summaries, transcripts, highlights, and insights may contain sensitive business or personal information. <br>
Mitigation: Use the skill only for explicit MeetGeek data requests and share retrieved meeting content only with the intended audience. <br>
Risk: The skill retrieves data from the user's connected MeetGeek account. <br>
Mitigation: Install and use it only when that account access is appropriate for the task, and resolve connection or credential issues through the documented setup flow only after an auth-related command failure. <br>


## Reference(s): <br>
- [ClawHub MeetGeek skill listing](https://clawhub.ai/oomol/skills/oo-meet-geek) <br>
- [MeetGeek homepage](https://meetgeek.ai) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON command responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schema inspection before action payloads are constructed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
