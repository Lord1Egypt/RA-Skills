## Description:

Operate and build OpenCreator workflows via API for template search, workflow runs, result delivery, and custom graph design.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhuozhihaicloud](https://clawhub.ai/user/zhuozhihaicloud)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to search and run OpenCreator templates, deliver generated media, or design custom workflow graphs for UGC, ecommerce image, storyboard video, and lipsync content workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send user media to OpenCreator production APIs and public temporary file hosts.

Mitigation: Confirm the user's intent before uploads or workflow runs, avoid confidential or regulated media, and prefer user-controlled or authenticated storage links.

Risk: Production workflow jobs may process unintended inputs or incur external service usage.

Mitigation: Collect and confirm required inputs before execution, use the user's own OpenCreator API key, and review workflow parameters before running.

Risk: Installer or source changes could alter agent behavior after review.

Mitigation: Use a reviewed ClawHub install path or pin installer versions where possible.

## Reference(s):

- [OpenCreator Skill Entry Point](artifact/SKILL.md)
- [OpenCreator Skills README](artifact/README.md)
- [OpenCreator Workflow API Guide](artifact/references/api-workflows.md)
- [Node Catalog and Model Selection](artifact/references/node-catalog.md)
- [Workflow Best Practices](artifact/references/best-practices.md)
- [Operator Playbook](artifact/references/operator-playbook.md)
- [UGC Lipsync Ad Scenario](artifact/references/scenarios/scenario-ugc-lipsync-ad.md)
- [Storyboard Video Scenario](artifact/references/scenarios/scenario-storyboard-video.md)
- [Ecommerce Multi-Image Scenario](artifact/references/scenarios/scenario-ecommerce-multi-image.md)
- [OpenCreator Production API Endpoint](https://api-prod.opencreator.io)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON workflow graph examples and inline shell/API commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include workflow node and edge JSON, API request examples, polling guidance, and generated media delivery instructions.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
