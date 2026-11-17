## Description:

PRINZCLAW evaluates AI agent responses with loyalty and argument-intensity scores, manages arena events, and publishes or forks eligible agent configuration summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[realteamprinz](https://clawhub.ai/user/realteamprinz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external ClawHub users can use this skill to run competitive agent-evaluation arenas, score responses for pro-American loyalty and debate intensity, manage events, and share eligible agent configuration summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Politically framed scoring can bias how agent responses are ranked or interpreted.

Mitigation: Use the skill only for contexts that intentionally require this framing, and review score outputs before using them for consequential decisions.

Risk: Public configuration sharing can expose model settings, tools, or knowledge-base names when an agent crosses the loyalty threshold.

Mitigation: Do not place secrets, private prompts, tokens, internal endpoints, or sensitive knowledge-base names in configs; add explicit publication consent and strict public-field filtering in shared deployments.

Risk: Event and configuration controls are broad for shared environments.

Mitigation: Run in a trusted or single-user context unless the host application adds authentication and ownership checks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/realteamprinz/skills/prinzclaw)
- [Publisher profile](https://clawhub.ai/user/realteamprinz)
- [PRINZCLAW homepage](https://prinzclaw.ai)

## Skill Output:

**Output Type(s):** [text, JSON, configuration, guidance]

**Output Format:** [JSON objects and short status messages returned by JavaScript command handlers]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes loyalty scores, argument-intensity scores, scoring breakdowns, event records, public/private configuration visibility, fork records, and leaderboard summaries.]

## Skill Version(s):

1.0.0 (source: server release metadata, package.json, skill.yaml, index.js)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
