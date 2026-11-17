## Description:

Drift lets stateless agents maintain time-shifted conversations by leaving questions, responses, and reflections for future sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cryptocana](https://clawhub.ai/user/cryptocana)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use Drift to maintain asynchronous conversation threads across stateless sessions, including reflections, questions, answers, and catch-up reviews.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI can read JSON files outside the intended thread folder through insufficient thread ID path scoping.

Mitigation: Validate thread IDs against the expected short hexadecimal format and verify resolved paths remain inside the configured Drift thread directory.

Risk: Stored thread content is printed back to the terminal and may include unsafe control sequences or sensitive local notes.

Mitigation: Sanitize terminal output and avoid using Drift with sensitive local JSON content until the CLI has been reviewed and hardened.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cryptocana/skills/nova-drift)
- [Project homepage](https://github.com/novaiok/drift)
- [README](README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and local JSON thread records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The CLI stores and reads conversation threads as JSON files under the configured Drift thread directory.]

## Skill Version(s):

0.1.0 (source: frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
