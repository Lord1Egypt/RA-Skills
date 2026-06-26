## Description: <br>
Job Hunter helps agents search public LinkedIn job listings, filter by role, technology, location, remote preference, and experience, and optionally score matches with Gemini. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[keepfit44](https://clawhub.ai/user/keepfit44) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Job seekers and career-support agents use this skill to run targeted LinkedIn searches, compare matching jobs, save promising listings, and revisit previous searches. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes network requests to LinkedIn and Gemini during job search and scoring. <br>
Mitigation: Use it only when those requests are acceptable for the user task, and review returned listings before relying on them. <br>
Risk: Local files may contain job-search history, saved listings, and an optional Gemini API key. <br>
Mitigation: Use a dedicated Gemini API key, avoid storing secrets in job notes, and delete local job-hunter files when they are no longer needed. <br>


## Reference(s): <br>
- [Job Hunter Data Formats](references/search_format.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, JSON, Configuration] <br>
**Output Format:** [Markdown guidance with shell commands and JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May store configuration, search history, and saved jobs under ~/.openclaw/job-hunter/.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
