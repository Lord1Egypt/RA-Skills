## Description:

Automatically backs up Plaud recordings to Google Drive, creates or reuses transcripts, classifies each recording, and logs audio and transcript links in Google Sheets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

External users and operators use this skill to sync new Plaud recordings into Google Drive, maintain a Google Sheets tracking log, and preserve transcripts for review or follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow reads Plaud recording metadata and content, copies recordings and transcripts into Google Drive, updates Google Sheets, and may send audio to a speech-to-text service.

Mitigation: Install and run it only on accounts whose recordings are approved for those connected services, and use least-privilege accounts where possible.

Risk: The security guidance flags supply-chain considerations for npx-based installation examples.

Mitigation: Prefer the OpenClaw install path or pin and review dependencies before using npx examples.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/agentpmt/skills/plaud-recordings-to-google-drive-sync)
- [AgentPMT workflow page](https://www.agentpmt.com/agent-workflow-skills/plaud-recordings-to-google-drive-sync)
- [AgentPMT account MCP/REST setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup)
- [Google Sheets tool skill](https://clawhub.ai/agentpmt/google-sheets)
- [Google Drive tool skill](https://clawhub.ai/agentpmt/google-drive)
- [Plaud tool skill](https://clawhub.ai/agentpmt/plaud)
- [Speech to Text With Speakers tool skill](https://clawhub.ai/agentpmt/speech-to-text-with-speakers)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON tool-call examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces workflow instructions for agent-mediated calls to Plaud, Google Drive, Google Sheets, and speech-to-text services; it does not declare a local command runtime.]

## Skill Version(s):

1.0.1 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
