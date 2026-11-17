## Description:

Helps finish an iOS release after build upload by preparing its App Store listing, resolving submission blockers, and submitting or resubmitting it for review through MetaRun.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iderasyh](https://clawhub.ai/user/iderasyh)

### License/Terms of Use:

MIT-0

## Use Case:

iOS developers and release managers use this skill to attach an uploaded build, address App Store submission requirements, and submit or resubmit a version for App Review with explicit approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An external MetaRun client can access App Store release credentials and perform consequential release actions.

Mitigation: Use a trusted, pinned or preinstalled client and a narrowly scoped token where possible; review each preview diff before approving changes or submission.

Risk: Live tool discovery can expose broader pricing, reviews, ASO, and TestFlight capabilities than the release handoff requires.

Mitigation: Limit use to release-handoff actions unless broader access is intentionally authorized.

## Reference(s):

- [MetaRun for agents](https://metarun.dev/agents)
- [MetaRun: release handoff on ClawHub](https://clawhub.ai/iderasyh/skills/metarun-release-handoff)

## Skill Output:

**Output Type(s):** [Guidance, Text, Shell commands]

**Output Format:** [Markdown with inline commands and release-status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include preview diffs, readiness blockers, and items requiring manual App Store Connect action.]

## Skill Version(s):

1.0.0 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
