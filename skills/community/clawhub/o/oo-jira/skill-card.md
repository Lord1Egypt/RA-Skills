## Description: <br>
Jira lets an agent read Jira issues, projects, comments, and JQL search results, and create Jira issues or comments through an OOMOL-connected account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate Jira from an agent workflow, including issue lookup, project lookup, comment review, JQL search, issue creation, and comment creation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create Jira issues or comments through the connected Jira account. <br>
Mitigation: Review the exact payload and effect before approving write actions. <br>
Risk: The skill depends on the third-party OOMOL connector and oo CLI operating against the user's connected Jira account. <br>
Mitigation: Install and use it only when the publisher and connector are trusted for the Jira workspace involved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-jira) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [Jira](https://www.atlassian.com/software/jira) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May execute Jira connector actions through the oo CLI and return connector JSON responses when the user directs an action.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
