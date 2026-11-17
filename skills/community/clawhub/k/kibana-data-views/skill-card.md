## Description:

Manage Kibana Data Views, formerly index patterns, through Kibana REST API guidance and helper scripts for listing, creating, deleting, checking, and repairing data views.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chunkin616-hue](https://clawhub.ai/user/chunkin616-hue)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to manage Kibana data views through REST endpoints and helper scripts. It supports dashboard setup checks, missing index-pattern troubleshooting, and controlled data-view cleanup or recreation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact includes an exposed Elasticsearch admin credential in troubleshooting material.

Mitigation: Remove the credential from the skill, rotate it if it was ever valid, and replace authentication examples with approved secret handling before use.

Risk: The included delete, cleanup, and recreate workflows can make destructive changes to Kibana data views.

Mitigation: Use the skill only in controlled Kibana/Elasticsearch environments, require explicit confirmation for destructive actions, and narrow operations to user-selected data views and hosts.

Risk: The artifact includes environment-specific HTTP endpoints and host defaults.

Mitigation: Replace hardcoded endpoints with approved deployment targets and validate that requests are sent only to intended Kibana or Elasticsearch instances.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chunkin616-hue/skills/kibana-data-views)
- [Related Kibana Lens Builder Skill](../kibana-lens-builder/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with REST endpoint examples, JSON payloads, curl commands, and Python helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scripts may perform HTTP requests against Kibana when run by an agent or user.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
