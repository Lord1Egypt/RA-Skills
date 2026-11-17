## Description:

Operates web page elements through Chrome DevTools Protocol and a Page JS Chrome extension to reduce token use during UI automation testing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tangjing](https://clawhub.ai/user/tangjing)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and test engineers use this skill to inspect element keys and issue CDP-driven clicks, inputs, and selections in non-sensitive browser automation and UI testing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on broad browser control and an unpinned third-party Chrome extension.

Mitigation: Install only after auditing and pinning the extension source, and restrict extension host access to test or public domains.

Risk: Visible page text, form labels, and element keys may reach the configured LLM service.

Mitigation: Use a dedicated browser profile with no saved credentials and avoid login, payment, medical, government, financial, or personal-data pages.

Risk: CDP-driven actions can click buttons, fill inputs, or submit non-sensitive forms in the active browser context.

Mitigation: Use the skill in automation testing contexts and require user review before submissions, destructive actions, or operations outside test domains.

## Reference(s):

- [Chrome DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/)
- [Chrome Extensions Documentation](https://developer.chrome.com/docs/extensions/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline JavaScript and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces browser automation guidance and CDP Runtime.evaluate snippets; page element keys may include visible text or labels.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
