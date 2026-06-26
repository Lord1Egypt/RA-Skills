## Description: <br>
Fetch the latest AI daily brief from imjuya/juya-ai-daily (GitHub) and return the Overview (summary) section. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Hunter-Wrynn](https://clawhub.ai/user/Hunter-Wrynn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to retrieve the latest available AI daily brief and return only the overview section, with an option to request details for a numbered item. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes network requests to GitHub and may fail or be rate-limited in restricted or high-volume environments. <br>
Mitigation: Ensure GitHub access and required command-line tools are available before use; set a GitHub token only when higher rate limits are needed. <br>
Risk: GitHub tokens are included in requests to GitHub when GITHUB_TOKEN or GH_TOKEN is set. <br>
Mitigation: Leave GITHUB_TOKEN and GH_TOKEN unset unless rate limits require authentication, and scope any token according to local credential policy. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Hunter-Wrynn/juya-ai-daily-skills) <br>
- [GitHub BACKUP contents endpoint](https://api.github.com/repos/imjuya/juya-ai-daily/contents/BACKUP?ref=master) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown text with optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns the latest available date, the overview section, and a short prompt for requesting item-level detail.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
