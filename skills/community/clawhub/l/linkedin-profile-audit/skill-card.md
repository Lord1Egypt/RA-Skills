## Description:

Audit and correct LinkedIn experience descriptions for overclaims, fabricated metrics, and inaccuracies using browser automation and LLM accuracy review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nissan](https://clawhub.ai/user/nissan)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill before job searches, AI-assisted profile rewrites, or reference checks to identify inaccurate LinkedIn experience claims, ask targeted clarification questions, and prepare corrected profile descriptions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can operate a logged-in LinkedIn browser session and make live profile edits.

Mitigation: Require read-only extraction first, review the proposed diff in the visible browser session, and approve each save explicitly.

Risk: The skill may retain profile and employment facts in a memory log for later writing.

Mitigation: Disable or decline memory logging unless the user explicitly wants those facts retained.

Risk: Profile edits may still introduce inaccurate or misleading claims if clarification is incomplete.

Mitigation: Answer one targeted clarification question per flagged claim and verify all corrected descriptions before publishing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nissan/skills/linkedin-profile-audit)
- [Publisher profile](https://clawhub.ai/user/nissan)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Code, Shell commands, Files]

**Output Format:** [Markdown guidance with generated Playwright scripts and local log files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce corrected LinkedIn descriptions, local review files, and a memory log when the user permits retention.]

## Skill Version(s):

1.0.1 (source: server release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
