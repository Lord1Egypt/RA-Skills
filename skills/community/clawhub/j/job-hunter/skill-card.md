## Description: <br>
Comprehensive job search assistant for finding, evaluating, and applying to job opportunities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sharbelayy](https://clawhub.ai/user/sharbelayy) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Job seekers and agents use this skill to find job openings, evaluate fit against a candidate profile, prepare tailored application materials, research salary ranges, prepare for interviews, and track application status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The included search helper script can execute local Python code from crafted job-search input. <br>
Mitigation: Review and patch scripts/search_jobs.sh before use so shell values are passed safely to Python and numeric options are validated. <br>
Risk: Candidate profiles, job trackers, and application materials can contain sensitive personal career data. <br>
Mitigation: Keep generated profile and tracker files in a private workspace and review outputs before sharing them externally. <br>
Risk: The search helper can query Brave Search when BRAVE_API_KEY is set. <br>
Mitigation: Set BRAVE_API_KEY only when external Brave Search requests are intended. <br>


## Reference(s): <br>
- [Cover Letter & Application Guide](references/cover-letter-guide.md) <br>
- [Interview Preparation Guide](references/interview-prep.md) <br>
- [Candidate Profile Template](references/profile-template.json) <br>
- [Job Search Strategies](references/search-strategies.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON outputs and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update candidate profiles, job result JSON, fit analysis JSON, and application tracker content in the workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
