## Description: <br>
Google Docs API integration with managed OAuth for searching, reading, creating, and updating Google Docs documents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to connect an OpenClaw agent to Google Docs through ClawLink, then search, read, create, and update documents with confirmation before writes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The connected Google account grants this integration access to documents available to that account. <br>
Mitigation: Install only when ClawLink is trusted, review the Google consent scopes, and connect the intended Google account. <br>
Risk: Create, update, and delete actions can change Google Docs content or structure. <br>
Mitigation: Preview changes and confirm the target document and intended effect before executing any write or destructive action. <br>


## Reference(s): <br>
- [Google Docs API Overview](https://developers.google.com/docs/api) <br>
- [Google Docs Documents Resource](https://developers.google.com/docs/api/reference/rest/v1/documents) <br>
- [ClawLink OpenClaw Docs](https://docs.claw-link.dev/openclaw) <br>
- [Google Docs Skill on ClawHub](https://clawhub.ai/hith3sh/google-docs-documents) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and tool-call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live ClawLink tool catalogs and requires explicit confirmation before create, update, or delete actions.] <br>

## Skill Version(s): <br>
1.0.5 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
