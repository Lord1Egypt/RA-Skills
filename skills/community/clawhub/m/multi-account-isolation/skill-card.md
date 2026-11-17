## Description:

Verifies whether authorized browser profiles are isolated by checking timezone and exit-IP consistency, WebRTC exposure, fingerprint stability, and separation of persona, address, and cookie state.

This skill is ready for commercial/non-commercial use.

## Publisher:

[antibrow](https://clawhub.ai/user/antibrow)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, QA teams, and anti-fraud engineers use this skill to audit authorized browser profiles and test identities running from one machine. It helps identify browser-layer isolation defects and distinguish them from non-browser correlation risks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can be misapplied to unauthorized account activity.

Mitigation: Use it only for accounts, test identities, QA fixtures, or anti-fraud systems that the operator owns or is authorized to operate, and comply with applicable terms and law.

Risk: The CI check references an npx command that may fetch unpinned package code.

Mitigation: Pin liarjs to an audited version or install it through a committed lockfile before running automated checks.

Risk: Profile-isolation testing may involve API keys, proxy credentials, cookies, and browser profile data.

Mitigation: Keep credentials and profile data scoped to an isolated test environment and avoid exposing raw secrets or session data in logs or reports.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/antibrow/skills/multi-account-isolation)
- [BrowserLeaks WebRTC](https://browserleaks.com/webrtc)
- [CreepJS](https://abrahamjuliot.github.io/creepjs/)
- [Whoer](https://whoer.net)
- [PixelScan](https://pixelscan.net)
- [liarjs](https://liarjs.dev)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with checklists, tables, and TypeScript, Python, and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Authorized-use profile-isolation checklist with concrete verification steps and failure triage.]

## Skill Version(s):

1.0.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
