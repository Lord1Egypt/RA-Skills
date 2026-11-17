## Description:

Guides agents through evidence-first ILC graph work, attribution, Genesis contact, and OpenClaw local capture.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jamison](https://clawhub.ai/user/jamison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw agents use this skill to set up invite-gated ILC access, inspect public-RC status, manage local graph submissions, and find Genesis contact guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing an unverified package or source may run untrusted software.

Mitigation: Verify the PyPI package or GitHub source before installing.

Risk: Enrollment creates a local ILC identity, and submissions write to a local graph workspace.

Mitigation: Run enrollment or submission commands only when you intend those changes.

Risk: Model Router may promote approved route metadata after the first-run advisory.

Mitigation: Review the advisory and metadata boundary before enabling routing; keep prompts, outputs, and secrets out of graph promotion.

## Reference(s):

- [ILC quickstart](https://github.com/jamison/ilc/blob/main/QUICKSTART.md)
- [Public RC gate](https://github.com/jamison/ilc/blob/main/docs/specs/ilc_public_rc_gate_001_1575c_v0.1.md)
- [Genesis contact protocol](https://github.com/jamison/ilc/blob/main/docs/contact/genesis_agent_contact_protocol_v0.1.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local graph work and invite-gated enrollment; no production settlement authority.]

## Skill Version(s):

0.5.9 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
