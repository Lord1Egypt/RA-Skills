## Description:

Generate images, PDFs, and videos from templates, then prepare, schedule, and publish social media content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[orshot](https://clawhub.ai/user/orshot)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and content teams use the skill to generate branded media and documents from templates, automate content workflows, and manage social posts across connected accounts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Workspace assets, connected social accounts, and submitted content may be exposed through the service or generated links.

Mitigation: Connect only intended workspaces and accounts, submit only content approved for sharing, treat hosted render URLs as shareable, and use opaque embed user IDs.

Risk: Publishing posts, running workflows, or deleting assets can cause external or irreversible changes.

Mitigation: Keep posts in draft during review and obtain explicit approval before publishing, running workflows, or deleting assets.

Risk: Bulk renders and recurring workflows can consume credits or publish on a schedule.

Mitigation: Review costs and recurring schedules before starting bulk work or activating automation.

Risk: The optional CLI introduces a package and version dependency.

Mitigation: Verify the package and version before installing or using the CLI.

## Reference(s):

- [Orshot agent integration](https://orshot.com/agents/openclaw)
- [Orshot documentation](https://orshot.com/docs)
- [API reference](references/api-reference.md)
- [Render configuration](references/render-configuration.md)
- [Template design specification](references/template-design-spec.md)
- [Recurring automation](references/recurring-automation.md)
- [Integrations and errors](references/integrations-and-errors.md)

## Skill Output:

**Output Type(s):** [Images, PDFs, Videos, Social media posts]

**Output Format:** [Rendered media files and draft, scheduled, or published social content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Media format, dimensions, and delivery depend on the selected template and destination.]

## Skill Version(s):

1.4.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
