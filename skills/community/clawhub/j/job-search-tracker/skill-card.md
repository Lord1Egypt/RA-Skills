## Description: <br>
Tracks job applications from discovery to offer, flags stale applications, and helps draft follow-ups, cover letters, interview prep, and salary negotiation materials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chris-openclaw](https://clawhub.ai/user/chris-openclaw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users managing an active job search use this skill to keep application status, contacts, follow-up dates, and offer details organized while generating job-search communications and preparation materials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Connected Gmail, LinkedIn, browser, or web-search tools may expose sensitive inbox content, job history, salary details, offer details, and recruiter contacts. <br>
Mitigation: Install only with tools the user is comfortable connecting; use tracker-only mode by not connecting Gmail or LinkedIn when lower exposure is preferred. <br>
Risk: Applications discovered from Gmail or LinkedIn could be added incorrectly if external findings are treated as authoritative without user review. <br>
Mitigation: Present externally discovered applications to the user and wait for explicit confirmation before adding them to the tracker. <br>
Risk: The local tracker and generated drafts can contain sensitive job-search and compensation information. <br>
Mitigation: Keep writes scoped to the current working directory, avoid including sensitive tracker fields in drafts unless requested, and require consent before destructive edits. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chris-openclaw/job-search-tracker) <br>
- [README](README.md) <br>
- [Changelog](CHANGELOG.md) <br>
- [Evaluation cases](evals/evals.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, guidance] <br>
**Output Format:** [Markdown tracker files, dashboard summaries, job-search drafts, analysis, and concise guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local applications.md, resumes/ metadata, dashboards, and drafts in the user's working directory.] <br>

## Skill Version(s): <br>
1.1.2 (source: frontmatter, README, CHANGELOG, and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
