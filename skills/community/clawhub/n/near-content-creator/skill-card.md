## Description:

Generate NEAR-focused content (threads, market updates, ecosystem news, tutorials).

This skill is ready for commercial/non-commercial use.

## Publisher:

[mastrophot](https://clawhub.ai/user/mastrophot)

### License/Terms of Use:

MIT

## Use Case:

External creators, developers, and ecosystem teams use this skill to draft NEAR educational threads, market updates, ecosystem news digests, and practical tutorials for publication or review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated market and news content depends on public endpoints and may be incomplete, unavailable, or stale.

Mitigation: Review generated content, source links, timestamps, and the data-quality line before publication; do not treat market updates as financial advice.

Risk: The package entrypoint points to dist/index.js while the artifact ships source that must be built.

Mitigation: Run npm install and npm run build before use, then confirm the dist output exists in the deployment artifact.

Risk: Dependency hygiene notes apply before development or CI use.

Mitigation: Update flagged dev dependencies and rerun tests and security checks before using the package in development automation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mastrophot/skills/near-content-creator)
- [Project homepage](https://github.com/mastrophot/near-content-creator)
- [NEAR Blog](https://near.org/blog)
- [nearcore releases](https://github.com/near/nearcore/releases)
- [near-api-js releases](https://github.com/near/near-api-js/releases)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Strings, string arrays, structured news items, and Markdown with bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Thread output is normalized to eight posts; market updates include a data-quality line.]

## Skill Version(s):

0.1.0 (source: SKILL.md metadata, package.json, molthub.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
