## Description:

Find people through an agent by helping users publish approved connection cards, search for relevant people, request introductions, and exchange contact details only after both sides consent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aeoess](https://clawhub.ai/user/aeoess)

### License/Terms of Use:

MIT-0

## Use Case:

External users and their agents use Mingle to discover relevant people, publish user-approved connection cards, request introductions, and exchange contact details only after explicit consent from both sides.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation runs npm package code and may change Claude Desktop or Cursor configuration.

Mitigation: Review the installer before use, prefer a pinned and verified package version, and confirm any AI-client configuration changes before installation.

Risk: Mingle creates a persistent local identity and may perform opt-in session-start inbox checks.

Mitigation: Keep background checks off unless explicitly desired, review local Mingle settings, and confirm that checks send only the Mingle request and authentication data needed to read the user's own inbox.

## Reference(s):

- [Mingle ClawHub Skill](https://clawhub.ai/aeoess/skills/mingle)
- [Mingle Homepage](https://aeoess.com/mingle)
- [Mingle MCP npm Package](https://www.npmjs.com/package/mingle-mcp)
- [Mingle API](https://api.aeoess.com)
- [Mingle MCP Project Page](https://github.com/aeoess/mingle-mcp)
- [Agent Passport System](https://aeoess.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent actions that publish cards, request introductions, respond to introductions, share contact lines, or change settings require explicit preview-and-confirm approval.]

## Skill Version(s):

5.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
