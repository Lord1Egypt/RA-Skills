## Description:

Face search and deep research via the Nuwa World API for visual identity intelligence and open-web knowledge synthesis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andrewchen-oss](https://clawhub.ai/user/andrewchen-oss)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to guide agents through Nuwa World API workflows for face-image search and open-web research on people, returning matching URLs, summaries, facts, and cited sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Uploaded face images and person-research queries are sent to a third-party service.

Mitigation: Use the skill only when users are authorized to investigate the image or person, and review Nuwa's privacy, retention, and legal terms before use.

Risk: API credentials may be exposed if copied into prompts, files, or command history.

Mitigation: Store the Nuwa API key in the NUWA_API_KEY environment variable and avoid hardcoding it in shared artifacts.

Risk: Face search and open-web research can produce sensitive or misleading results.

Mitigation: Treat returned URLs, scores, summaries, facts, and sources as leads requiring human review before taking action.

## Reference(s):

- [Nuwa World API documentation](https://gateway.nuwa.world/docs)
- [Nuwa World platform](https://platform.nuwa.world)
- [ClawHub skill page](https://clawhub.ai/andrewchen-oss/skills/nuwa-world-osint-human-research)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, markdown]

**Output Format:** [Markdown with inline bash code blocks and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and NUWA_API_KEY; Nuwa API responses may include URLs, scores, summaries, facts, and sources.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
