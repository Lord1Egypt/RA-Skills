## Description:

Activates an adversarial review posture for requests to find problems, poke holes, stress test, play devil's advocate, challenge, or find flaws in artifacts such as plans, code, documents, arguments, data pipelines, and architecture.

This skill is ready for commercial/non-commercial use.

## Publisher:

[long1973m](https://clawhub.ai/user/long1973m)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, reviewers, and other users invoke this skill when they want an agent to perform aggressive problem discovery on code, plans, documents, arguments, data pipelines, architecture, prompts, or other artifacts. It directs the agent to identify flaws, risks, assumptions, verification gaps, edge cases, and adversarial failure modes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad critical-review trigger phrases can make ordinary review requests unexpectedly hostile, one-sided, or hard to scope.

Mitigation: Install only when this aggressive dissent mode is desired, and give explicit limits on scope, tone, and output format.

Risk: Override-style posture may crowd out neutral audit framing or balanced assistance.

Mitigation: Use it as a review-style modifier and require the agent to keep findings concrete, bounded by the requested artifact, and clear about unverified claims.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/long1973m/skills/objection)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown findings with categorized problem statements, impact notes, verification steps, and an unverified claims section]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prompt-only skill; no API calls, shell commands, files, MCP tools, or credential environment variables were detected.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
