## Description: <br>
Query MeetGeek meeting intelligence from CLI - list meetings, get AI summaries, transcripts, action items, and search across all your calls with natural language. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nexty5870](https://clawhub.ai/user/nexty5870) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees, external collaborators, and developers use this skill to query MeetGeek meeting records from the CLI for summaries, transcripts, highlights, action items, and meeting search. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A saved MeetGeek API key can grant access to account meeting data. <br>
Mitigation: Install only in trusted environments, use `meetgeek auth --clear` when access is no longer needed, and avoid sharing the local config file. <br>
Risk: Meeting transcripts, summaries, action items, and exports can contain confidential information. <br>
Mitigation: Treat generated meeting content as confidential and avoid saving exports in shared or temporary locations when they contain sensitive data. <br>


## Reference(s): <br>
- [MeetGeek ClawHub Skill Page](https://clawhub.ai/nexty5870/meetgeek) <br>
- [meetgeek-cli npm Package](https://www.npmjs.com/package/meetgeek-cli) <br>
- [meetgeek-cli GitHub Repository](https://github.com/nexty5870/meetgeek-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks and CLI output guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local transcript export paths when the user asks to save meeting data.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
