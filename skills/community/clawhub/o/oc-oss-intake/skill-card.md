## Description:

Turn a promising open-source repo into a defensible OpenClaw adoption decision before code, dependencies, or risk enter the workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiepu110](https://clawhub.ai/user/jiepu110)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to evaluate open-source repositories before adoption, document license and dependency risk, and decide whether to reject, observe, adapt, or implement a candidate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: External repository review can expose the agent to unverified project claims, unsafe dependencies, or unclear license terms.

Mitigation: Confirm the official repository URL, review license and dependency signals, and avoid importing code or installing dependencies without separate review.

Risk: An adoption note could overstate readiness if repository activity, tests, or rollback criteria are weak.

Mitigation: Require an explicit adoption class, validation commands, and rollback criteria before moving from intake to implementation.

Risk: The skill includes visible voluntary links asking users to star ClawHub or a GitHub repository.

Mitigation: Treat those links as manual user actions only; they are not required for the intake decision and are not evidence of provenance.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown intake note]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes project metadata, capability summary, adoption class, risks and license notes, proposed local candidate, and validation plan.]

## Skill Version(s):

1.0.1 (source: server evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
