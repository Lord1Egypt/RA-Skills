## Description:

Diagnoses home internet outages with layered network checks, records timestamped evidence, and prepares an ISP complaint package.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT

## Use Case:

Households and remote workers use this skill to locate a home connectivity fault, choose a first response, monitor interruptions, and prepare evidence for an ISP complaint.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional monitor notification can run arbitrary shell commands when connectivity drops.

Mitigation: Avoid untrusted text in --notify; run diagnose and report manually or use a fixed, trusted notifier command.

Risk: Diagnostics contact public test endpoints and write an outage log locally.

Mitigation: Review network-probe destinations and choose an appropriate local log location before running the skill.

## Reference(s):

- [ISP Evidence Playbook](references/isp-evidence-playbook.md)
- [ClawHub skill release](https://clawhub.ai/voronindenis5/skills/internet-outage-warlord)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text and Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local JSONL outage logs and a ready-to-send ISP complaint.]

## Skill Version(s):

1.0.0 (source: frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
