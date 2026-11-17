## Description:

Optional design exploration for Platonic Coding Phases 1 and 2. Explores user intent, requirements, alternatives, and design before RFC formalization or implementation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[caesar0301](https://clawhub.ai/user/caesar0301)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to structure early design conversations, clarify requirements, compare approaches, and prepare approved design drafts before RFC formalization or implementation in the Platonic Coding workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional visual companion can run an unauthenticated local web server and may expose or log brainstorming session content if bound beyond loopback or used on shared networks.

Mitigation: Use the visual companion only on loopback/local URLs, avoid binding to 0.0.0.0 on shared or remote networks unless protected by an authenticated tunnel, and treat visible option text as potentially recorded in session state.

Risk: Brainstorming artifacts and companion state may contain sensitive product designs or requirements.

Mitigation: Review generated design drafts before reuse, clean up .superpowers/brainstorm data when it contains sensitive material, and avoid committing companion state unless intentionally retained.

Risk: Stopping visual companion sessions against untrusted or manually edited session directories can operate on unintended local paths.

Mitigation: Run stop-server.sh only against trusted session directories created by this skill's startup flow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/caesar0301/skills/platonic-brainstorming)
- [README](artifact/README.md)
- [Visual Companion Guide](artifact/visual-companion.md)
- [Upstream Superpowers brainstorming skill](https://github.com/obra/superpowers/tree/main/skills/brainstorming)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Conversational guidance and Markdown design drafts, with optional local browser companion setup commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create design drafts under docs/drafts and optional visual companion session files when the user approves that workflow.]

## Skill Version(s):

1.0.2 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
