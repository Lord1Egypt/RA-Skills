## Description:

Kimi Use provides Node.js tools for Kimi AI chat, image understanding, translation, and model-assisted web search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cnlangzi](https://clawhub.ai/user/cnlangzi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to call Kimi APIs from Node.js or the CLI for conversation, image analysis, translation, and search-style prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, selected image files, and the KIMI_API_KEY value can be sent to the configured remote API host.

Mitigation: Use only trusted API hosts, keep KIMI_API_HOST on the documented Kimi endpoint unless intentionally changed, and avoid sending sensitive text, screenshots, documents, or private identifiers.

Risk: The API key can be exposed if the execution environment or logs are not controlled.

Mitigation: Store KIMI_API_KEY in a protected environment, restrict access to the runtime, and rotate the key if exposure is suspected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cnlangzi/skills/kimi-use)
- [Kimi API key setup](https://www.kimi.com/code/user-center/basic-information/interface-key)
- [Kimi coding API endpoint](https://api.kimi.com/coding/v1)

## Skill Output:

**Output Type(s):** [text, shell commands, code, configuration, guidance]

**Output Format:** [Plain text or Markdown with command and JavaScript snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May stream text output when the CLI is run with streaming enabled.]

## Skill Version(s):

0.1.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
