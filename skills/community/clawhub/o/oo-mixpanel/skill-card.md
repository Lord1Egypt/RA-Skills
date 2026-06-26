## Description: <br>
Helps agents search and read Mixpanel analytics data through OOMOL's Mixpanel connector and oo CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and support teams use this skill to query Mixpanel events, funnels, cohorts, reports, retention, profiles, and related analytics from an OOMOL-connected account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may use existing local or connected credentials when running Mixpanel actions. <br>
Mitigation: Confirm the intended Mixpanel account, project, action, and payload before running connector commands, and only initiate setup or reauthentication when an auth or connection error requires it. <br>


## Reference(s): <br>
- [ClawHub Mixpanel Skill](https://clawhub.ai/oomol/oo-mixpanel) <br>
- [OOMOL Publisher Profile](https://clawhub.ai/user/oomol) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI Install Guide](https://cli.oomol.com/install-guide.md) <br>
- [Mixpanel](https://mixpanel.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with shell commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Mixpanel query results returned by the oo CLI when the user's connected account authorizes the requested action.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
