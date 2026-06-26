## Description: <br>
This skill lets an agent capture website screenshots through screenshot.fyi using the user's connected OOMOL account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to request website screenshots from an agent session and receive the generated screenshot URL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Credentialed or billable screenshot captures may run against private, internal, sensitive, or unintended URLs. <br>
Mitigation: Confirm the exact target URL and expected screenshot action with the user before running the capture. <br>
Risk: The artifact labels screenshot creation as read-only even though capture can create an external result or consume account credit. <br>
Mitigation: Treat screenshot capture as a credentialed, potentially billable action and pause when the target or cost impact is unclear. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-screenshot-fyi) <br>
- [screenshot.fyi homepage](https://www.screenshot.fyi) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON connector responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connector responses can include a generated screenshot URL and execution metadata.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
