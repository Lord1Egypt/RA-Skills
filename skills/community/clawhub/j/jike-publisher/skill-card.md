## Description:

Publish posts to Jike using browser automation for text posts with emoji, hashtags, topics, and links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maoruibin](https://clawhub.ai/user/maoruibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to draft and publish Jike updates through an already logged-in managed browser session. It is intended for text-based posts that may include Chinese content, emoji, hashtags, topics, links, and line breaks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish public posts through an already logged-in Jike browser session.

Mitigation: Require the agent to show the exact account and post content, then wait for explicit approval before publishing.

Risk: Post text may be stored locally in memory/jike-state.json.

Mitigation: Delete or minimize the state file when post content is sensitive.

Risk: The optional script describes the posting workflow and can report success without proving that a post was published.

Mitigation: Verify publication in the Jike browser session rather than relying on script output alone.

## Reference(s):

- [Jike Publisher Quick Reference](QUICK_REFERENCE.md)
- [Jike Publisher Examples](references/EXAMPLES.md)
- [Jike Publisher Troubleshooting](references/TROUBLESHOOTING.md)
- [Unicode Escape Guide for Chinese Content](references/UNICODE_ESCAPE.md)
- [Jike Web](https://web.okjike.com/)
- [Jike Following Feed](https://web.okjike.com/following)
- [ClawHub Skill Page](https://clawhub.ai/maoruibin/skills/jike-publisher)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and browser automation command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an active Jike login in the managed browser profile and fresh browser snapshots before page actions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
