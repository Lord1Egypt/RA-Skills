## Description: <br>
Searches LinkedIn candidate profiles through a Chrome debugging session, saves profile summaries locally, and helps score candidates against role and experience criteria. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qianjunye](https://clawhub.ai/user/qianjunye) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Recruiters and hiring teams use this skill to search for LinkedIn profiles for a target role and location, then save candidate files and summarize fit against required and preferred experience signals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow relies on a Chrome debugging session with a LinkedIn login state, which can expose browser session data if reused from a primary profile. <br>
Mitigation: Use a dedicated Chrome profile created only for this workflow, log into LinkedIn manually there, and close the remote-debug Chrome process after use. <br>
Risk: Candidate profile data is scraped and stored locally, which can create privacy and retention obligations. <br>
Mitigation: Keep saved candidate files in a controlled workspace and delete the temporary browser profile and candidate files when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/qianjunye/linkedin-candidate-search) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell and JavaScript snippets, saved Markdown candidate files, and summary tables.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Saves LinkedIn profile records under ./linkedin-save/{role}/ and grades candidates A/B/C when profile content is available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
