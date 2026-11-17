## Description:

Use SiteSpeakAI through an OOMOL-connected account to read chatbot data, query chatbots, and create, update, or delete supported answer entries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and SiteSpeakAI account operators use the skill to inspect chatbot settings, conversations, leads, sources, and configured messages, query chatbots, and manage updated answers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can run unverified downloaded code and introduce broader persistent changes without clear user approval.

Mitigation: Review and approve CLI installation separately using a verified release, review automatic skill synchronization (disable it with OO_SKILLS_SYNC_DISABLED if appropriate), and retain confirmation requirements for updates and deletions.

## Reference(s):

- [SiteSpeakAI](https://sitespeak.ai)
- [SiteSpeakAI API Reference](https://sitespeak.ai/docs/api-reference/introduction)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-sitespeakai)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Text]

**Output Format:** [JSON responses containing SiteSpeakAI data, or chatbot answer text with source URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions use the connected SiteSpeakAI account; writes and deletions change configured answer records.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
