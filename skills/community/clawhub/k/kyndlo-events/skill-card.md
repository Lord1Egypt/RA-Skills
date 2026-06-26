## Description: <br>
Kyndlo Events guides an agent through Kyndlo campaign task selection, venue research, event creation, image upload, and event validation workflows using the gokyn CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pirumpi](https://clawhub.ai/user/pirumpi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and operators use this skill to create Kyndlo events from campaign tasks, research matching venues, attach images, and validate existing event records in controlled batches. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An agent can use the configured Kyndlo token to claim tasks, create events, submit validations, and access broader event-management commands. <br>
Mitigation: Use the least-privileged token available, start with small batches, and review planned actions before confirming the workflow. <br>
Risk: Administrative commands such as update, delete, or campaign seeding can change production event or campaign data. <br>
Mitigation: Avoid those commands unless the user explicitly requests the administrative change and has reviewed the target records. <br>
Risk: Venue research and validation depend on current place data, so stale or incorrect venue details could produce inaccurate event records. <br>
Mitigation: Use the documented duplicate, county, hours, and validation checks, and pause after each batch to review results. <br>


## Reference(s): <br>
- [Kyndlo Events on ClawHub](https://clawhub.ai/pirumpi/kyndlo-events) <br>
- [gokyn CLI homepage](https://github.com/kyndlo/gokyn-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with CLI commands and JSON-aware summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke gokyn and goplaces commands that create, update, validate, or report event data after workflow confirmation.] <br>

## Skill Version(s): <br>
3.5.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
