## Description: <br>
Guides agents through safe Grafana inspection, dashboard diagnosis, dashboard JSON authoring, alert-rule proposals, and gated change application when verified tools are available. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kansodata](https://clawhub.ai/user/kansodata) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Grafana operators and developers use this skill to inspect live Grafana state, diagnose dashboards and alerting, and prepare dashboard JSON or alert-rule proposals for human review before any gated write operation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated dashboard or alerting changes could be based on stale, partial, or unavailable Grafana state. <br>
Mitigation: Start with read-only inspection, report uncertainty explicitly, and require human review before any apply operation. <br>
Risk: Write-capable Grafana tools may use credentials or gates that are not appropriate for the requested change. <br>
Mitigation: Confirm the runtime-exposed Grafana tools, credential scope, and explicit write gates before enabling apply modes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kansodata/kansodata-grafana-authoring-operations) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown with JSON snippets, logical diffs, and status labels] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may be labeled draft, review_ready, apply_ready, or human_review_required based on verified Grafana context.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
