## Description:

Records and queries a brand's versioned narrative canon, including tagline, message hierarchy, voice and naming rules, and canon re-version proposals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaron-he-zhu](https://clawhub.ai/user/aaron-he-zhu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and brand teams use this skill to maintain a single versioned narrative canon for a brand and to review complete canon-version proposals before downstream copy or campaign builders depend on them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Accepted canon changes persist in the event stream and may guide downstream brand messaging.

Mitigation: Require explicit user authorization, verify the expected runtime and host capability, and review proposed canon changes before any write path is used.

Risk: Unverified claims or wording could be mistaken for approved brand truth.

Mitigation: Keep unverified wording marked as needing a source and route it through a separate claim proposal rather than entering it into the canon as fact.

Risk: A standalone install without the expected host capability cannot append or project canonical narrative truth.

Mitigation: When required capability checks fail, leave a bounded proposal handoff instead of claiming that canonical state was updated.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aaron-he-zhu/skills/narrative-registry)
- [Project homepage](https://github.com/aaron-he-zhu/aaron-marketing-skills)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with text examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce canon status summaries, proposal handoffs, accepted version pointers, and instructions for authorized registry updates.]

## Skill Version(s):

19.0.0 (source: server evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
