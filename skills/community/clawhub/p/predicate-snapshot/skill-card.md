## Description:

ML-powered DOM pruning for 95% smaller browser prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rcholic](https://clawhub.ai/user/rcholic)

### License/Terms of Use:

(MIT OR Apache-2.0)

## Use Case:

Developers and browser-automation agents use this skill in OpenClaw to capture compact, ranked DOM snapshots and interact with page elements by Predicate ID.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can click, type, and scroll in active browser pages, including sensitive logged-in, payment, or admin pages.

Mitigation: Supervise /predicate-act use and avoid granting the skill active sessions with unnecessary privileges.

Risk: ML snapshot mode should be reviewed before use on sensitive browsing contexts.

Mitigation: Prefer /predicate-snapshot-local for sensitive pages or review page sensitivity before enabling ML ranking.

Risk: Mutable installer and dependency paths can change between installations.

Mitigation: Pin or verify the installer, package version, and dependencies instead of relying on @latest.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/rcholic/skills/predicate-snapshot)
- [Predicate Snapshot homepage](https://predicate.systems/skills/snapshot)
- [Predicate documentation](https://predicatesystems.ai/docs)
- [Install and test guide](docs/INSTALL_AND_TEST.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown headers followed by a compact pipe-delimited element table, or short status/error text for actions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Snapshot output is limited by a configurable element count; ML ranking requires PREDICATE_API_KEY, while local mode avoids ML re-ranking.]

## Skill Version(s):

0.4.0 (source: package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
